# Imagem base Python
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copia dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia aplicação
COPY main.py .

# Comando padrão
CMD ["python", "main.py"]
