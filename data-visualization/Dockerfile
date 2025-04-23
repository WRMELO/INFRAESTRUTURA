# Dockerfile base para data-visualization
# --- data-visualization Dockerfile ---
FROM python:3.10-slim

# 1) Diretório de trabalho
WORKDIR /app

# 2) Instalação das dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Código da aplicação
COPY . .

# 4) Porta exposta pelo Dash
EXPOSE 8050

# 5) Comando de inicialização
CMD ["python", "main.py"]

