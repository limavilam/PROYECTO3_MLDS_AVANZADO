from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from azure.storage.blob import BlobServiceClient

import os
os.environ["TF_NEED_TENSORRT"] = "0"


app = FastAPI()

# ---------------------------
# CONFIGURACIÓN BLOB STORAGE
# ---------------------------

AZURE_CONNECTION_STRING = os.getenv("AZURE_BLOB_CONNECTION_STRING")

CONTAINER_NAME = "modelos"
BLOB_NAME = "modelo_alzheimer.h5"

# archivo temporal donde se descargará el modelo
LOCAL_MODEL_PATH = "/tmp/modelo_alzheimer.h5"


def download_model_from_blob():
    """
    Descarga el modelo desde Azure Blob Storage solo si no existe localmente.
    """
    if os.path.exists(LOCAL_MODEL_PATH):
        print("✔ Modelo ya existe localmente. No se descarga.")
        return

    print("⏬ Descargando modelo desde Azure Blob Storage...")

    try:
        blob_service = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service.get_container_client(CONTAINER_NAME)
        blob_client = container_client.get_blob_client(BLOB_NAME)

        with open(LOCAL_MODEL_PATH, "wb") as f:
            f.write(blob_client.download_blob().readall())

        print("✔ Modelo descargado exitosamente")

    except Exception as e:
        print("❌ Error descargando el modelo:", str(e))
        raise e


# Descargar modelo al iniciar
download_model_from_blob()

print("⏳ Cargando modelo en memoria...")
model = load_model(LOCAL_MODEL_PATH)
print("✔ Modelo cargado correctamente")


CLASS_NAMES = ["Non Demented", "Very Mild Demented", "Mild Demented", "Moderate Demented"]


def preprocess_mri_image(image_bytes):
    """
    Preprocesamiento igual a tu notebook:
    - grayscale
    - resize 224x224
    - 3 canales
    - normalizar y preprocess_input
    """

    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Formato de imagen inválido")

    img = cv2.resize(img, (224, 224))

    img_3ch = np.stack([img, img, img], axis=-1)
    img_3ch = img_3ch.astype("float32") / 255.0
    img_3ch = preprocess_input(img_3ch)

    return np.expand_dims(img_3ch, axis=0)

@app.get("/")
async def root():
    return {"message": "API de predicción de Alzheimer está en funcionamiento."}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    if not file.content_type.startswith("image/"):
        return JSONResponse(
            content={"error": "Debe enviar un archivo de imagen"},
            status_code=400
        )

    try:
        image_bytes = await file.read()
        img_processed = preprocess_mri_image(image_bytes)

        preds = model.predict(img_processed)
        predicted_class = np.argmax(preds, axis=1)[0]

        return {
            "prediction_class_index": int(predicted_class),
            "prediction_label": CLASS_NAMES[predicted_class],
            "probabilities": preds.tolist()
        }

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
