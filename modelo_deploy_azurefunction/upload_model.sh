# Script para subir el modelo directamente a Azure Function
# Esto es necesario porque el modelo es muy grande (152MB)

echo "Subiendo modelo a Azure Function"

MODEL_PATH="modelo_alzheimer.h5"
FUNCTION_APP="AF-Diplomado3-UN"
RESOURCE_GROUP="diplomado"

if [ ! -f "$MODEL_PATH" ]; then
    echo "Error: No se encontró $MODEL_PATH"
    exit 1
fi

echo "Modelo: $MODEL_PATH"
echo "Tamaño: $(du -h $MODEL_PATH | cut -f1)"
echo ""

echo "Subiendo modelo usando Kudu API"

PUBLISH_PROFILE=$(az functionapp deployment list-publishing-profiles \
    --name $FUNCTION_APP \
    --resource-group $RESOURCE_GROUP \
    --xml 2>/dev/null)

if [ -z "$PUBLISH_PROFILE" ]; then
    echo "Error: No se pudieron obtener las credenciales de publicación"
    exit 1
fi

USERNAME=$(echo "$PUBLISH_PROFILE" | grep -oP '(?<=userName=")[^"]*' | head -1)
PASSWORD=$(echo "$PUBLISH_PROFILE" | grep -oP '(?<=userPwd=")[^"]*' | head -1)
FUNCTION_URL="https://${FUNCTION_APP}.scm.azurewebsites.net"

echo "Subiendo a: $FUNCTION_URL/api/vfs/site/wwwroot/$MODEL_PATH"

curl -X PUT \
    -u "$USERNAME:$PASSWORD" \
    -T "$MODEL_PATH" \
    "$FUNCTION_URL/api/vfs/site/wwwroot/$MODEL_PATH" \
    --progress-bar

if [ $? -eq 0 ]; then
    echo ""
    echo "Modelo subido exitosamente"
    echo ""
    echo "El modelo ahora está disponible en: /home/site/wwwroot/modelo_alzheimer.h5"
    echo ""
else
    echo ""
    echo "Error al subir el modelo"
    echo ""
    exit 1
fi

