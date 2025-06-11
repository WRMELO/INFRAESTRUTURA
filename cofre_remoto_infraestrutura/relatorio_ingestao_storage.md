# ✅ RELATÓRIO TÉCNICO: Ingestão e Movimentação de Arquivos RAW → Storage Único

## 1. 📂 Estrutura Lógica Definida

O pipeline atual é baseado em três etapas centrais, cada uma refletida por um notebook:

| Etapa | Notebook | Função Principal |
|-------|----------|------------------|
| **Ingestão** | `a-reception-raw.ipynb` | Receber arquivos do Google Drive, enviar ao MinIO (`reception-raw`) e registrar auditoria em `reception_audit` |
| **Movimentação única** | `b-storage-movimentacao-unico.ipynb` | Copiar apenas arquivos únicos para `storage-unique`, com prefixo de projeto, e registrar em `storage_audit` |
| **Curadoria (a seguir)** | `c-curadoria-imagens.ipynb` | Tratar imagens com resize e padronização, salvar no bucket `curated-unique` e auditar em `curation_audit` |

## 2. 🧠 Regras definidas e consensuais

### 🟡 Sobre nomes e prefixos

- A **pasta original do Google Drive** (`FIAP_PI/`, `BBAS3.SA/`, etc.) **não representa o projeto**.
- O **prefixo do projeto (`FDL`, `XYZ`, etc.)** é o identificador oficial do projeto, registrado em `projects_registry` e aplicado **a partir do notebook B**.
- O `prefix` deve ser **explicitamente inserido no destino (`storage-unique`)**, e registrado como tal na `storage_audit`.

## 3. 🧩 Arquitetura física dos dados

| Local | Conteúdo físico real |
|-------|-----------------------|
| `reception-raw` (MinIO) | Arquivos com caminho como `FIAP_PI/BBAS3.SA/arquivo.png` |
| `reception_audit` | `caminho_minio = reception-raw/FIAP_PI/...` |
| `storage-unique` | Esperado: `FDL/FIAP_PI/...`, mas atualmente: **zero objetos** |
| `storage_audit` | Esperado: registros com `prefix=FDL`, mas atualmente: **zero registros** |

## 4. ✅ Funções dos notebooks

### 📗 Notebook A — `a-reception-raw.ipynb`
- 🔹 Recebe arquivos da pasta montada do GDrive
- 🔹 Envia para o bucket `reception-raw`
- 🔹 Calcula o `hash_sha256`
- 🔹 Salva os metadados em `reception_audit`
- ✅ **Confirmado como funcionando** — 23.883 arquivos inseridos com sucesso

### 📘 Notebook B — `b-storage-movimentacao-unico.ipynb`
- 🔸 Lê os registros da `reception_audit`
- 🔸 Verifica quais `hash_sha256` **ainda não estão na `storage_audit`**
- 🔸 Copia o arquivo correspondente do bucket `reception-raw` para `storage-unique`
- 🔸 Aplica o `prefix` do projeto no destino (`FDL/FIAP_PI/...`)
- 🔸 Registra metadados completos em `storage_audit`

🔴 **Problemas detectados**:
- Nenhum arquivo foi copiado fisicamente para `storage-unique`
- Nenhum registro foi inserido na `storage_audit`
- Nenhuma mensagem de erro relevante foi exibida durante a cópia

## 5. 🧪 Testes executados

### 🔍 **Teste 1 – Inspeção de arquivos no MinIO**
```bash
mc ls --recursive local/storage-unique | grep '^FDL/' | wc -l
```
🔴 Resultado: **0 arquivos físicos**

### 🔍 **Teste 2 – Inspeção da `storage_audit` no PostgreSQL**
```bash
SELECT COUNT(*) FROM storage_audit WHERE prefix = 'FDL';
```
🔴 Resultado: **0 registros no banco**

### 🔍 **Teste 3 – Inspeção cruzada com Python**
- Listagem direta do bucket `reception-raw` retornou:
  ```
  FIAP_PI/BBAS3.SA/imagens/teste/comprar/2019-04-29_1.png
  ```

- Tabela `reception_audit` mostrava:
  ```
  caminho_minio = reception-raw/FIAP_PI/BBAS3.SA/...
  ```

- Tabela `storage_audit` esperava:
  ```
  prefix = FDL, caminho_minio = FDL/FIAP_PI/..., full_path = FDL/FIAP_PI/...
  ```

✅ **Confirmado que os caminhos reais e os esperados estavam desalinhados.**

## 6. 🛠️ Tentativas de correção já feitas

| Ação | Status |
|------|--------|
| Remoção de constraint de unicidade de `reception_audit` | ✅ Concluído |
| Limpeza total de `storage_audit` e `storage-unique` | ✅ Realizado |
| Ajuste no `CopySource` | 🔁 **Parcialmente aplicado** (mas ainda usando caminho errado) |
| Inclusão do prefixo do projeto via widget | ✅ Aplicado |
| Diagnóstico completo com inspeção tripla (MinIO, DB, código) | ✅ Concluído |

## 7. 🧨 Conclusão da falha

> O notebook B está tentando copiar objetos do MinIO usando o caminho:
```
reception-raw/FIAP_PI/...
```
> Mas o `CopySource(bucket, object_name)` espera **somente**:
```
FIAP_PI/...
```

A tentativa de cópia falha silenciosamente porque `client.copy_object(...)` **não encontra o arquivo original** no bucket de origem.

## ✅ Ação corretiva final e definitiva

Ajustar a linha de origem no notebook B para:

```python
origem_path = row["caminho_minio"].removeprefix("reception-raw/").lstrip("/")
```

E então:

```python
client.copy_object(
    BUCKET_DESTINO,
    destino_path,
    CopySource(BUCKET_ORIGEM, origem_path)
)
```

## 🧾 Próximos passos

1. ✅ Substituir o notebook B atual com a célula corrigida acima
2. ✅ Reexecutar notebook B com projeto `FDL`
3. 🔁 Verificar novamente com os 3 testes
4. ✅ Só então seguir para o notebook C (`c-curadoria-imagens.ipynb`)
