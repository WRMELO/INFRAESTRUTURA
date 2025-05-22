# 🔧 Imagem base oficial do Python
FROM python:3.11-slim

# 🌍 Variáveis de ambiente (opcional, segurança mínima)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 🏗️ Diretório de trabalho dentro do container
WORKDIR /workspace

# 🚀 Copia tudo da pasta local para dentro do container
COPY . /workspace

# 🛠️ Atualiza o apt e instala dependências do sistema (se necessário futuramente)
RUN apt-get update && apt-get install -y \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# 🔥 Comando padrão quando o container roda
CMD ["python", "main.py"]
