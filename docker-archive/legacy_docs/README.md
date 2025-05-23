
# 📦 Projeto: **Infraestrutura de Dados e IA – WRMELO**

## 🚀 **Objetivo**

Este repositório define uma **infraestrutura completa de dados e inteligência artificial**, baseada em containers Docker, operando em rede, com controle total sobre ingestão, curadoria, versionamento e modelagem de dados, tanto localmente quanto em ambiente de alta performance (Google Colab com GPU T4).

A arquitetura garante:

- 🔗 Governança e rastreabilidade dos dados.
- 🪣 Armazenamento seguro em Object Storage (MinIO).
- 🗄️ Controle relacional de metadados (PostgreSQL).
- 🧠 Logs, estados e pipelines não estruturados (MongoDB).
- 📈 Pipeline de dados como código.
- 📦 Infraestrutura como código.
- 🔥 Integração nativa com Google Drive e Colab para uso de GPUs T4.
- ✔️ Versionamento total pelo GitHub (`WRMELO/INFRAESTRUTURA`).

## 🏗️ **Arquitetura da Infraestrutura**

### 🔗 **Containers em Rede – Docker Swarm**

| Container                | Função Principal                                     |
|--------------------------|-------------------------------------------------------|
| `eda_jupyter-cpu`        | ✅ Desenvolvimento, notebooks, VSCode, ETL, EDA       |
| `eda_jupyter-gpu`        | ✅ Modelagem local com GPU (opcional)                 |
| `eda_minio`              | ✅ Object Storage (Data Lake)                         |
| `eda_database-services`  | ✅ PostgreSQL – Metadados, inventário, controle       |
| `mongo_mongodb`          | ✅ MongoDB – Logs, execução, estados                  |
| `eda_data-processing`    | 🚀 Serviços de ETL via API (opcional)                 |
| `eda_vector-database`    | 🚀 Vetorização, embeddings, IA                        |
| `eda_llm-services`       | 🚀 Modelos LLM locais (sumarização, embeddings)       |
| `eda_web-services`       | 🚀 APIs auxiliares, upload/download, microsserviços   |
| `eda_data-visualization` | 🚀 Dashboards, analytics                              |
| `eda_api-gateway`        | 🚀 Orquestração e roteamento de APIs                  |

## 🔗 **Pilares da Arquitetura**

- 🪣 **MinIO** → Armazenamento bruto, staging, curado, datasets, modelos.
- 🗄️ **PostgreSQL** → Governança, unicidade, versionamento, auditoria.
- 🧠 **MongoDB** → Logs, status, pipelines, dados semi-estruturados.
- 🔗 **Google Drive** → Transporte para e do Google Colab (T4).
- 🚀 **GitHub** → Versionamento de toda infraestrutura, notebooks, scripts e SQL.

## 🔥 **Pipeline Completo – Dados → IA**

### 1️⃣ **Captura – Google Drive → Local**
- Coleta os dados brutos no Drive.
- Download para `/workspace/eda/raw-data/projeto_x/` (container `eda_jupyter-cpu`).

**Commit Git:**  
`feat: captura inicial dos dados do Google Drive`

### 2️⃣ **Ingestão RAW**
- Calcula checksum (`md5`, `sha256`).
- Verifica unicidade no PostgreSQL (`inventario_dados`).
- Upload dos arquivos para MinIO (`raw-data/projeto_x/`).
- Registro dos metadados no PostgreSQL.

**Commit Git:**  
`feat: ingestão raw com controle de unicidade`

### 3️⃣ **Staging**
- Leitura do RAW no MinIO.
- Limpeza, padronização, validação de schemas.
- Grava staging em MinIO (`staging-data/projeto_x/`).
- Atualiza inventário em PostgreSQL (`staging_inventario`).

**Commit Git:**  
`feat: pipeline de staging implementado`

### 4️⃣ **Curadoria**
- Transformações finais, joins, engenharia de features.
- Grava dados curados em MinIO (`curated-data/projeto_x/`).
- Atualiza PostgreSQL (`curated_inventario`).

**Commit Git:**  
`feat: curadoria dos dados concluída`

### 5️⃣ **Dataset para Modelagem**
- Cria datasets (`train`, `test`, `validation`).
- Salva datasets em MinIO (`datasets/projeto_x/`).
- Exporta para Google Drive se necessário para modelagem no Colab.
- Atualiza inventário no PostgreSQL (`datasets_inventario`).

**Commit Git:**  
`feat: geração dos datasets para modelagem`

### 6️⃣ **Modelagem no Colab (T4)**
- Conecta ao Google Drive.
- Treina modelos (ML/DL/RL/NLP).
- Salva modelos e resultados no Drive e/ou MinIO.

**Commit Git:**  
`feat: pipeline de modelagem no Colab com GPU`

### 7️⃣ **Deploy e Outputs**
- Armazena modelos, outputs e resultados em:
   - MinIO (`models/projeto_x/`, `outputs/projeto_x/`).
   - PostgreSQL (`models_inventario`).
- Atualiza dashboards (`eda_data-visualization`).
- Publica APIs (`eda_api-gateway`).

**Commit Git:**  
`feat: deploy e outputs finalizados`

## 🔐 **Regras de Versionamento – GitHub**

> **Se não está no Git, não existe.**

- Todo notebook, script, SQL ou configuração alterado gera um commit rastreável.
- Commits são obrigatórios **antes e depois de executar qualquer pipeline relevante.**
- Toda alteração na estrutura de dados (schema, buckets, workflows) é registrada no Git.

### ✅ **Padrão de Commits**
- `init:` → Inicialização de estrutura.
- `feat:` → Novas funcionalidades ou pipelines.
- `fix:` → Correção de erros.
- `refactor:` → Refatorações sem alteração de funcionalidades.
- `docs:` → Atualização da documentação.
- `release:` → Entrega de versões estáveis.

## 📂 **Estrutura do Repositório**

```
/infra/               → Docker, network, volumes
/notebooks/           → Notebooks operacionais
/scripts/             → Scripts auxiliares (MinIO, Drive, PostgreSQL)
/sql/                 → Modelagem física dos bancos
/eda/                 → Dados locais organizados
/dockerfiles/         → Dockerfiles específicos
/configs/             → Configurações adicionais
```

## 🏛️ **Governança de Dados**

| Banco      | Função                                            |
|-------------|---------------------------------------------------|
| **MinIO**  | Dados brutos, staging, curados, modelos, outputs. |
| **PostgreSQL** | Inventário, versionamento, controle, auditoria.|
| **MongoDB**| Logs de execução, pipelines, estados temporários. |

## 🚦 **Fluxo Operacional**

```
Google Drive → Local → MinIO + PostgreSQL → Staging → Curado → Dataset → Colab (GPU) → Modelagem → Deploy → Outputs
```

## 🔥 **Conclusão**

Esta infraestrutura foi projetada para suportar projetos de dados e IA de forma:

- ✅ Robusta
- ✅ Escalável
- ✅ Auditável
- ✅ Documentada
- ✅ Integradora de ambientes locais e cloud (Colab GPU)

## 💡 **Regra Final:**  
**Pipeline de dados, de ponta a ponta, versionado, rastreável e auditável. Nenhum dado entra, se move ou sai sem controle rigoroso.**
