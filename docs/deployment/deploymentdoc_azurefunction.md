# Despliegue de Modelo con Azure Functions

## Infraestructura

* **Nombre del modelo:**
  `ModeloAlzheimerAccOptimo.ipynb`

* **Plataforma de despliegue:**
  **Azure Functions** (Python 3.11, Función de Consumo), utilizando **Azure Blob Storage** como trigger y almacenamiento.

* **Requisitos técnicos:**

  * **Azure Function App**
    * Python 3.11
    * Azure Functions 
    * TensorFlow 2.15.0
    * OpenCV (opencv-python-headless 4.8.1.78)
    * NumPy 1.24.3
    * Pillow 10.1.0
    * azure-functions
    * azure-storage-blob
  * **Azure Storage Account**
    * Blob Storage con contenedor `alzheimer`
    * Cadena de conexión configurada en `AzureWebJobsStorage`
  * **Infraestructura**
    * Azure CLI
    * Azure Functions Core Tools (`func`)
    * Azure Subscription
    * Azure Storage Account
    * Azure Function App (Consumption Plan)

* **Requisitos de seguridad:**
  * Autenticación mediante Azure CLI (`az login`).
  * Variables de entorno protegidas en Azure Function App.
  * Modelo almacenado en el sistema de archivos de la Function App.
  * Cadena de conexión de Storage Account protegida.
  * Configuración de email mediante variables de entorno (SMTP).
  * Control de acceso basado en RBAC para recursos de Azure.

* **Diagrama de arquitectura:**

![Diagrama de sequencia](/docs/diagramas/diagrama_secuencia_af.png)

![Diagrama de arquitectura](/docs/diagramas/diagrama_arquitectura_af.png)

---

## Arquitectura del Sistema

### **Flujo de Procesamiento**

1. **Carga de Imagen**: El usuario sube una imagen al contenedor `alzheimer` en Azure Blob Storage.
2. **Trigger Automático**: Azure Function `ProcessImage` se activa automáticamente mediante un blob trigger.
3. **Preprocesamiento**: La imagen se decodifica, redimensiona a 224x224 y se preprocesa para VGG16.
4. **Predicción**: El modelo TensorFlow carga (si no está cargado) y realiza la predicción.
5. **Notificación**: Se envía un correo electrónico con los resultados de la predicción.
6. **Logging**: Todo el proceso se registra en Application Insights.

### **Componentes Principales**

* **Function App**: `AF-Diplomado3-UN`
* **Resource Group**: `diplomado`
* **Storage Account**: `diplomadoaf85`
* **Blob Container**: `alzheimer`
* **Function**: `ProcessImage` (Blob Trigger)
* **Modelo**: `modelo_alzheimer.h5` (152MB)

---

## Código de despliegue

* **Estructura del proyecto:**
  ```
  modelo_deploy_azurefunction/
  ├── ProcessImage/
  │   ├── __init__.py          # Código principal de la función
  │   └── function.json        # Configuración del trigger
  ├── host.json                # Configuración del host
  ├── requirements.txt         # Dependencias Python
  ├── deploy.sh                # Script de despliegue
  ├── upload_model.sh          # Script para subir el modelo
  ├── upload_image.sh          # Script para subir imágenes
  ├── configure_email.sh       # Script para configurar email
  └── local.settings.json.disable  # Plantilla de configuración local
  ```

* **Archivos principales:**
  * `/modelo_deploy_azurefunction/ProcessImage/__init__.py` - Lógica de procesamiento
  * `/modelo_deploy_azurefunction/ProcessImage/function.json` - Configuración del blob trigger
  * `/modelo_deploy_azurefunction/host.json` - Configuración del runtime
  * `/modelo_deploy_azurefunction/requirements.txt` - Dependencias

* **Variables de entorno requeridas:**
  ```
  AzureWebJobsStorage          # Cadena de conexión al Storage Account
  EMAIL_FROM                  # Email remitente (ej: limavilam03@gmail.com)
  EMAIL_PASSWORD              # Contraseña de aplicación para SMTP
  SMTP_SERVER                 # Servidor SMTP (ej: smtp.gmail.com)
  SMTP_PORT                   # Puerto SMTP (ej: 587)
  FUNCTIONS_WORKER_RUNTIME    # python
  ```

* **Configuración del Blob Trigger:**
  * **Path**: `alzheimer/{name}`
  * **Connection**: `AzureWebJobsStorage`
  * **Direction**: `in`
  * **Type**: `blobTrigger`

---

## Documentación del despliegue

### **Instrucciones de instalación**

1. Instalar herramientas requeridas:

   ```bash
   # Instalar Azure CLI
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   
   # Instalar Azure Functions Core Tools
   npm install -g azure-functions-core-tools@4 --unsafe-perm true
   
   # Verificar instalación
   az --version
   func --version
   ```

2. Iniciar sesión en Azure:

   ```bash
   az login
   ```

3. Navegar al directorio del proyecto:

   ```bash
   cd modelo_deploy_azurefunction
   ```

---

### **Instrucciones de configuración**

#### **1. Preparar el modelo**

El modelo debe estar en formato `.h5` y ubicado en el directorio raíz del proyecto:

```bash
# Copiar el modelo al directorio de despliegue
cp /ruta/al/modelo/modelo_alzheimer.h5 ./modelo_deploy_azurefunction/
```

#### **2. Configurar variables de entorno**

Editar `deploy.sh` con los valores correctos:

```bash
RESOURCE_GROUP="diplomado"
FUNCTION_APP_NAME="AF-Diplomado3-UN"
LOCATION="eastus"
STORAGE_ACCOUNT="diplomadoaf85"
CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=..."
```

#### **3. Crear Storage Account (si no existe)**

```bash
az storage account create \
  --name diplomadoaf85 \
  --resource-group diplomado \
  --location eastus \
  --sku Standard_LRS
```

#### **4. Crear contenedor de blobs**

```bash
az storage container create \
  --name alzheimer \
  --account-name diplomadoaf85 \
  --connection-string "CADENA_DE_CONEXION"
```

---

### **Desplegar la Function App**


```bash
cd modelo_deploy_azurefunction
chmod +x deploy.sh
./deploy.sh
```

El script:
- Verifica que existan las herramientas necesarias
- Crea el Resource Group si no existe
- Crea la Function App si no existe
- Configura la cadena de conexión
- Despliega el código de la función


### **Subir el modelo**

Como el modelo es demasiado grande para incluirse en el despliegue estándar. Se debe subir manualmente:

```bash
cd modelo_deploy_azurefunction
chmod +x upload_model.sh
./upload_model.sh
```

O manualmente usando la API de Kudu:

```bash
# Obtener credenciales de publicación
PUBLISH_PROFILE=$(az functionapp deployment list-publishing-profiles \
  --name AF-Diplomado3-UN \
  --resource-group diplomado \
  --xml)

# Extraer usuario y contraseña
USERNAME=$(echo "$PUBLISH_PROFILE" | grep -oP '(?<=userName=")[^"]*' | head -1)
PASSWORD=$(echo "$PUBLISH_PROFILE" | grep -oP '(?<=userPwd=")[^"]*' | head -1)

# Subir modelo
curl -X PUT \
  -u "$USERNAME:$PASSWORD" \
  -T modelo_alzheimer.h5 \
  "https://AF-Diplomado3-UN.scm.azurewebsites.net/api/vfs/site/wwwroot/modelo_alzheimer.h5"
```

El modelo quedará disponible en: `/home/site/wwwroot/modelo_alzheimer.h5`

---

### **Configurar notificaciones por email**

```bash
cd modelo_deploy_azurefunction
chmod +x configure_email.sh
# Editar configure_email.sh con las credenciales
./configure_email.sh
```

**Nota**: Para Gmail, es necesario usar una "Contraseña de aplicación" en lugar de la contraseña normal.

---

### **Instrucciones de uso**

1. **Subir una imagen al contenedor de blobs:**

   ```bash
   cd modelo_deploy_azurefunction
   chmod +x upload_image.sh
   # Editar upload_image.sh con la cadena de conexión correcta
   ./upload_image.sh /ruta/a/imagen.jpg
   ```

   O usando Azure CLI directamente:

   ```bash
   az storage blob upload \
     --container-name alzheimer \
     --name imagen.jpg \
     --file /ruta/a/imagen.jpg \
     --connection-string "CADENA_DE_CONEXION" \
     --overwrite
   ```

   O subirlo directamente al blob storage.

2. **La función se ejecuta automáticamente:**
   - Al detectar el nuevo blob en `alzheimer/{name}`, la función `ProcessImage` se activa.
   - La imagen se procesa y se realiza la predicción.
   - Se envía un correo electrónico con los resultados.

3. **Verificar logs:**

   ```bash
   az functionapp logs tail \
     --name AF-Diplomado3-UN \
     --resource-group diplomado
   ```

4. **Resultados de la predicción:**
   - **Clases posibles:**
     - `Mild Demented` (Clase 0)
     - `Moderate Demented` (Clase 1)
     - `Non Demented` (Clase 2)
     - `Very Mild Demented` (Clase 3)
   - El correo incluye:
     - Clase predicha
     - Nivel de confianza
     - Probabilidades para todas las clases

---

### **Instrucciones de mantenimiento**

* **Actualizar el modelo TensorFlow**

  1. Subir el nuevo modelo:

     ```bash
     ./upload_model.sh
     ```

  2. Reiniciar la Function App:

     ```bash
     az functionapp restart \
       --name AF-Diplomado3-UN \
       --resource-group diplomado
     ```

* **Actualizar el código de la función**

  1. Modificar el código en `ProcessImage/__init__.py`
  2. Redesplegar:

     ```bash
     func azure functionapp publish AF-Diplomado3-UN --python
     ```

* **Actualizar dependencias**

  1. Modificar `requirements.txt`
  2. Redesplegar la función

* **Rotación de variables de entorno**

  ```bash
  az functionapp config appsettings set \
    --name AF-Diplomado3-UN \
    --resource-group diplomado \
    --settings "NUEVA_VARIABLE=valor"
  ```

* **Revisión de logs**

  ```bash
  # Logs en tiempo real
  az functionapp logs tail \
    --name AF-Diplomado3-UN \
    --resource-group diplomado
  
  # Ver logs en Azure Portal
  # Function App > Functions > ProcessImage > Monitor
  ```

* **Monitoreo y métricas**

  - Application Insights está habilitado por defecto
  - Ver métricas en Azure Portal: Function App > Monitor
  - Revisar ejecuciones en: Function App > Functions > ProcessImage > Monitor

---

## Características Técnicas

### **Preprocesamiento de Imágenes**

- Decodificación de imagen desde bytes
- Redimensionamiento a 224x224 píxeles
- Conversión a escala de grises y expansión a 3 canales
- Preprocesamiento VGG16 (`preprocess_input`)

### **Modelo**

- Arquitectura: Basada en VGG16
- Formato: `.h5` (Keras/TensorFlow)
- Tamaño aproximado: 152MB
- Carga: Lazy loading (se carga una sola vez al primer uso)

### **Notificaciones**

- Protocolo: SMTP
- Formato: Texto plano
- Contenido: Resultados de predicción con probabilidades
- Destinatario: Configurado en `EMAIL_TO` (hardcoded en código)

### **Timeout y Recursos**

- Timeout de función: 10 minutos (configurado en `host.json`)
- Plan: Consumption (escalado automático)
- Memoria: Hasta 1.5GB por instancia

---
