import logging
import azure.functions as func
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


EMAIL_TO = "limavilam03@gmail.com"
EMAIL_FROM = os.environ.get("EMAIL_FROM", "noreply@azure.com")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

# Mapeo de clases
CLASS_LABELS = {
    0: "Mild Demented",
    1: "Moderate Demented",
    2: "Non Demented",
    3: "Very Mild Demented"
}

# Variable global para el modelo (se carga una vez)
model = None

def load_model_once():
    """Carga el modelo una sola vez para mejorar el rendimiento"""
    global model
    if model is None:
        current_dir = os.path.dirname(__file__)
        
        possible_paths = [
            os.path.join(os.path.dirname(current_dir), 'modelo_alzheimer.h5'),  
            os.path.join('/home/site/wwwroot', 'modelo_alzheimer.h5'), 
            os.path.join(current_dir, 'modelo_alzheimer.h5'),  
            'modelo_alzheimer.h5' 
        ]
        
        model_path = None
        for path in possible_paths:
            if os.path.exists(path):
                model_path = path
                break
        
        if model_path:
            logging.info(f"Cargando modelo desde: {model_path}")
            model = load_model(model_path)
            logging.info("Modelo cargado exitosamente")
        else:
        
            logging.error(f"Modelo no encontrado. Directorio actual: {current_dir}")
            logging.error(f"Directorio raíz del proyecto: {os.path.dirname(current_dir)}")
            logging.error(f"Archivos en directorio actual: {os.listdir(current_dir) if os.path.exists(current_dir) else 'No existe'}")
            if os.path.exists(os.path.dirname(current_dir)):
                logging.error(f"Archivos en directorio raíz: {os.listdir(os.path.dirname(current_dir))}")
            raise FileNotFoundError(f"Modelo no encontrado. Buscado en: {possible_paths}")
    return model

def preprocess_image(image_bytes):
    """
    Preprocesa la imagen para el modelo
    - Decodifica la imagen
    - Redimensiona a 224x224
    - Convierte a 3 canales
    - Aplica preprocesamiento de VGG16
    """
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            raise ValueError("No se pudo decodificar la imagen")
        
        # Redimensionar a 224x224
        img = cv2.resize(img, (224, 224))
        
        # Expandir a 3 canales (replicar canal gris)
        img_3ch = np.stack([img, img, img], axis=-1)
        
        img_batch = np.expand_dims(img_3ch, axis=0)
        
        img_preprocessed = preprocess_input(img_batch.astype(np.float32))
        
        return img_preprocessed
    except Exception as e:
        logging.error(f"Error en preprocesamiento: {str(e)}")
        raise

def predict_image(model, image_preprocessed):
    """
    Realiza la predicción con el modelo
    """
    try:
        predictions = model.predict(image_preprocessed, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        class_probabilities = {
            CLASS_LABELS[i]: float(predictions[0][i]) 
            for i in range(len(CLASS_LABELS))
        }
        
        return predicted_class, confidence, class_probabilities
    except Exception as e:
        logging.error(f"Error en predicción: {str(e)}")
        raise

def send_email(image_name, predicted_class, confidence, class_probabilities):
    """
    Envía un correo electrónico con los resultados
    """
    try:
      
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = f"Resultados del Análisis de Alzheimer - {image_name}"
        
      
        body = f"""
        Resultados del Análisis de Imagen MRI
        
        Nombre de la imagen: {image_name}
        
        Resultado de la predicción:
        - Clase predicha: {CLASS_LABELS[predicted_class]}
        - Confianza: {confidence:.2%}
        
        Probabilidades por clase:
        """
        
        for class_name, prob in sorted(class_probabilities.items(), key=lambda x: x[1], reverse=True):
            body += f"  - {class_name}: {prob:.2%}\n"
        
        body += f"""
        
        Este es un mensaje automático del sistema de análisis de Alzheimer.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        

        if EMAIL_PASSWORD:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_FROM, EMAIL_TO, text)
            server.quit()
            logging.info(f"Correo enviado exitosamente a {EMAIL_TO}")
        else:
            logging.warning("EMAIL_PASSWORD no configurado. No se enviará correo.")
            logging.info(f"Contenido del correo que se enviaría:\n{body}")
            
    except Exception as e:
        logging.error(f"Error al enviar correo: {str(e)}")
        raise

def main(myblob: func.InputStream) -> None:
    """
    Función principal que se ejecuta cuando se sube un blob al contenedor
    """
    logging.info(f'Python blob trigger function processed blob \n'
                 f'Name: {myblob.name}\n'
                 f'Blob Size: {myblob.length} bytes')
    
    try:
        image_name = os.path.basename(myblob.name)
        logging.info(f"Procesando imagen: {image_name}")
        
        image_bytes = myblob.read()
        logging.info(f"Imagen leída: {len(image_bytes)} bytes")
        
        logging.info("Preprocesando imagen")
        image_preprocessed = preprocess_image(image_bytes)
        logging.info("Imagen preprocesada exitosamente")
        
  
        logging.info("Cargando modelo")
        model = load_model_once()
        

        logging.info("Realizando predicción")
        predicted_class, confidence, class_probabilities = predict_image(model, image_preprocessed)
        
        logging.info(f"Predicción completada: {CLASS_LABELS[predicted_class]} (confianza: {confidence:.2%})")
        
        logging.info("Enviando correo")
        send_email(image_name, predicted_class, confidence, class_probabilities)
        
        logging.info(f"Procesamiento completado exitosamente para {image_name}")
        
    except Exception as e:
        logging.error(f"Error al procesar la imagen: {str(e)}", exc_info=True)
        raise
