
# 📘 Rastreabilidade do Pipeline de Curadoria de Imagens

## 📊 Tabela Principal: Pipeline com Rastreabilidade e Auditoria

| Etapa | Movimentação | Quem | Como | Evento principal | Auditoria / Tabela |
|-------|--------------|------|------|------------------|---------------------|
| 1️⃣ **Recepção** | Cópia do **Google Drive** para o bucket `recepcao-raw` | ✅ **Todos os arquivos** encontrados no diretório selecionado pelo usuário | 🔁 Mantendo a **estrutura de pastas original** do Google Drive | 🏷️ **Criação do nome do projeto** (`project_name`) e do `prefix` (`prefix = pasta.split('-')[0]`) | 🗂️ `reception_audit`<br>Campos: `project_name`, `prefix`, `diretorio_origem`, `caminho_relativo`, `nome_arquivo`, `file_ext`, `hash_sha256`, `caminho_minio`, `data_processamento` |
| 2️⃣ **Movimentação para Storage Único** | Cópia de `recepcao-raw` para o bucket `storage-unique` | ✅ Apenas arquivos **únicos**, com base em `hash_sha256` | 🔍 Verificação de duplicatas via cálculo de hash<br>❌ Arquivos duplicados não são copiados ou são movidos para pasta de descarte | 🧾 **Verificação de unicidade absoluta** do conteúdo | 🗂️ `storage_audit`<br>Campos: `prefix`, `project_name`, `filename`, `file_ext`, `bucket`, `full_path`, `hash`, `hash_sha256`, `source_bucket`, `upload_date`, `copied_at`, `caminho_minio` |
| 3️⃣ **Curadoria Leve** | Cópia de `storage-unique` para `staging-unique` | ✅ Apenas imagens **válidas** (abrem sem erro com `PIL.Image.verify`) | 🧪 Validação de decodificabilidade da imagem, sem análise técnica ainda | 📌 Arquivos são preparados para curadoria técnica posterior | 🗂️ `staging_audit`<br>Campos: `prefix`, `filename`, `file_ext`, `bucket_origem`, `bucket_destino`, `status`, `curation_type`, `curation_status`, `timestamp`, `tipo`, `finalidade`, `full_path`, `novo_nome`, `comentario` |
| 4️⃣ **Diagnóstico Técnico + Seleção de Parâmetros** | (Sem movimentação) | Leitura de todas as imagens do bucket `staging-unique` | 📊 Coleta de métricas: `res_w`, `res_h`, `aspect_ratio`, `std`, `file_size`, `mode` | 🛠️ Geração interativa do dicionário `crit_params` via widgets | ❌ **Sem auditoria persistente** nesta etapa — os critérios são mantidos apenas em memória |
| 5️⃣ **Curadoria Pesada Final** | Cópia de `staging-unique` para `curated-unique` | ✅ Apenas imagens que passam nos critérios técnicos definidos em `crit_params` | 🔁 Conversão para modo (`L`, `RGB`, etc), padronização quadrada com `ImageOps.pad()`, salvamento como `.png`, verificação técnica final | 🧾 Registro final e técnico completo da imagem tratada<br>📂 Armazenamento definitivo para uso em DL/RL (Google Colab) | 🗂️ `curation_audit`<br>Campos: `prefix`, `filename`, `file_ext`, `curation_type`, `curation_status`, `full_path`, `source_path`, `bucket_origin`, `bucket_curated`, `curation_details` (JSON), `timestamp` |

---

## 🔑 Tabela Complementar: Chaves de Rastreabilidade e Consistência

| Campo / Chave | Presente em | Função técnica |
|---------------|-------------|----------------|
| `hash_sha256` | `reception_audit`, `storage_audit` | 🧬 Garante unicidade do conteúdo binário do arquivo |
| `prefix` + `filename` | Em todas as tabelas | 🔗 Ligação lógica e humana entre projeto e arquivo |
| `full_path` | `storage_audit`, `staging_audit`, `curation_audit` | 📁 Caminho absoluto no MinIO (rastreia movimentações) |
| `source_path` → `full_path` | `curation_audit` | 🔍 Traça o caminho da origem para o destino curado |

## CAMPOS EXISTENTES

![[imagem campos em tabelas.png]]