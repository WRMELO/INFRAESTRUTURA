# Resumo Completo do Processo EDA

Este documento descreve toda a configuração e os componentes do pipeline de EDA implementado no repositório **`INFRAESTRUTURA`**, incluindo containers, scripts, notebooks e orquestração via Docker Swarm.

---

## 1. Estrutura do Repositório

```plaintext
INFRAESTRUTURA/
├── .devcontainer/                # Configuração do Dev Container (devcontainer.json)
├── dockerfiles/                  # Dockerfiles de cada serviço
│   ├── jupyter-cpu/Dockerfile
│   ├── jupyter-gpu/Dockerfile
│   ├── api-gateway/Dockerfile
│   ├── data-processing/Dockerfile
│   ├── data-visualization/Dockerfile
│   ├── database-services/Dockerfile
│   ├── vector-database/Dockerfile
│   ├── minio/Dockerfile
│   ├── ml-training/Dockerfile
│   ├── llm-services/Dockerfile
│   └── web-services/Dockerfile
│   └── docker-compose.yml       # Orquestração Swarm para stack "eda"
├── eda/                          # Scripts Python de cada etapa do pipeline
│   ├── raw/
│   │   └── ingest_raw.py         # Ingestão de arquivos brutos (RAW)
│   ├── staging/
│   │   └── staging_process.py    # Processamento raw → staging
│   └── curated/
│       └── curated_process.py    # Transformação staging → curated
├── notebooks/                    # Jupyter Notebooks de orquestração e validação
│   ├── 01_ingestao_raw.ipynb     # Executa ingest_raw e valida RAW
│   ├── 02_staging.ipynb          # Executa staging_process e valida staging
│   ├── 03_curated.ipynb          # Executa curated_process e valida curated
│   ├── 04_datalake_load.ipynb    # (Próximo) carrega curated → datalake
│   └── 05_exploracao_eda.ipynb    # Análise exploratória final
├── README.md                     # Visão geral e instruções iniciais
└── CHANGELOG.md                  # Histórico de alterações (Unreleased)
```

---

## 2. Dev Container

- Baseado em `dockerComposeFile: docker-compose.yml` no `.devcontainer/devcontainer.json`.
- Serviço **jupyter-cpu** monta todo o diretório raiz em `/home/jovyan/work`.
- VSC Desktop conecta-se via extensão Remote - Containers, permitindo edição de `.py` e `.ipynb`.
- Features instaladas: Git, Python, Jupyter, Mermaid, Docker, GitLens etc.

---

## 3. Orquestração Docker Swarm

O arquivo `dockerfiles/docker-compose.yml` define a **stack** `eda` com:

- **Rede**: `default` overlay, `attachable: true` → cria `eda_default` automaticamente.
- **Volumes nomeados**:
  - `db_data` para persistir PostgreSQL (`/var/lib/postgresql/data`).
  - `minio_data` para persistir MinIO (`/data`).
- **Serviços** (todos `replicated: 1`):

  | Serviço          | Imagem               | Portas       | Placement         |
  |------------------|----------------------|--------------|-------------------|
  | api-gateway      | `api-gateway:latest` | `8000:8000`  | manager           |
  | jupyter-cpu      | `jupyter-cpu:latest` | `8888:8888`  | manager           |
  | jupyter-gpu      | `jupyter-gpu:latest` | `8889:8888`  | worker            |
  | data-processing  | `data-processing:latest` | -       | manager           |
  | data-visualization | `data-visualization:latest` | `8050:8050` | manager        |
  | database-services | `database-services:latest` | `5432:5432` | manager        |
  | vector-database  | `vector-database:latest` | `8200:8200` | manager           |
  | minio            | `minio:latest`         | `9000-9001:9000-9001` | manager |
  | ml-training      | `ml-training:latest`   | -          | manager           |
  | llm-services     | `llm-services:latest`  | -          | manager           |
  | web-services     | `web-services:latest`  | `80:80`    | manager           |

**Redeploy automação**:

```bash
docker stack rm eda
docker stack deploy -c dockerfiles/docker-compose.yml eda
```

---

## 4. Pipeline de Ingestão e Processamento

### 4.1 RAW (Ingestão)

- **Script**: `eda/raw/ingest_raw.py`:
  - Lista objetos no bucket `raw-data` (MinIO).
  - Baixa cada arquivo temporariamente, calcula checksum SHA-256.
  - Extrai `file_name` e armazena `object_path`, `file_name`, `checksum` em `raw.data_files` (Postgres).
- **Notebook**: `01_ingestao_raw.ipynb`:
  - Célula única que roda `%run ../eda/raw/ingest_raw.py`.
  - Validações (amostra e contagem total) e registro em `meta.audit_log`.

### 4.2 STAGING (Processamento)

- **Script**: `eda/staging/staging_process.py`:
  - Lê `raw.data_files`, recupera objetos no bucket conforme `object_path`.
  - Aplica transformações de limpeza, tipagem, pivot etc. (configurável).
  - Grava resultado em `staging.processed_data`.
  - Insere registro em `meta.audit_log` com `step_name='staging_process'`, `raw_file_id`, `output_location`.
- **Notebook**: `02_staging.ipynb`:
  - Executa `%run eda/staging/staging_process.py`.
  - Validações de amostra, contagem e audit_log (filtra `step_name='staging_process'`).

### 4.3 CURATED (Transformação Final)

- **Script**: `eda/curated/curated_process.py`:
  - Garante `CREATE SCHEMA IF NOT EXISTS curated`.
  - Carrega `staging.processed_data` via Pandas.
  - Permite transformações customizadas (ex.: renomear colunas, conversão de datas, deduplicação).
  - Grava em `curated.data_curated` (append).
  - Insere registro em `meta.audit_log` com `step_name='curated_process'`.
- **Notebook**: `03_curated.ipynb`:
  - Executa `%run eda/curated/curated_process.py`.
  - Validações de amostra, contagem e audit_log (filtra `step_name='curated_process'`).

> **Próximos notebooks**:
>
> - `04_datalake_load.ipynb` para carregar curated → datalake.
> - `05_exploracao_eda.ipynb` para análise exploratória final.

---

## 5. Persistência e Volumes

- **PostgreSQL**: volume `eda_db_data` em `/var/lib/postgresql/data` — mantém tabelas RAW, staging, curated, datalake e meta.
- **MinIO**: volume `eda_minio_data` em `/data` — mantém buckets e objetos brutos.
- **Observação**: sem volumes, dados se perdem a cada `docker stack rm`.

---

## 6. Configurações Adicionais e Boas Práticas

- **Dependências Python**:
  - MinIO SDK (`minio`), SQLAlchemy, psycopg2-binary, Pandas.
  - Instalar via Dockerfile ou `%pip install` no notebook.
- **Rede**:
  - Overlay para comunicação entre manager e worker (GPU).
- **Desenvolvimento**:
  - Edição de `.py` via VS Code Explorer ou células `# %%` interativas.
  - Uso de Dev Containers garante consistência de ambiente.

---

> **Conclusão**: Com esta arquitetura, temos um pipeline reprodutível, escalável e auditável, do raw ao curated, pronto para downstream em datalake e análises.  
> Salve este resumo em **`README.md`** ou na documentação central para referência futura.
