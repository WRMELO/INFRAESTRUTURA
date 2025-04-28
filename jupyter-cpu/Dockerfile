FROM jupyter/base-notebook:python-3.10

WORKDIR /home/jovyan/work

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888

CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.allow_origin='*'"]
