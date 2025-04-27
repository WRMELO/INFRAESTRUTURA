# Resumo do Pipeline EDA – Status até agora

Este documento consolida tudo o que foi realizado até o momento, servindo de referência para retomarmos amanhã.

---

## 1. Infraestrutura de Containers

1. **Docker Swarm Stack “eda”**  
   - Serviços levantados: `minio`, `database-services` (Postgres), `jupyter-cpu`, `jupyter-gpu`, `data-processing`, `data-visualization`, `vector-database`, `llm-services`, `api-gateway`, `web-services`, `gpu-utils`, `ml-training`.  
   - Ajustes de porta (8888, 9000, 5432, etc.) e remoção de conflitos com outros stacks (DS).

2. **Volumes e Montagens**  
   - Bind‐mount do host (`/home/wrm/datascience/projects`) para o container `jupyter-cpu` em `/home/jovyan/work`.  
   - Criação, no host, da hierarquia de pastas:  
     ```
     projects/
       └─ eda/
            └─ raw/
     ```
   - Redeploy da stack e atualização forçada do serviço `jupyter-cpu` para refletir as mudanças.

3. **Configuração Dev Container**  
   - Criação de `.devcontainer/devcontainer.json` corretamente seguindo o schema atual, com:  
     - `dockerComposeFile`, `service`, `workspaceFolder`.  
     - `features` (instalação do Git).  
     - `customizations.vscode` para extensões (Python, Jupyter, Pylance, Mermaid, Docker, GitLens) e settings (terminal, associações, formatação).  
   - Reconexão via **Attach to Running Container** no VS Code, garantindo kernel e ambiente Conda dentro do container.

4. **VS Code & Jupyter**  
   - Desabilitada persistência de terminais com `"terminal.integrated.enablePersistentSessions": false`.  
   - Notebook Editor associado a `*.ipynb` via `workbench.editorAssociations`.  
   - Extensões instaladas e funcionais dentro do container: Python, Jupyter, Mermaid Preview, GitLens, Docker, Pylance.

---

## 2. Banco de Dados (PostgreSQL)

1. **Schemas Criados**  
   - `raw`, `meta`, `curated`, `datalake`.  
   - Adição posterior do schema `staging`.

2. **Tabelas no Schema `raw`**  
   - `raw.data_files` com colunas:  
     - `id SERIAL PK`  
     - `file_name TEXT`  
     - `checksum TEXT`  
     - `ingest_timestamp TIMESTAMP DEFAULT now()`  
     - `object_path TEXT`  
   - Adicionada **constraint UNIQUE** em `checksum` para suportar `ON CONFLICT`.

3. **Tabelas de Metadados**  
   - `meta.audit_log` (registro de cada execução do pipeline).  
   - `meta.version_history` (versões de objetos/schemas vinculadas a `audit_log`).

---

## 3. Ingestão RAW

1. **Script `ingest_raw.py`**  
   - Localização: `/home/jovyan/work/eda/raw/ingest_raw.py`  
   - Funcionalidades:  
     - Conecta ao MinIO (`admin`/`senhasegura` em `minio:9000`).  
     - Lista objetos no bucket `raw-data`.  
     - Faz download para `/tmp`, calcula checksum SHA-256.  
     - Insere ou ignora duplicatas em `raw.data_files` usando `ON CONFLICT`.

2. **Testes Manuais**  
   - Upload de `teste_eda.txt` para MinIO via `mc cp`.  
   - Execução do script no container: `python ingest_raw.py` → “Ingestão RAW concluída.”  
   - Verificação no banco: `SELECT * FROM raw.data_files;`.

3. **Integração em Notebook**  
   - Criação de `01_ingestao_raw.ipynb` no diretório `notebooks/`.  
   - Uso de `%run ../eda/raw/ingest_raw.py` para invocar o script.  
   - Validação dos registros com Pandas e SQLAlchemy dentro do notebook.

4. **Dependências Instaladas**  
   - `minio`, `sqlalchemy`, `psycopg2-binary` via `pip install` no ambiente do kernel Jupyter.

---

## Próximos Passos

- **Passo 6 – Staging**:  
  1. Criar schema e tabela `staging.processed_data`.  
  2. Escrever `staging_process.py` em `/eda/staging`.  
  3. Testar no notebook `02_staging.ipynb`.

- **Passo 7 – Curated**: criar `curated_process.py` e notebook `03_curated.ipynb`.

- **Passo 8 – Data Lake**: criar `datalake_load.py` e notebook `04_datalake_load.ipynb`.

- **Passo 9 – Exploração**: notebook `05_exploracao_eda.ipynb` com gráficos iniciais.

Salve este resumo no seu `EDA.md` e use-o como checklist ao retomar. Até amanhã!
