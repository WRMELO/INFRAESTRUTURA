# Dockerfile base para jupyter-gpu
# —————————————————————————————————————
# Imagem base Jupyter + Python 3.10
# —————————————————————————————————————
FROM jupyter/base-notebook:python-3.10

USER root

# Instala pacotes de SO
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      git \
      curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala libs Python
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

USER $NB_UID
WORKDIR /home/jovyan/work

EXPOSE 8888

# Inicia JupyterLab sem token e acessível em 0.0.0.0
CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.ip='0.0.0.0'"]

