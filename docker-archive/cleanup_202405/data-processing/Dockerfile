# Dockerfile base para data-processing
# --- data-processing Dockerfile ---
FROM python:3.10-slim

# 1) definir diretório de trabalho
WORKDIR /app

# 2) copiar e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) copiar código da aplicação
COPY . .

# 4) expor porta para API (ajuste se necessário)
EXPOSE 8001

# 5) comando de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

