# Usar una imagen oficial de Python como base
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requerimientos
COPY requirements.txt ./

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la app
COPY . .

# Exponer el puerto en el que corre Django
EXPOSE 8000

# Comando para correr la app (usando gunicorn para producción)
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"] 