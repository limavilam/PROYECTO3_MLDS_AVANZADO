# Reporte de Datos

Este documento contiene los resultados del análisis exploratorio de datos.

## Resumen general de los datos


El análisis se realizó sobre dos conjuntos de datos, `df_train` y `df_test`, que contienen imágenes de resonancia magnética (MRI) y sus respectivas etiquetas de diagnóstico relacionadas con el Alzheimer.

---

### **Número de Observaciones**

| Dataset    | Cantidad de imágenes |
| ---------- | -------------------- |
| `df_train` | 5120 imágenes        |
| `df_test`  | 1280 imágenes        |

---

### **Variables**

| Dataset                | Columnas | Descripción                                            |
| ---------------------- | -------- | ------------------------------------------------------ |
| `df_train` / `df_test` | `image`  | Contiene los bytes de la imagen y metadatos asociados. |
| `df_train` / `df_test` | `label`  | Variable objetivo que indica el nivel de demencia.     |

---

### **Tipos de Datos**

| Columna | Tipo de dato | Descripción                                       |
| ------- | ------------ | ------------------------------------------------- |
| `image` | `object`     | Contiene diccionarios con los bytes de la imagen. |
| `label` | `int64`      | Nivel de demencia asociado a la imagen.           |

---

### **Valores Faltantes**

| Dataset    | Valores nulos           |
| ---------- | ----------------------- |
| `df_train` | 0 en todas las columnas |
| `df_test`  | 0 en todas las columnas |

---

### Distribución de la Variable Objetivo ('label') en `df_train`:

La variable `label` es de tipo categórico-ordinal, representando diferentes estados de demencia de la siguiente manera:

---
| Código | Clase              | Descripción       |
| ------ | ------------------ | ----------------- |
| 0      | Mild Demented      | Demencia Leve     |
| 1      | Moderate Demented  | Demencia Moderada |
| 2      | Non Demented       | No Demencia       |
| 3      | Very Mild Demented | Demencia Muy Leve |
---

La distribución de estas clases en el conjunto de entrenamiento es:

---
| Código | Clase              | Cantidad de Imágenes |
| ------ | ------------------ | -------------------- |
| 2      | Non Demented       | 2566                 |
| 3      | Very Mild Demented | 1781                 |
| 0      | Mild Demented      | 724                  |
| 1      | Moderate Demented  | 49                   |
---

Esta distribución muestra un claro desbalance de clases, con la categoría 'Non Demented' siendo la más frecuente y 'Moderate Demented' la menos frecuente.


## Resumen de calidad de los datos

*   **Imágenes Corruptas:**
    *   Se decodificaron las imágenes almacenadas como bytes en la columna `image` a arreglos NumPy de 224x224x3 (tres canales).
    *   Se implementó una función `imagen_valida` para verificar que los arreglos de imagen resultantes no fueran nulos y tuvieran datos.
    *   **Resultados:** No se encontraron ni eliminaron imágenes corruptas en `df_train` (5120 de 5120 se mantuvieron) ni en `df_test` (1280 de 1280 se mantuvieron). Esto indica que todas las imágenes en los conjuntos de datos son válidas y decodificables.

*   **Detección de Duplicados:**
    *   Para identificar imágenes duplicadas, se calculó un hash MD5 para cada arreglo de imagen (`img_arr`).
    *   **Resultados:** No se encontraron imágenes duplicadas en `df_train` (0 duplicados) ni en `df_test` (0 duplicados).

*   **Normalización de Imágenes:**
    *   Las imágenes decodificadas y redimensionadas a 224x224x3 (`img_arr`) se normalizaron. El proceso de decodificación inicial escaló los valores de píxeles a un rango de 0-255.
    *   **Proceso:** Se dividió cada valor de píxel por 255.0 para escalar los datos al rango [0, 1].
    *   **Ejemplo de Normalización (`df_train`):**
        *   Antes de normalizar: Valores de píxeles entre 0 y 152.
        *   Después de normalizar: Valores de píxeles entre 0.0 y 0.596078431372549.
    *   **Ejemplo de Normalización (`df_test`):**
        *   Antes de normalizar: Valores de píxeles entre 0 y 250.
        *   Después de normalizar: Valores de píxeles entre 0.0 y 0.9803921568627451.
    *   Esta normalización es un paso estándar y crucial para la preparación de datos de imagen para modelos de Deep Learning, ya que ayuda a la estabilidad y velocidad del entrenamiento del modelo.

## Variable objetivo

La variable objetivo, `label`, representa el estado de demencia del paciente. Se mapea a las siguientes categorías, tal como se definió en el notebook:

*   **0:** Mild Demented
*   **1:** Moderate Demented
*   **2:** Non Demented
*   **3:** Very Mild Demented

La distribución de estas categorías en el conjunto de entrenamiento es la siguiente:
*   `Non Demented` (2): 2566
*   `Very Mild Demented` (3): 1781
*   `Mild Demented` (0): 724
*   `Moderate Demented` (1): 49

Esta distribución es visualmente impactante, mostrando que la mayoría de los casos corresponden a 'Non Demented' o 'Very Mild Demented', mientras que los casos de 'Moderate Demented' son muy escasos. Esta asimetría debe considerarse en el diseño del modelo para evitar sesgos.

## Variables individuales

Se transformó la columna `image` que contenía los bytes de las imágenes en una nueva columna `img_arr` que almacena los arreglos NumPy de las imágenes decodificadas, redimensionadas a 224x224 píxeles y con 3 canales (replicando la imagen en escala de grises para adaptarse a modelos pre-entrenados que esperan 3 canales RGB). Además, estas imágenes fueron normalizadas en el rango [0, 1].

A partir de `img_arr`, se extrajeron dos características adicionales para cada imagen en `df_train`:
*   `mean_pixel`: La media de la intensidad de píxeles de cada imagen.
*   `std_pixel`: La desviación estándar de la intensidad de píxeles de cada imagen.

El análisis se centró en `mean_pixel` como un indicador de las características de la imagen.



## Ranking de variables

A partir de las estadísticas descriptivas calculadas por clase y de las visualizaciones realizadas, tenemos:

| Label | Categoría            | n_imágenes | mean_pixel (media) | std(mean_pixel) |
| :---: | :------------------- | ---------: | -----------------: | --------------: |
| 0     | Mild Demented        |       724  | 0.261911           | 0.020898        |
| 1     | Moderate Demented    |        49  | 0.270272           | 0.019699        |
| 2     | Non Demented         |      2566  | 0.288351           | 0.025964        |
| 3     | Very Mild Demented   |      1781  | 0.271775           | 0.027948        |

Estos valores muestran que `mean_pixel` tiende a ser mayor en la clase **Non Demented** que en el resto de categorías, y que la dispersión de `mean_pixel` (su desviación estándar por grupo) es algo mayor en las clases `Non Demented` y `Very Mild Demented`. 
<br/><br/>Esta evidencia cuantitativa es la base para asignar a `mean_pixel` el primer lugar en el ranking de variables, mientras que `std_pixel` se considera secundaria y complementaria.

Se arma el siguiente ranking de importancia:

1. **`mean_pixel` (media de intensidad de píxel)**  
   - Muestra diferencias claras en sus medias entre las categorías de la variable objetivo (`label`), especialmente entre la clase `Non Demented` y el resto.  
   - Está directamente relacionada con el "brillo" promedio de la imagen, lo que puede reflejar patrones estructurales globales en las MRI.  
   - Es la variable con mayor capacidad observada para capturar variaciones entre clases de demencia en esta etapa exploratoria.

2. **`std_pixel` (desviación estándar de intensidad de píxel)**  
   - Resume el grado de variabilidad/contraste dentro de cada imagen.  
   - Aporta información complementaria a `mean_pixel`, pero sus diferencias entre clases son menos marcadas y muestran un mayor solapamiento en los valores.  
   - Su poder discriminativo parece menor que el de la media, aunque puede ayudar a capturar sutiles diferencias de textura.

## Relación entre variables explicativas y variable objetivo

Se examinó la relación entre la media de píxeles (`mean_pixel`) y la variable objetivo (`label`) utilizando un boxplot y estadísticas descriptivas agrupadas por `label`.

**Estadísticas Descriptivas de `mean_pixel` por `label`:**

| Label | Categoría         | count | mean     | std      | min      | 25%      | 50%      | 75%      | max      |
| :---- | :---------------- | :---- | :------- | :------- | :------- | :------- | :------- | :------- | :------- |
| 0     | Mild Demented     | 724.0 | 0.261911 | 0.020898 | 0.175491 | 0.251599 | 0.266915 | 0.276109 | 0.305354 |
| 1     | Moderate Demented | 49.0  | 0.270272 | 0.019699 | 0.238255 | 0.251057 | 0.270376 | 0.287820 | 0.297590 |
| 2     | Non Demented      | 2566.0| 0.288351 | 0.025964 | 0.168651 | 0.272060 | 0.292569 | 0.307359 | 0.339165 |
| 3     | Very Mild Demented| 1781.0| 0.271775 | 0.027948 | 0.130074 | 0.261202 | 0.276836 | 0.290543 | 0.318842 |

**Observaciones clave del boxplot y las estadísticas:**

*   **Diferencias en la media de píxeles:** Se observa una variación en la media de píxeles entre las diferentes categorías de demencia. La clase 'Non Demented' (label 2) presenta la media de píxeles más alta (aproximadamente 0.288), lo que podría sugerir imágenes con mayor brillo o menor oscuridad en promedio en comparación con otras clases.
*   **Superposición de distribuciones:** A pesar de las diferencias en las medias, las cajas (rangos intercuartílicos) de las diferentes categorías se superponen considerablemente. Esto indica que `mean_pixel` por sí solo puede no ser un predictor fuerte y unívoco del estado de demencia, ya que hay mucha variabilidad dentro de cada clase y similitud entre ellas.
*   **Variabilidad (std):** La desviación estándar (`std_pixel` no se mostró en la tabla pero se calculó) y la `std` de `mean_pixel` por grupo también varían, siendo 'Non Demented' (0.026) y 'Very Mild Demented' (0.0279) las que presentan mayor dispersión en sus medias de píxeles.
*   **Clase 'Moderate Demented' (label 1):** Esta clase tiene un número muy bajo de observaciones (49), lo que hace que sus estadísticas sean menos robustas. Su media de píxeles (0.270) es similar a la de 'Very Mild Demented' (0.272) y 'Mild Demented' (0.262).

En resumen, la media de píxeles proporciona una pequeña indicación de diferencias entre las clases, pero la superposición de sus distribuciones sugiere que características más complejas y de alto nivel extraídas por modelos de Deep Learning serán necesarias para una clasificación precisa.
