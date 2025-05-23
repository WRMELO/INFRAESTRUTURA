
# 🧱 PIPELINE_DESIGN.md

## 🎯 Objetivo
Este documento descreve detalhadamente o desenho funcional do pipeline de dados da infraestrutura WRMELO, do ponto de entrada (dados brutos) até o treinamento de modelos e deploy de resultados.

---

## 🔂 Fluxo Geral do Pipeline

```
Google Drive → Local (Jupyter Container) 
→ MinIO (Object Storage) + PostgreSQL (Inventário)
→ Staging → Curadoria → Datasets → Colab (GPU)
→ Modelagem → Deploy → Outputs
```

---

## 1️⃣ Captura de Dados

- **Origem:** Google Drive (usuário ou integração)
- **Destino inicial:** Container `eda_jupyter-cpu` → `/workspace/eda/raw-data/`
- **Ferramentas:** `00_capture_drive.ipynb`, `pydrive`

---

## 2️⃣ Ingestão RAW

- Verificação de unicidade (via checksum)
- Registro no PostgreSQL: `inventario_dados`
- Armazenamento no MinIO: `raw-data/projeto_x/`

---

## 3️⃣ Staging

- Processamento inicial, limpeza, padronização
- Salvamento em:
  - PostgreSQL: `staging_inventario`
  - MinIO: `staging-data/projeto_x/`

---

## 4️⃣ Curadoria

- Engenharia de variáveis, transformações finais
- Registro em:
  - PostgreSQL: `curated_inventario`
  - MinIO: `curated-data/projeto_x/`

---

## 5️⃣ Geração de Datasets

- Separação em `train`, `test`, `validation`
- Exportação para Colab (Google Drive) e MinIO
- Registro em: `datasets_inventario`

---

## 6️⃣ Modelagem no Colab (T4)

- Acesso aos dados via Google Drive
- Execução com GPU para ML/DL/RL/NLP
- Armazenamento de modelos em Drive e/ou MinIO

---

## 7️⃣ Deploy e Outputs

- Upload dos modelos para MinIO: `models/projeto_x/`
- Resultados e métricas salvos como `outputs/`
- APIs publicadas se necessário

---

## 🔁 Ciclos Iterativos

- Todo notebook e script modificado gera commit.
- Cada etapa do pipeline é acompanhada por metadados e logs.
