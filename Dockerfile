# ---- Imagen base optimizada con TensorFlow ----
FROM python:3.10-slim

# ---- Crear carpeta de aplicación ----
WORKDIR /app

# ---- Instalar dependencias del sistema ----

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
 && rm -rf /var/lib/apt/lists/*

# ---- Copiar dependencias Python ----
COPY requirements.txt .

# ---- Instalar dependencias Python (FastAPI, Uvicorn, etc.) ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copiar código fuente  ----
COPY src/grupo3/api /app

# ---- Exponer puerto de FastAPI ----
EXPOSE 8080

# ---- Comando de arranque ----
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
