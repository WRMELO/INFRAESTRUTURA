# Dockerfile base para gpu-utils
# --- gpu-utils Dockerfile ---
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 1) Instalar Python e pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# 2) Definir diretório de trabalho
WORKDIR /app

# 3) Copiar e instalar dependências
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 4) Copiar utilitários/​scripts para /app
COPY . .

# 5) Comando padrão: executa script de info GPU
CMD ["python3", "main.py"]

