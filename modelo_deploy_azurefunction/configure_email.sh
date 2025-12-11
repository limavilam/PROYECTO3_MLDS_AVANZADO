echo "Configuración de Email para Azure Function"

# Variables
RESOURCE_GROUP="diplomado"
FUNCTION_APP_NAME="AF-Diplomado3-UN"
EMAIL_FROM="limavilam03@gmail.com"
EMAIL_PASSWORD="tvyhpgyurafucymu"  #Contraseña de aplicacion
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT="587"

EMAIL_PASSWORD_CLEAN=$(echo "$EMAIL_PASSWORD" | tr -d ' ')

echo "Function App: $FUNCTION_APP_NAME"
echo "Resource Group: $RESOURCE_GROUP"
echo "Email FROM: $EMAIL_FROM"
echo ""

if ! command -v az &> /dev/null; then
    echo "Error: Azure CLI no está instalado."
    exit 1
fi

# Verificar que la Function App existe
if ! az functionapp show --name $FUNCTION_APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo "Error: Function App '$FUNCTION_APP_NAME' no encontrada."
    exit 1
fi

echo "Configurando variables de entorno de email"

# Configurar las variables de entorno
az functionapp config appsettings set \
    --name $FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings \
        "EMAIL_FROM=$EMAIL_FROM" \
        "EMAIL_PASSWORD=$EMAIL_PASSWORD_CLEAN" \
        "SMTP_SERVER=$SMTP_SERVER" \
        "SMTP_PORT=$SMTP_PORT" \
    --output none

if [ $? -eq 0 ]; then
    echo ""
    echo "Configuración de email completada exitosamente!"
    echo ""
    echo "Variables configuradas:"
    echo "  - EMAIL_FROM: $EMAIL_FROM"
    echo "  - EMAIL_PASSWORD: [configurada]"
    echo "  - SMTP_SERVER: $SMTP_SERVER"
    echo "  - SMTP_PORT: $SMTP_PORT"
    echo ""
    echo "La función se reiniciará automáticamente para aplicar los cambios."
    echo ""
else
    echo "Error al configurar las variables de entorno."
    exit 1
fi

