# Informe de salida

## Resumen Ejecutivo

En el sigueinte informe se describe los resultados del proyecto de machine learning para la detección de Alzheimer utilizando imágenes de resonancia magnética (MRI) y presenta los principales logros y lecciones aprendidas durante el proceso.

El proyecto logró desarrollar e implementar un modelo de Deep Learning capaz de clasificar imágenes MRI en cuatro categorías de deterioro cognitivo (Non-Demented, Very Mild Demented, Mild Demented y Moderate Demented) con un accuracy del 97% de exactitud. El modelo fue desplegado en dos arquitecturas diferentes: Azure Container Apps y Azure Functions, demostrando la viabilidad del sistema como herramienta de apoyo al diagnóstico temprano en entornos clínicos.

El proyecto siguió la metodología CRISP-DM, abarcando desde el entendimiento del negocio hasta el despliegue, e incluyó un pipeline completo de preprocesamiento, entrenamiento, evaluación e implementación. 

## Resultados del proyecto

### Entregables y logros alcanzados

El proyecto completó todas las fases del ciclo CRISP-DM, generando los siguientes entregables:

#### 1. Entendimiento del Negocio y Datos
- **Project Charter**: Documentación completa del objetivo, alcance, metodología y stakeholders del proyecto.
- **Análisis Exploratorio de Datos (EDA)**: Identificación de desbalanceo crítico de clases (desde 49 hasta 2566 muestras por clase), análisis de calidad de imágenes, detección de duplicados y caracterización de variables.
- **Data Dictionary y Data Summary**: Documentación de la estructura, distribución y calidad de los datos.

#### 2. Preparación de Datos
- **Pipeline de Preprocesamiento**: Implementación de funciones para decodificación de imágenes desde formato Parquet, normalización, redimensionamiento a 224×224 píxeles y conversión a 3 canales RGB.
- **Balanceo de Clases**: Estrategia de sobremuestreo que equilibró todas las clases a 2566 muestras, superando el desbalance inicial.
- **Data Augmentation**: Implementación de transformaciones controladas (zoom 2%, rotación ±2°, ajuste de brillo 90-110%) para mejorar la generalización sin distorsionar patrones neuroanatómicos.


#### 3. Modelamiento
- **Modelo Baseline**: Arquitectura CNN personalizada de 4 capas convolucionales (32, 64, 128, 256 filtros) con BatchNormalization, MaxPooling, capas Dense y Dropout del 50%.
- **Optimización**: Entrenamiento durante 12 épocas con optimizador Adam (learning rate inicial 1e-4), callbacks de ModelCheckpoint y ReduceLROnPlateau.
- **Notebooks Reproducibles**: Implementación completa en Jupyter Notebooks con documentación y análisis de curvas de aprendizaje.

#### 4. Evaluación
- **Métricas de Rendimiento**: El modelo final alcanzó:
  - **Exactitud global: 97%**
  - **F1-score promedio: 0.97**
  - **F1-scores de 0.94 y 0.95** en clases "Mild" y "Moderate" respectivamente
- **Análisis de Matriz de Confusión**: Identificación de confusión manejable entre clases "Mild" y "Moderate", reflejando la continuidad neuroanatómica entre estas etapas.
- **Validación de Generalización**: Curvas de entrenamiento y validación mostraron convergencia estable sin sobreajuste evidente.

#### 5. Despliegue
- **Arquitectura 1 - Azure Container Apps**: 
  - Backend FastAPI con TensorFlow desplegado en contenedores Docker
  - Frontend React/Vite con interfaz de usuario
  - Integración con Azure Blob Storage para almacenamiento de modelos
  - Documentación completa de despliegue y mantenimiento
  
- **Arquitectura 2 - Azure Functions**:
  - Función serverless con blob trigger para procesamiento automático
  - Sistema de notificaciones por email con resultados de predicción
  - Optimización para procesamiento bajo demanda
  - Documentación de configuración y uso

### Evaluación del modelo final vs. modelo base

- El sobremuestreo permitió que el modelo aprendiera representaciones robustas de todas las clases, especialmente la clase minoritaria "Moderate Demented" (de 49 a 2566 muestras).
- Las transformaciones mejoraron la capacidad de generalización sin distorsionar características neuroanatómicas críticas.
- Ajuste fino de learning rate, callbacks y regularización resultó en convergencia estable y mejor rendimiento.

### Relevancia para el negocio

Los resultados del proyecto tienen relevancia significativa para el sector de la salud:

1. Apoyo al Diagnóstico Temprano, el modelo puede identificar casos de deterioro cognitivo, lo cual es crucial para intervenciones tempranas.

2. Escalabilidad: Las dos arquitecturas de despliegue (Container Apps y Functions) permiten escalar el sistema según la demanda, desde procesamiento bajo demanda hasta alto volumen de casos.

4. El modelo está diseñado como herramienta de apoyo, no como reemplazo del diagnóstico clínico, lo cual es fundamental para su aceptación en entornos médicos.

## Lecciones aprendidas

### Principales desafíos y obstáculos

1. Desbalanceo Extremo de Clases: El dataset presentaba una distribución muy desbalanceada (Non Demented: 2566, Very Mild: 1781, Mild: 724, Moderate: 49). Este desbalance inicial representó un desafío significativo que requirió estrategias de balanceo cuidadosas para evitar sesgos hacia las clases mayoritarias.

2. Complejidad del Despliegue: La implementación de dos arquitecturas diferentes (Container Apps y Functions) requirió aprendizaje de múltiples servicios de Azure y adaptación del código para diferentes entornos de ejecución.

4. Tamaño del Modelo: El modelo final tiene un tamaño de aproximadamente 152MB, lo cual presentó desafíos en el despliegue de Azure Functions, requiriendo estrategias de carga diferida (lazy loading) y optimización de memoria.

5. Procesamiento de Imágenes Médicas: El preprocesamiento de imágenes MRI requiere cuidado especial para preservar características neuroanatómicas críticas mientras se aplican transformaciones necesarias para el modelo.

### Lecciones aprendidas

#### Manejo de Datos
- El análisis exploratorio detallado permitió identificar problemas críticos (desbalanceo, calidad de imágenes) antes del modelamiento, ahorrando tiempo y recursos.
- El sobremuestreo resultó más efectivo que técnicas de submuestreo para este caso, permitiendo mantener la diversidad de datos mientras se equilibraban las clases.
- La implementación de funciones de validación de imágenes (detección de corruptas, duplicados) fue fundamental para garantizar la integridad del pipeline.

#### Modelamiento

- La CNN de 4 capas demostró que arquitecturas relativamente simples, pueden alcanzar óptimo rendimientos.
- La combinación de BatchNormalization, Dropout y data augmentation controlado permitió entrenar un modelo robusto, a pesar de la complejidad de las imágenes médicas.
- El uso de F1-score junto con accuracy permitió identificar problemas específicos por clase (confusión entre Mild y Moderate) que no eran evidentes solo con la exactitud global.

#### Implementación y Despliegue
- La containerización desde el inicio facilitó el despliegue y la reproducibilidad entre entornos.
- La arquitectura separada entre frontend y backend permitió escalar y mantener cada componente independientemente.
- Implementar dos arquitecturas diferentes (Container Apps y Functions) proporcionó flexibilidad para diferentes casos de uso y requisitos de escalabilidad.
- La estrategia de almacenar modelos en Blob Storage y cargarlos bajo demanda fue esencial para el despliegue en entornos con limitaciones de tamaño.

### Recomendaciones para futuros proyectos de machine learning

1. Estimar con precisión los requisitos de almacenamiento y cómputo desde el inicio, considerando alternativas locales cuando los recursos cloud son limitados.

2. Dedicar tiempo suficiente al análisis exploratorio de datos antes de cualquier modelamiento, ya que los insights obtenidos guían todas las decisiones posteriores.

3. Comenzar con arquitecturas simples y agregar complejidad solo cuando sea necesario, en lugar de comenzar con modelos complejos que pueden ser difíciles de optimizar.

4. Mantener documentación actualizada en cada fase del proyecto facilita la reproducibilidad y el mantenimiento futuro.

5. En proyectos de salud, siempre diseñar modelos como herramientas de apoyo, nunca como reemplazo del juicio profesional, y documentar claramente las limitaciones.

## Impacto del proyecto

### Impacto en el negocio y la industria

El proyecto tiene el potencial de generar impacto significativo en el sector de la salud, particularmente en el área de neurología y diagnóstico por imágenes:

1. El modelo puede identificar casos de "Very Mild Demented" con buena precisión, lo cual es crítico para la detección temprana de Alzheimer. 

2. Al proporcionar una evaluación objetiva y rápida de imágenes MRI, el sistema puede ayudar a reducir el tiempo de análisis por parte de los especialistas.

3. Las arquitecturas de despliegue implementadas permiten que el sistema sea accesible desde diferentes ubicaciones, facilitando su uso en áreas con menor acceso a especialistas en neuroimagen.


### Áreas de mejora y oportunidades de desarrollo futuras

1. Implementar modelos preentrenados (ResNet, EfficientNet, Vision Transformer) podría capturar características más ricas y generalizables, potencialmente mejorando el rendimiento, especialmente en la distinción entre "Mild" y "Moderate".

2. Migrar de cortes individuales a volúmenes cerebrales completos (3D CNNs) permitiría capturar información espacial tridimensional valiosa para evaluar atrofia y cambios estructurales más complejos.

3. Desarrollar un modelo binario inicial que distinga "Deterioro Cognitivo" vs. "Normal", seguido de modelos especializados para refinar la clasificación dentro de cada grupo, podría mejorar la precisión en etapas intermedias.

4. Implementar arquitecturas con atención (SE-Net, CBAM) para focalizar regiones anatómicas relevantes podría mejorar la interpretabilidad y el rendimiento.

5. Incorporar capas interpretables (Grad-CAM integrado) para visualizar qué regiones del cerebro influyen en las predicciones, facilitando la validación clínica y la aceptación del modelo.

6. Realizar validación del modelo con datasets de diferentes instituciones y poblaciones para evaluar la generalización real del modelo.

## Conclusiones

### Resumen de resultados y principales logros

El proyecto de detección de Alzheimer mediante imágenes MRI fue completado favorablemente, superando los objetivos iniciales establecidos. Los principales logros incluyen:

1. El modelo alcanzó un 97% de exactitud y un **F1-score promedio de 0.97**, superando el objetivo inicial de 85-90% de precisión.

2. Se desarrolló un pipeline completo desde la adquisición de datos hasta el despliegue, siguiendo la metodología CRISP-DM.

3. La estrategia de balanceo de datos mediante sobremuestreo permitió superar el desbalance extremo inicial (desde 49 hasta 2566 muestras por clase), logrando que el modelo aprendiera representaciones robustas de todas las clases.

4. Se implementaron y documentaron dos arquitecturas de despliegue diferentes (Azure Container Apps y Azure Functions), demostrando flexibilidad y adaptabilidad a diferentes requisitos operacionales.

### Conclusiones finales

El modelo desarrollado tiene el potencial de servir como herramienta de apoyo valiosa en entornos clínicos, complementando (no reemplazando) el juicio profesional de neurólogos y radiólogos. La precisión alcanzada, especialmente en la detección de casos tempranos, es clínicamente relevante y puede contribuir significativamente a la detección temprana del Alzheimer.

### Recomendaciones para futuros proyectos

1. Invertir tiempo significativo en el análisis exploratorio y la preparación de datos, ya que esto tiene el mayor impacto en el rendimiento final del modelo.

2. Comenzar con arquitecturas simples y agregar complejidad solo cuando sea necesario y justificado por mejoras medibles en el rendimiento.

3. Mantener documentación actualizada y completa en cada fase facilita la reproducibilidad, el mantenimiento y la transferencia de conocimiento.

4. En proyectos de salud, siempre diseñar sistemas como herramientas de apoyo, documentar limitaciones claramente, y trabajar en colaboración con profesionales médicos para validación clínica.

## Agradecimientos

El desarrollo y éxito de este proyecto fue el resultado del trabajo colaborativo y la dedicación de todo el equipo. Cada miembro aportó conocimientos y habilidades que fueron esenciales para superar los desafíos encontrados y alcanzar los objetivos establecidos.

Agradecemos a la Universidad Nacional de Colombia, a los profesores Jorge Camargo, Felipe Restrepo, Fabio Gonzalez, Oscar Perdomo y Juan Malagón junto con al "Programa de Formación en Machine Learning y Data Science" por proporcionar las herramientas necesarias para el desarrollo de este proyecto.
