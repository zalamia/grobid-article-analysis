# Imagen base de python
FROM python:3.10-slim

# Directorio de trabajo
WORKDIR /app

# Copiamos tu requirements.txt y lo instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código y los PDFs
COPY main.py .
COPY pdfs/ ./pdfs/

# Ejecutar el script
CMD ["python", "main.py"]