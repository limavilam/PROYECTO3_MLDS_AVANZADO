# Project Charter - Entendimiento del Negocio

## Nombre del Proyecto

Modelo de Machine Learning para la detección de Alzheimer utilizando imágenes MRI

## Objetivo del Proyecto

Desarrollar e implementar un modelo de Deep Learning capaz de clasificar imágenes de resonancia magnética (MRI) cerebral
en cuatro categorías correspondientes a los distintos niveles de progresión del Alzheimer (Non-Demented, Very Mild Demented, Mild Demented y Moderate Demented), 
a través de un pipeline que incluya preprocesamiento, técnicas de balanceo de clases, estrategias de aumento de datos y optimización de hiperparámetros, 
con el fin de construir un sistema de apoyo al diagnóstico temprano que maximice la precisión, sensibilidad y capacidad de generalización del modelo sobre datos no vistos.

## Alcance del Proyecto

### Incluye:

- El proyecto utilizará un dataset público de imágenes de resonancia magnética del cerebro, este se encuentra estructurado en cuatro clases asociadas al 
nivel de progresión de la enfermedad (Non-Demented, Very Mild Demented, Mild Demented y Moderate Demented). Este dataset fue obtenido desde Kaggle (https://www.kaggle.com/datasets/borhanitrash/alzheimer-mri-disease-classification-dataset/data) y se encuentra almacenado en archivos parquet los cuales contienen
6400 imágenes codificadas. 
- Se espera desarrollar un modelo de Deep Learning capaz de clasificar imágenes MRI en las cuatro categorías de Alzheimer con altos niveles de precisión, junto con un
pipeline que abarque el preprocesamiento, entrenamiento, validación, evaluación y despliegue. 
- El éxito del proyecto se evaluará mediante la solidez del modelo y la calidad del proceso. En términos de desempeño, se considerará exitoso si el modelo alcanza métricas como una precisión global superior a un umbral predefinido (idealmente entre 85–90%) y mantiene un F1-score adecuado, 
especialmente en las clases minoritarias, demostrando así un comportamiento robusto y consistente. En términos metodológicos, el pipeline deberá ser completamente reproducible, incorporando análisis, curvas de aprendizaje y matriz de confusión. 
Asimismo, el desarrollo debe seguir las fases de la metodología CRISP-DM y culminar con una propuesta de despliegue o un prototipo funcional como resultado final 

### Excluye:

- Recomendaciones médicas o clínicas, análisis neurológicos de partes del cerebro. 

## Metodología

El proyecto se desarrollará siguiendo la metodología CRISP-DM, las fases a implementar serán:

- Entendimiento del negocio: se definió el problema como un modelo de clasificación para apoyar la detección temprana de Alzheimer a través de imágenes MRI. Se establecieron objetivos y criterios de éxito.
- Entendimiento de los datos: Se realizará una exploración del dataset, análisis de distribución por clases, calidad de imágenes, formatos, tamaño y necesidades de preprocesamiento. Se identificarán potenciales problemas como desbalanceo de clases.
- Preparación de los Datos: Se desarrollará el pipeline completo de preprocesamiento, normalización de imágenes, redimensionamiento, división estratificada en entrenamiento/validación/test, data augmentation, etiquetado y balanceo.
- Modelamiento: Se entrenará un modelo de Deep Learning (redes convolucionales o transfer learning), se ajustarán hiperparámetros para optimizar el rendimiento.
- Evaluación: Se validará el modelo con métricas como accuracy, precisión, recall, F1-score y matriz de confusión. Se evaluará la capacidad del modelo para generalizar y se comparará contra los criterios de éxito definidos.
- Despliegue: Para los fines del módulo, esta fase incluirá la documentación del pipeline, entrega del código, reporte y el despliegue.

## Cronograma

| Etapa | Duración Estimada | Fechas                                 |
|------|------------------|----------------------------------------|
| Entendimiento del negocio y carga de datos | 1 semana         | del 18 de noviembre al 21 de noviembre |
| Preprocesamiento, análisis exploratorio | 1 semana         | del 24 de noviembre al 28 de noviembre |
| Modelamiento y extracción de características | 1 semana         | del 1 de diciembre al 5 de diciembre   |
| Despliegue | 1 semana         | del 9 de diciembre al 12 de diciembre  |
| Evaluación y entrega final | 1 semana         | del 15 de diciembre al 19 de diciembre |


## Equipo del Proyecto

| Nombre | Cargo 
|------|------------------
| Iván Quevedo | Científico de datos
| Lina Ávila   | Líder técnico - científica de datos 
| Raúl Ramírez | Ingeniero de ML/MLOPS 

## Presupuesto

| Categoría de Gasto            | Descripción                                                     | Costo Estimado (COP) | Notas / Consideraciones                              |
|-------------------------------|-----------------------------------------------------------------|----------------------|------------------------------------------------------|
| **I. Personal**               |                                                                 |                      |                                                      |
| Científico de Datos Senior    | Diseño del modelo, preprocesamiento, optimización               | $22.810.000          | 1.5 meses a tiempo parcial                           |
| Ingeniero de ML / MLOps       | Implementación, experimentos, pipeline de despliegue            | $15.932.000          | 1.5 meses a tiempo completo                          |
| **II. Infraestructura y Software** |                                                                 |                      |                                                      |
| Plataforma Cloud (GPU)        | Uso de instancias GPU en Azure o AWS                            | $7.720.000           | Aproximadamente 220 horas GPU                        |
| Almacenamiento Cloud          | Almacenamiento en S3 / Blob Storage para imágenes y checkpoints | $308.000             | ~500-700 GB por 2 meses                              |
| Servicios de Despliegue       | Endpoint para inferencia, autoscaling ligero                    | $2.316.000           | Uso de servicios como Azure ML o SageMaker           |
| Licencias y Herramientas      | Librerías, control de versiones, IDE                            | $0                   | Se usarán herramientas open-source                   |
| **III. Implementación y Operación** |                                                                 |                      |                                                      |
| Monitoreo y Logging           | Uso de CloudWatch o Azure Monitor                               | $579.000             | Métricas + alarmas básicas                           |
| **IV. Misceláneos**            |                                                                 |                      |                                                      |
| Investigación y Desarrollo    | Lectura de artículos, pruebas de concepto                       | $2.702.000           | Tiempo dedicado a experimentación                    |
| Gestión de Proyecto           | Coordinación, reuniones, documentación                          | $1.351.000           | Proporción del tiempo del equipo                     |
| Contingencias (10%)           | Fondo para imprevistos                                          | $5.110.000           | Aproximadamente 10 % del total                       |
| **TOTAL ESTIMADO DEL PROYECTO** |                                                                 | **$58.828.000 COP**  |                                                      |


## Stakeholders

- Los principales stakeholders de este proyecto corresponden a profesionales del ámbito clínico y técnico que podrían beneficiarse directamente del uso de un sistema de clasificación automática de imágenes MRI para apoyar el diagnóstico temprano de Alzheimer. 
Entre ellos se encuentran los neurólogos, responsables del manejo integral de pacientes con deterioro cognitivo; los médicos radiólogos, especialistas en la interpretación de imágenes diagnósticas; y los ingenieros biomédicos o personal de tecnología en salud, quienes analizan la viabilidad de integrar herramientas de inteligencia artificial en sistemas clínicos.
También se consideran como stakeholders a investigadores que estudian Alzheimer.
- La relación con los stakeholders se fundamenta en la necesidad de articular el desarrollo técnico del modelo con los requerimientos reales del contexto clínico. Los neurólogos ofrecen la perspectiva médica necesaria para comprender las diferentes etapas del Alzheimer
y la relevancia de una herramienta que facilite la identificación temprana de la enfermedad. Los radiólogos, por su parte, aportan criterios para validar visualmente las predicciones del modelo y compararlas con patrones radiológicos reconocidos. Los ingenieros biomédicos evalúan la posibilidad de integrar este tipo de soluciones a los sitemas del hospital, 
finalmente, los investigadores estudian la enfermedad con el propósito de encontrar técnicas que hagan una detección temprana, entiendan en mayor profundidad la enfermedad y puedan dar posibles soluciones.
- Los stakeholders esperan que el proyecto genere un modelo de clasificación confiable, capaz de ofrecer un apoyo complementario al diagnóstico clínico sin sustituir la experticia profesional.

## Aprobaciones

- Iván Quevedo
- Raúl Ramírez
- Lina Ávila
