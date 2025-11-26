# Definición de los datos

## Origen de los datos

- [ ] Especificar la fuente de los datos y la forma en que se obtuvieron.

Los datos utilizados en este proyecto se encuentran en formato **Parquet** y provienen del dataset
“Alzheimer MRI Disease Classification Dataset” (Kaggle), el cual contiene imágenes de resonancia magnética (MRI)
clasificadas en cuatro categorías:

- Mild Demented  
- Moderate Demented  
- Non Demented  
- Very Mild Demented  

El dataset fue descargado y preprocesado previamente para generar los archivos `train.parquet` y `test.parquet`,
los cuales se almacenan en Google Drive en las siguientes rutas:

-     /content/drive/MyDrive/DIPLOMADO2/PROYECTO3_MLDS_AVANZADO/train.parquet
-     /content/drive/MyDrive/DIPLOMADO2/PROYECTO3_MLDS_AVANZADO/test.parquet

Cada archivo contiene imágenes codificadas en formato binario junto con su etiqueta de clase.

## Especificación de los scripts para la carga de datos

- [ ] Especificar los scripts utilizados para la carga de los datos.

Se implementó una función llamada `decodificar_imagen` que actúa como script de carga y transformación inicial.
Esta función realiza:

1. Conversión del campo `image.bytes` a un arreglo NumPy.
2. Decodificación de la imagen desde binario usando OpenCV.
3. Carga en escala de grises.
4. Redimensionamiento a 224x224 píxeles.
5. Expansión a 3 canales para compatibilidad con modelos preentrenados.

## Referencias a rutas o bases de datos origen y destino

- [ ] Especificar las rutas o bases de datos de origen y destino para los datos.

En este proyecto se utilizan dos conjuntos principales de referencias a rutas:

- **Ruta de datos de origen**:

Los datos originales se encuentran almacenados en formato **Parquet** en Google Drive.
Estas rutas corresponden al dataset antes de cualquier transformación:

1. **Ruta de entrenamiento (origen):**
  `/content/drive/MyDrive/DIPLOMADO2/PROYECTO3_MLDS_AVANZADO/train.parquet`

2. **Ruta de prueba (origen):**
  `/content/drive/MyDrive/DIPLOMADO2/PROYECTO3_MLDS_AVANZADO/test.parquet`

Estos archivos contienen:
- Imágenes codificadas como diccionarios con campos binarios (`image["bytes"]`)
- Etiquetas numéricas (`label`)

- **Ruta de datos procesados (destino):**
Después de decodificar, normalizar y transformar las imágenes,
los datos procesados pueden almacenarse en un directorio destino:

1. **Ruta destino:**
  `/content/drive/MyDrive/DIPLOMADO2/PROYECTO3_MLDS_AVANZADO/procesado/`

En este destino se podrían guardar:

- `X_train.npy`  (imágenes procesadas de entrenamiento)
- `y_train.npy`  (etiquetas)
- `X_test.npy`
- `y_test.npy`


### Rutas de origen de datos

- [ ] Especificar la ubicación de los archivos de origen de los datos.

Como se mencionó anteriormente, los datos utilizados en este proyecto provienen del dataset Alzheimer MRI Disease Classification, disponible en Kaggle.
Para su procesamiento y modelado en Google Colab, los archivos fueron previamente descargados y almacenados en Google Drive en formato Parquet.
Rutas de origen de los archivos:

    /content/drive/MyDrive/DIPLOMADO2/PROYECTO3_MLDS_AVANZADO/train.parquet  
    /content/drive/MyDrive/DIPLOMADO2/PROYECTO3_MLDS_AVANZADO/test.parquet

- [ ] Especificar la estructura de los archivos de origen de los datos.

Tras inspeccionar los datasets se obtuvo lo siguiente:

    train.parquet

- **Número de registros:** 5120
- **Columnas totales:** 2
- **Uso de memoria:** 80.1 KB

| # | Columna | Non-Null Count | Tipo   |
|---|---------|----------------|--------|
| 0 | label   | 5120           | int64  |
| 1 | image   | 5120           | object |

**Tipos de datos:**
- `int64` (1 columna)
- `object` (1 columna)

      test.parquet

- **Número de registros:** 1280
- **Columnas totales:** 2
- **Uso de memoria:** 20.1 KB

| # | Columna | Non-Null Count | Tipo   |
|---|---------|----------------|--------|
| 0 | label   | 1280           | int64  |
| 1 | image   | 1280           | object |

**Tipos de datos:**

`int64` (1 columna)

`object` (1 columna)


- [ ] Describir los procedimientos de transformación y limpieza de los datos.

1. **Eliminación de imágenes corruptas**
   - Se verifica que cada imagen sea válida (no nula y tamaño mayor a cero).
   - Se eliminan filas que no cumplan esta condición.

2. **Detección de duplicados**
   - Cada imagen se convierte en un hash MD5.
   - Se identifican duplicados (No hay duplicados en el dataset).

3. **Normalización**
   - Las imágenes se normalizan a valores entre 0 y 1.

4. **Balance de clases**
   - Se revisa la distribución de clases.
   - Actualmente, el dataset de entrenamiento está desbalanceado:
     ```
     Non Demented: 2566
     Very Mild Demented: 1781
     Mild Demented: 724
     Moderate Demented: 49
     ```

5. **Data Augmentation (pendiente)**
   - Aunque aún no se ha implementado, se planea generar variaciones artificiales de las imágenes durante el entrenamiento:
     - Rotaciones aleatorias
     - Desplazamientos horizontales y verticales
     - Zoom
     - Volteo horizontal
     - Ajuste de brillo
   - Esto permitirá aumentar la diversidad del dataset y mejorar la capacidad de generalización del modelo.

### Base de datos de destino

- [ ] Especificar la base de datos de destino para los datos.
- [ ] Especificar la estructura de la base de datos de destino.
- [ ] Describir los procedimientos de carga y transformación de los datos en la base de datos de destino.
