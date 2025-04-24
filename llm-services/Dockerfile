# Dockerfile base para llm-services
# 1. Imagem base
FROM python:3.10-slim

# 2. Diretório de trabalho
WORKDIR /app

# 3. Copia dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia o código da aplicação
COPY main.py .

# 5. Expõe porta e define entrypoint
EXPOSE 8000
CMD ["python", "main.py"]

