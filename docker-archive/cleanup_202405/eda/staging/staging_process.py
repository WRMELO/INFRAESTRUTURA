import json
import pandas as pd
from minio import Minio
from sqlalchemy import create_engine, text
import os

# Configurações
MINIO = Minio("minio:9000", access_key="admin", secret_key="senhasegura", secure=False)
DB_URL = "postgresql://postgres:senhasegura@database-services:5432/postgres"
engine = create_engine(DB_URL)
BUCKET = "raw-data"

def list_raw_entries():
    with engine.begin() as conn:
        return conn.execute(text("SELECT id, object_path FROM raw.data_files")).fetchall()

def process_file(raw_id, path):
    tmp = f"/tmp/{os.path.basename(path)}"
    MINIO.fget_object(BUCKET, path, tmp)
    df = pd.read_csv(tmp)
    df = df.dropna(how="all", axis=1)
    os.remove(tmp)
    return df

def load_to_staging():
    entries = list_raw_entries()
    with engine.begin() as conn:
        for raw_id, path in entries:
            df = process_file(raw_id, path)
            for rec in df.to_dict(orient="records"):
                conn.execute(text(
                    "INSERT INTO staging.processed_data (raw_file_id, record) VALUES (:rid, :rec)"
                ), {"rid": raw_id, "rec": json.dumps(rec)})
            # registrar no audit_log
            conn.execute(text(
                "INSERT INTO meta.audit_log (step_name, params, output_location, raw_file_id) "
                "VALUES ('staging_process', :params, :out, :rid)"
            ), {
                "params": json.dumps({"file": path}),
                "out": f"staging.processed_data (raw_id={raw_id})",
                "rid": raw_id
            })

if __name__ == "__main__":
    load_to_staging()
    print("Staging concluído.")
