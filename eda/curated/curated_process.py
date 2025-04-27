#!/usr/bin/env python3
# eda/curated/curated_process.py
#
# Transforma dados de staging em curated.data_curated e grava auditoria.

import os
import json
import pandas as pd
from sqlalchemy import create_engine, text

def main():
    # --- Configuração de conexão ---
    DB_URL = os.getenv(
        "RAW_DB_URL",
        "postgresql://postgres:senhasegura@database-services:5432/postgres"
    )
    engine = create_engine(DB_URL)

    # --- Parâmetros de saída ---
    CURATED_SCHEMA = "curated"
    CURATED_TABLE  = "data_curated"

    # 1) Garante que o schema curated existe
    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {CURATED_SCHEMA};"))

    # 2) Lê todos os dados de staging
    df = pd.read_sql(f"SELECT * FROM staging.processed_data;", engine)

    # 3) Aqui você pode incluir suas transformações:
    # Exemplo:
    # df = df.rename(columns={"old_col": "new_col"})
    # df["some_date"] = pd.to_datetime(df["some_date"])
    # df = df.drop_duplicates(subset=["id"])

    # 4) Grava no schema curated.data_curated
    df.to_sql(
        name       = CURATED_TABLE,
        con        = engine,
        schema     = CURATED_SCHEMA,
        if_exists  = "append",
        index      = False
    )

    # 5) Registra no audit_log
    with engine.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO meta.audit_log (step_name, params, output_location) "
                "VALUES (:step, :params, :out)"
            ),
            {
                "step":   "curated_process",
                "params": json.dumps({}),
                "out":    f"{CURATED_SCHEMA}.{CURATED_TABLE}"
            }
        )

    # 6) Feedback ao usuário
    print(
        f"Curated process concluído: "
        f"{len(df)} registros em {CURATED_SCHEMA}.{CURATED_TABLE}"
    )

if __name__ == "__main__":
    main()
