# Reporte del Modelo Baseline

Este documento contiene los resultados del modelo baseline.

## Descripción del modelo

El modelo baseline es una arquitectura de red neuronal convolucional (CNN) desarrollada en TensorFlow/Keras para la clasificación de imágenes de resonancia magnética (MRI) en 4 categorías relacionadas con el Alzheimer:

0: Mild Demented
1: Moderate Demented
2: Non Demented
3: Very Mild Demented

Se trata de un modelo secuencial simple diseñado para establecer una línea base de rendimiento antes de aplicar técnicas de optimización o modelos preentrenados.

## Diseño del modelo

```
ENTRADA (224×224×3)
       ↓
┌─────────────────────┐
│  Conv2D-32 (3×3)    │ ← 32 filtros, padding='same'
│  activación: ReLU   │
└─────────────────────┘
       ↓
┌─────────────────────┐
│ BatchNormalization  │ ← Normalización por lote (128 params)
└─────────────────────┘
       ↓
┌─────────────────────┐
│  MaxPooling2D (2×2) │ ← Reducción espacial 50%
└─────────────────────┘
       ↓ (112×112×32)
┌─────────────────────┐
│  Conv2D-64 (3×3)    │ ← 64 filtros, padding='same'
│  activación: ReLU   │
└─────────────────────┘
       ↓
┌─────────────────────┐
│ BatchNormalization  │ ← Normalización por lote (256 params)
└─────────────────────┘
       ↓
┌─────────────────────┐
│  MaxPooling2D (2×2) │ ← Reducción espacial 50%
└─────────────────────┘
       ↓ (56×56×64)
┌─────────────────────┐
│ Conv2D-128 (3×3)    │ ← 128 filtros, padding='same'
│  activación: ReLU   │
└─────────────────────┘
       ↓
┌─────────────────────┐
│ BatchNormalization  │ ← Normalización por lote (512 params)
└─────────────────────┘
       ↓
┌─────────────────────┐
│  MaxPooling2D (2×2) │ ← Reducción espacial 50%
└─────────────────────┘
       ↓ (28×28×128)
┌─────────────────────┐
│ Conv2D-256 (3×3)    │ ← 256 filtros, padding='same'
│  activación: ReLU   │
└─────────────────────┘
       ↓
┌─────────────────────┐
│ BatchNormalization  │ ← Normalización por lote (1024 params)
└─────────────────────┘
       ↓
┌─────────────────────┐
│  MaxPooling2D (2×2) │ ← Reducción espacial 50%
└─────────────────────┘
       ↓ (14×14×256)
┌─────────────────────┐
│     Flatten()       │ ← Vectorización: 14×14×256 = 50,176
└─────────────────────┘
       ↓ (50,176)
┌─────────────────────┐
│    Dense-256        │ ← Capa totalmente conectada
│  activación: ReLU   │ (12,845,312 parámetros)
└─────────────────────┘
       ↓
┌─────────────────────┐
│    Dropout(0.5)     │ ← Regularización: 50% neuronas desactivadas
└─────────────────────┘
       ↓
┌─────────────────────┐
│    Dense-4          │ ← Capa de salida
│ activación: softmax │ (1,028 parámetros)
└─────────────────────┘
       ↓
SALIDA (4 probabilidades)
[NonD, VeryMild, Mild, Moderate]
```

## Variables de entrada

Formato de entrada: Imágenes de MRI decodificadas y redimensionadas a 224x224 píxeles con 3 canales (RGB)

**Volumen de datos:**

- Entrenamiento: 5120 muestras
- Prueba: 1280 muestras

**Preprocesamiento:**

1. Decodificación desde bytes en formato JPEG
2. Conversión a escala de grises y expansión a 3 canales
3. Redimensionamiento
3. Normalización

## Variable objetivo

Nombre: ```label```
Tipo: Categórica

## Evaluación del modelo

### Métricas de evaluación

El rendimiento del modelo se evaluó utilizando métricas ampliamente reconocidas en problemas de clasificación multiclase: precisión (precision), exhaustividad (recall) y puntuación F1 (F1-score), complementadas con la exactitud global (accuracy). 
La precisión mide la proporción de predicciones positivas correctas en cada clase, indicando la confiabilidad del modelo al clasificar un caso en una categoría específica. 
La exhaustividad, por su parte, evalúa la capacidad del modelo para identificar correctamente todos los casos reales de cada clase, reflejando su sensibilidad. 
La puntuación F1 combina ambas métricas en un solo valor armónico, siendo especialmente útil cuando se busca un equilibrio entre precisión y exhaustividad. 
Además, se incluyeron el promedio macro y el promedio ponderado de estas métricas para ofrecer una visión global del desempeño del modelo considerando todas las clases de manera equitativa y según su distribución respectiva. 
Estas métricas se calcularon sobre una matriz de confusión, que permitió visualizar los aciertos y errores por clase, facilitando la identificación de patrones de confusión, como se observó entre las categorías "Mild" y "Moderate".

### Resultados de evaluación

| Clase          | Precisión | recall | F1-Score | support |
|----------------|-----------|--------|----------|---------|
| Non Demented   | 1.00      | 1.00   | 1.00     | 321     |
| Very Mild      | 1.00      | 1.00   | 1.00     | 320     |
| Mild           | 0.99      | 0.90   | 0.94     | 321     |
| Moderate       | 0.91      | 0.98   | 0.95     | 321     |
| **Exactitud**  |           |        | **0.97** | 1283    |
| **Macro Avg**  | 0.97      | 0.97   | 0.97     | 1283    |
| **Weighted Avg**| 0.97     | 0.97   | 0.97     | 1283    |

## Análisis de los resultados

Los resultados obtenidos reflejan un rendimiento general sólido, alcanzando una precisión global del 97% en el conjunto de prueba. Es destacable la excelente capacidad de clasificación para las categorías "Non Demented" y "Very Mild", donde tanto la precisión como la exhaustividad alcanzan valores del 100%, lo que indica una identificación perfecta en estas clases. 
Para las clases "Mild" y "Moderate" se observan resultados ligeramente inferiores, aunque todavía elevados, con puntuaciones F1 de 0.94 y 0.95 respectivamente, mostrando una alta fiabilidad en la distinción de estas etapas más avanzadas. En general, el modelo demuestra un equilibrio adecuado entre precisión y exhaustividad en todas las categorías, confirmando su robustez para la clasificación de diferentes grados de demencia.

**Fortalezas del modelo**

- Clasificación perfecta en etapas iniciales: El modelo logra precisión perfecta en las clases “Non Demented” y “Very Mild”, lo que refleja una capacidad excepcional para identificar correctamente casos sin demencia y con deterioro cognitivo muy leve, minimizando falsos positivos y falsos negativos en estas categorías clave.
- Estabilidad en el entrenamiento: Las curvas de pérdida y exactitud muestran una convergencia estable entre los conjuntos de entrenamiento y validación a partir de la época 11, sin signos evidentes de sobreajuste en las etapas observadas. Esto sugiere una buena generalización y un buen proceso de aprendizaje.
- Balance métrico consistente: Todas las clases mantienen puntuaciones F1 superiores a 0.94, lo que indica un buena relación incluso en las categorías más desafiantes.

**Debilidades y áreas de mejora**

- Confusión entre clases contiguas: Se observa una ligera disminución en el rendimiento en las clases “Mild” y “Moderate”, con una precisión de 0.99 y 0.91, y exhaustividad de 0.90 y 0.98, respectivamente. La matriz de confusión revela cierta confusión bidireccional entre estas dos categorías, lo que sugiere que los rasgos visuales o clínicos entre estas etapas pueden ser más sutiles y difíciles de distinguir para el modelo.
- Limitación en la identificación de casos límite: Aunque el accuracy global es alto, el F1-score de 0.94 en “Mild” apunta a una dificultad relativa en la clasificación de casos en etapas intermedias, donde la diferenciación visual o patológica puede ser menos evidente.

## Conclusiones

El modelo baseline demuestra un desempeño alto y generalizable, particularmente fuerte en la identificación de extremos del espectro (no dementes y deterioro muy leve). 
Su principal área de mejora radica en afinar la discriminación entre las etapas “Mild” y “Moderate”. 

## Referencias

Islam J, Zhang Y. Brain MRI analysis for Alzheimer's disease diagnosis using an ensemble system of deep convolutional neural networks. Brain Inform. 2018 May 31;5(2):2. doi: 10.1186/s40708-018-0080-3. PMID: 29881892; PMCID: PMC6170939.

Zhou, J., Wei, Y., Li, X. et al. A deep learning model for early diagnosis of alzheimer’s disease combined with 3D CNN and video Swin transformer. Sci Rep 15, 23311 (2025). https://doi.org/10.1038/s41598-025-05568-y