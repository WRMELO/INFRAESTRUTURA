# Dockerfile base para api-gateway
# --- api-gateway Dockerfile ---
FROM python:3.10-slim

# 1) diretório de trabalho
WORKDIR /app

# 2) dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) código da aplicação
COPY . .

# 4) porta exposta
EXPOSE 8000

# 5) comando de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
