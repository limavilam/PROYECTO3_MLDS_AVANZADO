echo "Despliegue de Azure Function - Modelo Alzheimer"


if [ ! -f "function.json" ]; then
    echo "Error: No se encontró function.json. Asegúrate de estar en la carpeta Modelo_Deploy/"
    exit 1
fi

if [ ! -f "modelo_alzheimer.h5" ]; then
    echo "ADVERTENCIA: No se encontró modelo_alzheimer.h5"
    echo "El modelo de Alzheimer debe estar en la carpeta Modelo_Deploy/modelo_alzheimer.h5"
    read -p "¿Continuar de todos modos? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi


if ! command -v az &> /dev/null; then
    echo "Error: Azure CLI no está instalado."
    exit 1
fi

if ! command -v func &> /dev/null; then
    echo "Error: Azure Functions Core Tools no está instalado."
    exit 1
fi

# Variables
RESOURCE_GROUP="diplomado"
FUNCTION_APP_NAME="AF-Diplomado3-UN"
LOCATION="eastus"

echo "Grupo de recursos: $RESOURCE_GROUP"
echo "Function App: $FUNCTION_APP_NAME"
echo ""


if ! az group show --name $RESOURCE_GROUP &> /dev/null; then
    echo "Creando grupo de recursos"
    az group create --name $RESOURCE_GROUP --location $LOCATION
else
    echo "Grupo de recursos ya existe."
fi

if ! az functionapp show --name $FUNCTION_APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo "Creando Function App"
    
    
    STORAGE_ACCOUNT="diplomadoaf85"
    
    az functionapp create \
        --resource-group $RESOURCE_GROUP \
        --consumption-plan-location $LOCATION \
        --runtime python \
        --runtime-version 3.11 \
        --functions-version 4 \
        --name $FUNCTION_APP_NAME \
        --storage-account $STORAGE_ACCOUNT
    
    echo "Function App creada."
else
    echo "Function App ya existe."
fi

echo "Configurando cadena de conexión"
CONNECTION_STRING="CADENA_CONEXION"

az functionapp config appsettings set \
    --name $FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings "AzureWebJobsStorage=$CONNECTION_STRING" \
    --output none

echo "Cadena de conexión configurada."

echo ""
echo "Desplegando función"
func azure functionapp publish $FUNCTION_APP_NAME --python

if [ $? -eq 0 ]; then
    echo ""
    echo "Despliegue completado exitosamente"
    echo ""
else
    echo "Error en el despliegue."
    exit 1
fi

