# Despliegue de modelos

## Infraestructura

* **Nombre del modelo:**
  `ModeloAlzheimerAccOptimo.ipynb`

* **Plataforma de despliegue:**
  **Azure Container Apps**, utilizando imágenes Docker almacenadas en **Azure Container Registry (ACR)**.

* **Requisitos técnicos:**

  * **Backend**

    * Python 3.10+
    * TensorFlow 2.x
    * FastAPI
    * Uvicorn
    * python-multipart
    * Docker Engine 24+
    * Puerto expuesto: **8080**
  * **Frontend**

    * Node.js 18+
    * npm 10+
    * Framework: React/Vite
    * Docker Engine 24+
    * Puerto expuesto en contenedor: **80**
  * **Infraestructura**

    * Azure CLI
    * Azure Subscription
    * Azure Container Registry
    * Azure Container Apps Environment

* **Requisitos de seguridad:**

  * Autenticación de ACR mediante `az acr login` o identidades administradas.
  * Encriptación en tránsito mediante HTTPS automático en Container Apps.
  * Variables de entorno protegidas en Azure Container Apps.
  * Modelos y contenedores almacenados únicamente en el ACR privado.
  * Restricciones de CORS configuradas entre frontend y backend.
  * Control de acceso basado en RBAC para recursos de Azure.

* **Diagrama de arquitectura:**

![Diagrama de sequencia](/docs/diagramas/DiagramaDeSequencia.png)

![Diagrama de arquitectura](/docs/diagramas/DiagramaDeArquitectura.png)
---

## Código de despliegue

* **Archivo principal:**
  Backend: `Dockerfile` + `main.py`
  Frontend: `Dockerfile` + `src/main.jsx` 

* **Rutas de acceso a los archivos:**

  * Backend:

    * `/backend/api/main.py`
    * `/backend/Dockerfile`
    * `/backend/requirements.txt`
  * Frontend:
    * `/frontend/Dockerfile`
    * `/frontend/`
  * Infraestructura:

    * Imágenes: `ACR_NAME.azurecr.io/alzheimer-front-app:latest`
    * Imágenes: `ACR_NAME.azurecr.io/alzheimer-app:latest`

* **Variables de entorno:**

  ```
  RESOURCE_GROUP
  LOCATION
  ACR_NAME
  ENVIRONMENT_NAME

  BACKEND_APP_NAME
  BACKEND_IMAGE_NAME

  FRONTEND_APP_NAME
  FRONTEND_IMAGE_NAME

  VITE_API_URL

  MODEL_PATH="/app/model"
  ```

---

## Documentación del despliegue

### **Instrucciones de instalación**

1. Instalar herramientas requeridas:

   ```bash
   sudo apt install docker.io
   pip install --upgrade azure-cli
   ```

2. Iniciar sesión en Azure:

   ```bash
   az login
   ```

3. Crear o usar un Azure Container Registry:

   ```bash
   az acr create --name $ACR_NAME --resource-group $RESOURCE_GROUP \
     --sku Basic --admin-enabled true
   ```

4. Hacer login en el ACR:

   ```bash
   az acr login --name $ACR_NAME
   ```

---

### **Instrucciones de configuración**

#### **1. Build de imágenes Docker**

**Backend**

```bash
docker build -t $ACR_NAME.azurecr.io/$BACKEND_IMAGE_NAME:latest ./backend
```

**Frontend**

```bash
docker build -t $ACR_NAME.azurecr.io/$FRONTEND_IMAGE_NAME:latest ./frontend
```

#### **2. Push de imágenes**

```bash
docker push $ACR_NAME.azurecr.io/$BACKEND_IMAGE_NAME:latest
docker push $ACR_NAME.azurecr.io/$FRONTEND_IMAGE_NAME:latest
```

#### **3. Crear el entorno de Azure Container Apps (si no existe)**

```bash
az containerapp env create \
  --name $ENVIRONMENT_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION
```

---

### **Crear los Container Apps**

#### **Backend**

```bash
az containerapp create \
  --name $BACKEND_APP_NAME \
  --image $ACR_NAME.azurecr.io/$BACKEND_IMAGE_NAME:latest \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT_NAME \
  --registry-server $ACR_NAME.azurecr.io \
  --ingress external \
  --target-port 8080 \
  --env-vars AZURE_BLOB_CONNECTION_STRING="mi_cadena_de_conexion"
```

#### **Frontend**

```bash
az containerapp create \
  --name $FRONTEND_APP_NAME \
  --image $ACR_NAME.azurecr.io/$FRONTEND_IMAGE_NAME:latest \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT_NAME \
  --registry-server $ACR_NAME.azurecr.io \
  --ingress external \
  --target-port 80 \
  --env-vars VITE_API_URL="https://URL_DEL_BACKEND"
```

---

### **Instrucciones de uso**

1. El usuario ingresa al frontend desplegado en Azure.

2. Carga una imagen en la interfaz.

3. El frontend envía:

   ```
   POST /predict
   Content-Type: multipart/form-data
   ```

   al backend.

4. El backend:

   * Lee la imagen.
   * La procesa con **TensorFlow**.
   * Devuelve la predicción al frontend.

5. El frontend muestra el resultado.

![frontend](/docs/images/frontend.png)

6. El backend genera y expone un Swagger con los detalles de los endpoints expuestos y su forma de uso

![swagger](/docs/images/swagger.png)
---

### **Instrucciones de mantenimiento**

* **Actualizar el modelo TensorFlow**

  * Reemplazar el modelo dentro en el blobStorage en caso de obtener una version mejorada del modelo en formato .h5
  * Reconstruir la imagen:

    ```bash
    docker build -t $ACR_NAME.azurecr.io/$BACKEND_IMAGE_NAME:latest ./backend
    docker push $ACR_NAME.azurecr.io/$BACKEND_IMAGE_NAME:latest
    ```
  * Actualizar Container App:

    ```bash
    az containerapp update \
      --name $BACKEND_APP_NAME \
      --resource-group $RESOURCE_GROUP \
      --image $ACR_NAME.azurecr.io/$BACKEND_IMAGE_NAME:latest
    ```

* **Actualizar el frontend**

  * Modificar código → `npm run build`
  * Reconstruir imagen, push y update igual que arriba.

* **Rotación de variables de entorno**

  * Editarlas desde Azure Portal o CLI:

    ```bash
    az containerapp update \
      --name $FRONTEND_APP_NAME \
      --resource-group $RESOURCE_GROUP \
      --set-env-vars VITE_API_URL="nuevo valor"
    ```

* **Revisión de logs**

  ```bash
  az containerapp logs show \
    --name $BACKEND_APP_NAME \
    --resource-group $RESOURCE_GROUP
  ```

---