FROM jupyter/base-notebook:python-3.10

# Instalar rclone e dependências do Google Cloud SDK
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        apt-transport-https \
        ca-certificates \
        gnupg && \
    # Instalar rclone
    apt-get install -y --no-install-recommends rclone && \
    # Adicionar o repositório do Google Cloud SDK
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
        > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
        | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-cloud-sdk && \
    rm -rf /var/lib/apt/lists/*

# Voltar ao usuário jovyan
USER jovyan

# Definir diretório de trabalho
WORKDIR /home/jovyan/work

# Copiar e instalar dependências Python do requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expor porta padrão do Notebook
EXPOSE 8888

# Comando de inicialização do Jupyter Notebook
CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.allow_origin='*'"]
