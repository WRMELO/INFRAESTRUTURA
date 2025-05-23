# ingest_raw.py – versão atualizada para preencher também file_name

import os
import tempfile
import hashlib
import json
import pandas as pd
from minio import Minio
from sqlalchemy import create_engine, text

# --- Configurações de conexão ---
MINIO_CLIENT = Minio(
    "minio:9000",
    access_key=os.getenv("MINIO_ROOT_USER", "admin"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD", "senhasegura"),
    secure=False
)
DB_URL = os.getenv(
    "RAW_DB_URL",
    "postgresql://postgres:senhasegura@database-services:5432/postgres"
)
engine = create_engine(DB_URL)
BUCKET_RAW = "raw-data"

def process_object(path: str) -> str:
    # Baixa o objeto para arquivo temporário e calcula checksum
    tmp = tempfile.NamedTemporaryFile(delete=False)
    MINIO_CLIENT.fget_object(BUCKET_RAW, path, tmp.name)
    tmp.close()

    sha = hashlib.sha256()
    with open(tmp.name, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    checksum = sha.hexdigest()

    # Extrai apenas o nome do arquivo para file_name
    file_name = os.path.basename(path)
    # Determina a extensão do arquivo e classifica apenas certas extensões como dados

    ext = os.path.splitext(file_name.lower())[1]

    data_exts = {".csv", ".parquet", ".xls", ".xlsx"}

    category = "data" if ext in data_exts else "info"
    # Classifica o arquivo como dado ou informação


    # Insere metadados incluindo file_name (coluna NOT NULL)
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO raw.data_files (object_path, file_name, checksum, category)
                VALUES (:path, :fname, :cs, :category)
                ON CONFLICT (checksum) DO NOTHING
                """
            ),
            {"path": path, "fname": file_name, "cs": checksum, "category": category}
        )
    return checksum

def main():
    errors = []
    print("Iniciando ingestão RAW...\n")

    for obj in MINIO_CLIENT.list_objects(BUCKET_RAW, recursive=True):
        try:
            cs = process_object(obj.object_name)
            print(f"✓ {obj.object_name} (checksum: {cs[:8]}…)")
        except Exception as e:
            errors.append((obj.object_name, str(e)))
            print(f"✗ Erro ao processar {obj.object_name}: {e}")

    print(f"\nIngestão concluída com {len(errors)} erro(s).\n")

if __name__ == "__main__":
    main()
