# Dockerfile base para jupyter-cpu
# --- jupyter-cpu Dockerfile ---
FROM jupyter/base-notebook:python-3.10

# 1) definir diretório de trabalho
WORKDIR /home/jovyan/work

# 2) copiar e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) expor porta padrão do Notebook
EXPOSE 8888

# 4) iniciar o Notebook sem token (permite acesso externo)
CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.allow_origin='*'"]

