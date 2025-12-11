if [ $# -eq 0 ]; then
    echo "Uso: ./upload_image.sh <ruta_a_imagen>"
    echo "Ejemplo: ./upload_image.sh /ruta/a/imagen.jpg"
    exit 1
fi

IMAGE_PATH="$1"
CONTAINER_NAME="alzheimer"
STORAGE_ACCOUNT="diplomadoaf85"
CONNECTION_STRING="CADENADECONEXIONABLOBSTORAGE"


if [ ! -f "$IMAGE_PATH" ]; then
    echo "Error: El archivo no existe: $IMAGE_PATH"
    exit 1
fi

FILENAME=$(basename "$IMAGE_PATH")

echo "Subiendo imagen al contenedor alzheimer"
echo "Archivo: $FILENAME"
echo "Ruta completa: $IMAGE_PATH"
echo ""

az storage blob upload \
    --container-name "$CONTAINER_NAME" \
    --name "$FILENAME" \
    --file "$IMAGE_PATH" \
    --connection-string "$CONNECTION_STRING" \
    --overwrite

if [ $? -eq 0 ]; then
    echo ""
    echo "Imagen subida exitosamente: $FILENAME"
    echo ""
    echo "La función ProcessImage se ejecutará automáticamente."

else
    echo ""
    echo "Error al subir la imagen"
    exit 1
fi

