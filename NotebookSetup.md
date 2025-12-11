# 🧠 Instalación de TensorFlow + Entorno ML en macOS (M1/M2/M3 o Intel)

**Compatible con Python 3.9 + Jupyter + lectura de Parquet**

---

## ✅ 1. Crear entorno Conda (Python 3.9)

```bash
conda create -n tf39 python=3.9 -y
conda activate tf39
```

---

## ✅ 2. Instalar Jupyter dentro del entorno

```bash
pip install jupyterlab
```

> Esto asegura que Jupyter pueda ejecutar kernels dentro del entorno.

---

## ✅ 3. Instalar dependencias base numéricas

```bash
pip install "numpy>=1.22.4,<1.23" pandas matplotlib seaborn scipy
```

---

## ✅ 4. Instalar scikit-learn

```bash
pip install scikit-learn
```

---

## ✅ 5. Instalar OpenCV

```bash
pip install opencv-python
```

---

## ✅ 6. Instalar TensorFlow para macOS

### 🔹 Procesadores Apple M-series (ARM):

```bash
pip install tensorflow-macos==2.9.0
pip install tensorflow-metal==0.5.0
```

### 🔹 Mac Intel:

```bash
pip install tensorflow==2.9.0
```

> ⚠️ 2.9.0 es la versión más estable compatible con Python 3.9.

---

## ✅ 7. Instalar dependencias complementarias requeridas por tu notebook

```bash
pip install pyarrow     # lectura de archivos .parquet
pip install pillow      # manipulación de imágenes
pip install h5py        # guardado de modelos keras
```

---

## 📌 8. (Opcional) Instalar utilidades para modelos e imágenes

```bash
pip install imageio tqdm
```

---

## 📌 9. Registrar kernel de Jupyter para usar este entorno

```bash
pip install ipykernel
python -m ipykernel install --user --name=tf39 --display-name="TensorFlow Py3.9"
```


# 📦 📌 Listado consolidado de dependencias instaladas

```
python 3.9
jupyterlab
numpy >=1.22.4,<1.23
pandas latest compatible
matplotlib
seaborn
scikit-learn
opencv-python
tensorflow-macos 2.9.0 (M-series)
tensorflow-metal 0.5.0 (M-series)
pyarrow
pillow
h5py
imageio (opcional)
tqdm (opcional)
```

---

---

# 🚀 Verificación del entorno

Abra Jupyter:

```bash
jupyter lab
```

Nuevo notebook → seleccionar kernel `TensorFlow Py3.9`

Ejecutar:

```python
import numpy as np
import pandas as pd
import tensorflow as tf
import cv2

print("NumPy:", np.__version__)
print("Pandas:", pd.__version__)
print("TensorFlow:", tf.__version__)
print("OpenCV:", cv2.__version__)
```

Salida esperada similar:

```
NumPy: 1.22.4
Pandas: 2.x.x
TensorFlow: 2.9.x
OpenCV: 4.x.x
```