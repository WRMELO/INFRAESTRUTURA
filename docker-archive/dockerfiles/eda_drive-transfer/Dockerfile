# 🔧 Imagem base
FROM python:3.11-slim

# 🌍 Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 🏗️ Diretório de trabalho dentro do container
WORKDIR /workspace

# 🚀 Copia os arquivos locais para o container
COPY . /workspace

# 🛠️ Instala dependências
RUN apt-get update && apt-get install -y \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# 🔥 Comando padrão ao rodar o container
CMD ["python", "main.py"]
