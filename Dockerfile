# ---- Imagen base optimizada con TensorFlow ----
FROM tensorflow/tensorflow:2.12.0

# ---- Crear carpeta de aplicación ----
WORKDIR /app

# ---- Instalar dependencias del sistema ----
RUN apt-get update && apt-get install -y \
    python3-opencv \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ---- Copiar dependencias Python ----
COPY requirements.txt .

# ---- Instalar dependencias Python (FastAPI, Uvicorn, etc.) ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copiar código fuente  ----
COPY src/grupo3/api/main.py .

# ---- Exponer puerto de FastAPI ----
EXPOSE 8000

# ---- Comando de arranque ----
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
