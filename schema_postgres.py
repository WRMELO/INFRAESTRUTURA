schema_postgres = {
    "curation_audit": [
        "id", "storage_id", "filename", "tipo_dado", "status", "data_tratamento"
    ],
    "reception_audit": [
        "id", "diretorio_origem", "caminho_relativo", "nome_arquivo",
        "hash_sha256", "tamanho_bytes", "data_processamento", "caminho_minio"
    ],
    "projects_registry": [
        "id", "prefix", "project_name", "description", "active", "created_at"
    ],
    "storage_audit": [
        "id", "prefix", "project_name", "bucket", "full_path", "filename",
        "size_bytes", "hash", "upload_date", "source_bucket", "hash_sha256"
    ],
    "storage_com_origem": [
        "storage_id", "filename", "bucket", "hash_sha256", "diretorio_origem",
        "caminho_relativo", "nome_arquivo", "caminho_minio", "data_processamento"
    ]
}