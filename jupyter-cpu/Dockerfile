FROM jupyter/base-notebook:python-3.10

# Instalar rclone via apt
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends rclone && \
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
