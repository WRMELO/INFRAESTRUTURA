
# 📋 METADATA_STRUCTURE.md

## 🎯 Objetivo

Documentar a estrutura dos metadados utilizados no PostgreSQL para controle de governança de dados, unicidade e versionamento.

---

## 🗃️ Tabela: inventario_dados

| Campo            | Tipo         | Descrição                              |
|------------------|--------------|-----------------------------------------|
| id               | SERIAL       | Identificador único                     |
| projeto          | TEXT         | Nome do projeto                         |
| tipo_dado        | TEXT         | raw / staging / curated / dataset       |
| caminho_minio    | TEXT         | Caminho completo no MinIO               |
| checksum_md5     | TEXT         | Hash do arquivo                         |
| dt_upload        | TIMESTAMP    | Data de upload                          |
| origem           | TEXT         | Origem do dado (ex: Drive, pipeline)    |
| valido           | BOOLEAN      | Se é válido ou duplicado                |

---

## 🗃️ Tabela: staging_inventario

Semelhante à `inventario_dados`, mas com informações sobre validação e conformidade de schema.

---

## 🗃️ Tabela: curated_inventario

- Acrescenta:
  - `descricao_transformacao` (TEXT)
  - `versao` (TEXT)

---

## 🗃️ Tabela: datasets_inventario

- Acrescenta:
  - `tipo_dataset` (train/test/validation)
  - `dimensao` (INTEGER)
  - `modelo_destino` (TEXT)

---

## 🗃️ Tabela: models_inventario

| Campo            | Tipo         | Descrição                              |
|------------------|--------------|-----------------------------------------|
| id               | SERIAL       | Identificador                           |
| nome_modelo      | TEXT         | Nome lógico                             |
| projeto          | TEXT         | Projeto associado                       |
| caminho_minio    | TEXT         | Caminho do artefato salvo               |
| data_treinamento | TIMESTAMP    | Data de treino                          |
| metrica_principal| TEXT         | Ex: AUC, RMSE, Accuracy                 |
| valor_metrica    | FLOAT        | Valor da métrica                        |

---

## 🔐 Segurança e Auditoria

Todos os registros possuem controle de data, origem, e hash. Consultas cruzadas permitem detectar inconsistências, arquivos faltantes, ou duplicados no MinIO.
