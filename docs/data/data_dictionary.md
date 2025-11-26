# Diccionario de datos

## Base de datos 1

**Descripción:**  

Dataset de imágenes MRI para clasificación del Alzheimer, almacenado en archivos `.parquet`. 
Cada registro contiene la etiqueta de la clase de Alzheimer y la imagen codificada en bytes.

| Variable | Descripción                                        | Tipo de dato | Rango/Valores posibles                        | Fuente de datos |
|----------|---------------------------------------------------|-------------|-----------------------------------------------|----------------|
| label    | Código numérico de la clase de Alzheimer          | int64       | 0: Mild Demented, 1: Moderate Demented, 2: Non Demented, 3: Very Mild Demented | Kaggle - Alzheimer MRI Disease Classification Dataset |
| image    | Imagen codificada en bytes dentro de un diccionario | object      | Diccionario con clave `"bytes"` que contiene la imagen | Kaggle - Alzheimer MRI Disease Classification Dataset |


