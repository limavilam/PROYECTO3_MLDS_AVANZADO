# Reporte del Modelo Final

## Resumen Ejecutivo

El modelo final desarrollado para la clasificación de grados de demencia a partir de imágenes de resonancia magnética (MRI) alcanzó un rendimiento general del 97% de exactitud en el conjunto de prueba, con una puntuación F1 promedio de 0.97 en todas las clases. 
El modelo demostró una capacidad excepcional para identificar casos de "Non Demented" y "Very Mild" con precisión y recall del 100%, mientras que en las etapas "Mild" y "Moderate" mantuvo puntuaciones F1 de 0.94 y 0.95, respectivamente. Estos resultados indican que el modelo es altamente confiable para la clasificación de deterioro cognitivo, con un buen equilibrio entre sensibilidad y especificidad, lo que lo posiciona como una herramienta prometedora para apoyo diagnóstico en entornos clínicos asistidos por inteligencia artificial.

## Descripción del Problema

El diagnóstico temprano y preciso de la enfermedad de Alzheimer y otros tipos de demencia representa un desafío clínico significativo debido a la superposición sintomática entre etapas y la dependencia de evaluaciones subjetivas. Este proyecto se desarrolló en el contexto de imágenes diagnosticas, con el objetivo de diseñar un modelo de clasificación automática que pueda distinguir entre cuatro categorías clínicas: Non Demented, Very Mild, Mild y Moderate, utilizando volúmenes de MRI cerebrales. La justificación del modelo radica en la necesidad de herramientas objetivas, escalables y reproducibles que complementen el juicio clínico, reduzcan la variabilidad interobservador y faciliten la identificación temprana de patrones neurodegenerativos.

## Descripción del Modelo

El modelo final implementado es una arquitectura de red neuronal convolucional (CNN) personalizada en 2D, diseñada específicamente para procesar imágenes de resonancia magnética cerebral en formato de cortes axiales con dimensiones de 224×224 píxeles y 3 canales de color (RGB). Dado el desbalance inicial en el dataset (con distribuciones de 2566, 1781, 724 y 49 muestras por clase), se aplicó un balanceo de datos mediante sobremuestreo, resultando en 2566 muestras por cada una de las cuatro categorías: Non Demented (0), Very Mild (1), Mild (2) y Moderate (3).

La arquitectura CNN sigue un diseño clásico y progresivo de extracción de características:

1. Cuatro bloques convolucionales con filtros crecientes (32, 64, 128, 256), cada uno con:

- Capa Conv2D (3×3) con activación ReLU y padding 'same'
- BatchNormalization para estabilizar el entrenamiento
- MaxPooling2D (2×2) para reducción espacial

2. Capas totalmente conectadas:

- Aplanado de características (Flatten)
- Capa Dense de 256 unidades con ReLU
- Dropout del 50% para regularización
- Capa de salida Softmax con 4 unidades (clases)

**Preprocesamiento y aumento de datos:**

Las imágenes fueron normalizadas mediante la función ```preprocess_input```. Para el conjunto de entrenamiento se aplicaron transformaciones de aumento de datos controladas: zoom (2%), rotación (±2°), y ajuste de brillo (90-110%), con el objetivo de mejorar la generalización sin distorsionar los patrones neuroanatómicos.

**Entrenamiento:**

El modelo fue compilado con el optimizador Adam (tasa de aprendizaje inicial 1e-4), función de pérdida sparse categorical crossentropy, y métrica de exactitud. Se implementaron dos callbacks clave:

- ModelCheckpoint: para guardar los pesos del mejor modelo basado en la pérdida de validación
- ReduceLROnPlateau: que reduce la tasa de aprendizaje en un 50% tras 3 épocas sin mejora en la pérdida de validación

El entrenamiento se realizó durante 12 épocas, alcanzando el mejor rendimiento en la época 11, donde se observó convergencia estable entre las curvas de entrenamiento y validación, con una precisión final del 97% en el conjunto de prueba.

**Implementación:**

Desarrollado en TensorFlow/Keras, el modelo fue entrenado utilizando ```ImageDataGenerator``` para manejo eficiente de batches, con aceleración por GPU para optimizar el proceso computacional.

## Evaluación del Modelo

La evaluación se realizó utilizando métricas estándar de clasificación multiclase, obteniendo los siguientes resultados:


| Clase          | Precisión | recall | F1-Score | support |
|----------------|-----------|--------|----------|---------|
| Non Demented   | 1.00      | 1.00   | 1.00     | 321     |
| Very Mild      | 1.00      | 1.00   | 1.00     | 320     |
| Mild           | 0.99      | 0.90   | 0.94     | 321     |
| Moderate       | 0.91      | 0.98   | 0.95     | 321     |
| **Exactitud**  |           |        | **0.97** | 1283    |
| **Macro Avg**  | 0.97      | 0.97   | 0.97     | 1283    |
| **Weighted Avg**| 0.97     | 0.97   | 0.97     | 1283    |

El modelo muestra un rendimiento casi perfecto en las clases extremas, lo que sugiere una alta capacidad para distinguir entre cerebros sanos y aquellos con deterioro avanzado. La ligera confusión entre "Mild" y "Moderate" (evidenciada en la matriz de confusión) refleja la continuidad neuroanatómica entre estas etapas. El recall en "Moderate" (0.98) indica una sensibilidad clínicamente valiosa para no pasar por alto casos avanzados. La estabilidad durante el entrenamiento valida la robustez del modelo y su capacidad de generalización.

## Conclusiones y Recomendaciones

1. El modelo CNN personalizado de 4 capas convolucionales logró un rendimiento excepcional (97% de exactitud) en la clasificación de cuatro etapas de deterioro cognitivo, demostrando que arquitecturas relativamente simples pero bien diseñadas pueden ser altamente efectivas para tareas de neuroimagen cuando se combinan con técnicas adecuadas de preprocesamiento y regularización.
2. La estrategia de balanceo de datos (sobremuestreo a 2566 muestras por clase) resultó fundamental para superar el desbalance inicial extremo (desde 49 hasta 2566 muestras), permitiendo al modelo aprender representaciones robustas de todas las clases sin sesgo hacia las mayoritarias.
3. El modelo mostró fortalezas diferenciadas por clase: mientras que alcanzó clasificación perfecta (100%) en las categorías "Non Demented" y "Very Mild", presentó una confusión manejable pero significativa entre "Mild" y "Moderate" (F1-scores de 0.94 y 0.95), lo que refleja la continuidad sintomática y neuroanatómica entre estas etapas clínicas.
4. Las técnicas de regularización integrada (BatchNormalization, Dropout del 50%, aumento de datos controlado) permitieron un entrenamiento estable sin sobreajuste evidente, a pesar de la complejidad inherente a las imágenes médicas.


**Limitaciones Identificadas:**

Si bien el modelo personalizado funciona bien, arquitecturas preentrenadas mediante Transfer Learning podrían capturar características más ricas y generalizables.
La distinción entre "Mild" y "Moderate" podría beneficiarse de un enfoque jerárquico que primero clasifique entre "Deterioro Leve" vs. "Deterioro Moderado-Avanzado", y luego refine dentro de cada grupo.
Al procesar cortes individuales en lugar de volúmenes completos, el modelo pierde información espacial tridimensional valiosa para evaluar atrofia y cambios estructurales.

**Recomendaciones para Iteraciones Futuras:**

1. Implementación de Transfer Learning
2. Enfoque binario inicial donde se desarrolle un modelo para distinguir "Deterioro Cognitivo" vs. "Normal"
3. Combinar "Mild" y "Moderate" en una categoría "Deterioro Establecido"
4. Migración a arquitecturas 3D para procesar volúmenes cerebrales completos
Implementación de mecanismos de atención (SE-Net, CBAM) para focalizar regiones anatómicas relevantes
Incorporación de capas interpretables (Grad-CAM integrado) para validación clínica y trazabilidad

**Escenarios de aplicación**:

El modelo debe siempre funcionar como herramienta de apoyo y nunca como diagnóstico autónomo

## Referencias

Islam J, Zhang Y. Brain MRI analysis for Alzheimer's disease diagnosis using an ensemble system of deep convolutional neural networks. Brain Inform. 2018 May 31;5(2):2. doi: 10.1186/s40708-018-0080-3. PMID: 29881892; PMCID: PMC6170939.

Zhou, J., Wei, Y., Li, X. et al. A deep learning model for early diagnosis of alzheimer’s disease combined with 3D CNN and video Swin transformer. Sci Rep 15, 23311 (2025). https://doi.org/10.1038/s41598-025-05568-y