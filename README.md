# Team Data Science Project Template

Esta plantilla es una implementación de la plantilla de proyecto de Team Data Science Process que actualmente se utiliza en el "Programa de Formación en Machine Learning y Data Science" en la Universidad Nacional de Colombia.

Esta plantilla proporciona las siguientes carpetas y archivos:

* `src`: acá debe ir el código o implementación del proyecto en Python.
* `docs`: en esta carpeta se encuentran las plantillas de los documentos definidos en la metodología.
* `scripts`: esta carpeta debe contener los scripts/notebooks que se ejecutarán.
* `pyproject.toml`: archivo de definición del proyecto en Python.

# Instalar Python y crear entorno virtual 
```python
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

# Instalar dependencias
```
pip install -r requirements.txt
```

# Instalar Docker Desktop
```
- Ir a https://www.docker.com/products/docker-desktop/
- Descargar la versión para tu sistema operativo.
- Instalar siguiendo el asistente.
- Abrir Docker Desktop y verificar que esté corriendo (el ícono debe estar activo).
```

# Ejecutar MinIO en Docker

```bash
docker run -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD=password123 \
  --name minio \
  quay.io/minio/minio server /data --console-address ":9001"
```

## Esto levanta:

- API S3-compatible en: http://localhost:9000
- GUI de MinIO (MinIO Console) en: http://localhost:9001

## Credenciales:

- Usuario: admin
- Password: password123

