# 🧾 Histórico Detalhado do Pipeline de Curadoria – Projeto FIAP / FDL

---

## 🟢 Ponto de Partida

### 🗓️ Início:
O desenvolvimento partiu da necessidade de estruturar um pipeline completo e auditável de ingestão, organização e curadoria de arquivos provenientes de múltiplas fontes, principalmente o Google Drive. O escopo original era receber arquivos, evitar duplicações e realizar transformações mínimas antes da utilização em modelos de aprendizado.

### 📌 Filosofia Inicial:
- **Simplicidade operacional**
- **Registro total via auditorias**
- **Separação clara por etapa (a, b, c...)**
- **Bucket único de entrada e saída**

---

## 🧱 Estrutura Inicial (Notebook A e B)

### ✅ `a-recepcao-raw.ipynb`:
- Responsável por:
  - Receber os arquivos do GDrive
  - Armazenar em `reception-raw` (MinIO)
  - Registrar auditoria completa em `reception_audit`

### ✅ `b-storage-movimentacao-unico.ipynb`:
- Responsável por:
  - Detectar arquivos únicos por `hash_sha256`
  - Copiar para `storage-unique`
  - Registrar em `storage_audit` com o `prefix` do projeto

### 💡 Decisão importante:
- Prefixo do projeto (ex: `FDL`) passou a ser o identificador de *pertencimento*
- Caminho no MinIO + registros no PostgreSQL passaram a seguir esse prefixo

---

## 📉 Dificuldade Enfrentada (Notebook B)

- 📍 Inicialmente, `CopySource()` usava caminho incorreto (`reception-raw/` incluído)
- 🐞 Isso gerava falhas silenciosas nas cópias
- 🔧 Solução: `removeprefix("reception-raw/")` + revisão completa do `storage_audit`

---

## 📈 Avanço: Organização única dos arquivos

Ao final do notebook B:
- Arquivos estavam corretamente salvos no bucket `storage-unique`
- Auditoria 100% rastreável
- Prefixo do projeto devidamente aplicado

---

## 🧠 Filosofia e Escopo Inicial da Curadoria (Notebook C)

### Inicial:
- Executar curadoria leve e avançada
- Salvar tudo diretamente em `storage-curated`
- Controlar com nomes como `curado_arquivo.ext`

### Evolução:
- Identificou-se a necessidade de um **cardápio** por tipo de dado:
  - `imagem`, `texto`, `numérico`, `vetor`
- Adicionou-se a necessidade de um **subcardápio** para imagens (DL vs RL)

---

## 🔄 Mudança de Estratégia

### Decisões tomadas:
1. Criar dropdown de seleção de projeto e tipo
2. Gerar amostras por tipo a partir da `storage_audit`
3. Permitir escolha entre DL e RL para imagens
4. Abandonar bucket intermediário (`storage-arranged`) e salvar direto em `storage-curated`
5. Unificar resize e transformações com base no destino final
6. Recriar a tabela `curation_audit` com estrutura final (prefix, tipo, origem, destino, etc.)

---

## 📍 Ponto Atual

- Notebooks A e B finalizados e testados
- Célula do notebook C lista tipos e permite escolha
- Notebook `curadoria_imagens.ipynb` iniciando com base em:
  - `prefix` do projeto
  - Lista de arquivos
  - Escolha de finalidade (DL ou RL)
  - Resize adequado e auditoria

---

## 🎯 Filosofia Atual

- **Curadoria direcionada por aplicação (DL ou RL)**
- **Sem bucket intermediário**
- **Curadoria final é o resultado direto e auditado**
- **Auditorias completas em `curation_audit`**

---

## 🔮 Sugestões para os Próximos Passos

1. [ ] Finalizar notebook de curadoria de imagens com escolha dinâmica DL/RL
2. [ ] Criar notebooks de curadoria para `texto`, `numerico`, `vetor`
3. [ ] Criar notebooks de validação estatística e visual por tipo curado
4. [ ] Automatizar um “validador” de consistência entre storage e banco
5. [ ] Gerar relatórios automáticos pós-curadoria com gráficos e logs

---

🧭 Este documento serve como rastreador de decisões, mudanças e próximas ações. Ele deve acompanhar cada nova versão ou pivotagem no pipeline.
