# Dockerfile base para vector-database
# Imagem base Python
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copia e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia aplicação
COPY main.py .

# Porta do serviço
EXPOSE 8002

# Comando padrão
CMD ["python", "main.py"]

