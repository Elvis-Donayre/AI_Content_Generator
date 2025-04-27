FROM tiangolo/uvicorn-gunicorn:python3.9

# Instalar dependencias del sistema para Chrome/Chromium y otros requisitos
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    chromium \
    chromium-driver

# Crear y establecer el directorio de trabajo
WORKDIR /backend

# Copiar los archivos de dependencias
COPY requirements.txt ./

# Instalar dependencias y actualizar pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

# Establecer variable de entorno para usar Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copiar el código fuente
COPY . .

# Exponer el puerto de FastAPI
EXPOSE 8004

# Definir el punto de entrada
ENTRYPOINT ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8004"]