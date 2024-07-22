# Usa una imagen base de Python 3.12
FROM python:3.12

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos (requirements.txt) al contenedor
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación al contenedor
COPY . .

# Expone el puerto 8000 (puerto uvicorn)
EXPOSE 8000

# Comando por defecto para ejecutar la aplicación con uvicorn
# CMD ["uvicorn", "plantasid:app"]
CMD ["uvicorn", "plantasid:app", "--host", "0.0.0.0", "--port", "8000"]
