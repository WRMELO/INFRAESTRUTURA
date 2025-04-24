# Dockerfile base para web-services
# Imagem base Python
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copia e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia aplicação
COPY main.py .

# Expõe porta do serviço
EXPOSE 8003

# Comando padrão
CMD ["python", "main.py"]

