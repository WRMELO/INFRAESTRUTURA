# ✅ Continuação do Pipeline a partir do notebook `b-storage-movimentacao-unico.ipynb`

## 📌 Ponto de Partida

Encerrado o notebook `b-*`, temos:

- Todos os arquivos únicos armazenados no bucket `storage-unique`;
- Seus metadados registrados na tabela `storage_audit`, incluindo:
  - `prefix`, `project_name`, `filename`, `full_path`, `bucket`, etc.;
- Garantida a unicidade e o vínculo entre projeto e arquivo.

A partir desse ponto, iniciamos a **fase de curadoria**, conduzida pelo notebook `c-curadoria.ipynb`.

---

## 🧠 Papel do notebook `c-curadoria.ipynb`

O `c-*` tem como papel:

- Organizar visualmente os arquivos presentes em `storage_audit`;
- Permitir a seleção do projeto ou prefixo;
- Identificar e agrupar os arquivos por tipo de conteúdo:
  - `numerico`
  - `texto`
  - `imagem`
  - `vetor`
- Permitir a execução de pipelines específicos para cada tipo;
- Armazenar os arquivos tratados no bucket `curated-unique`;
- Registrar os resultados da curadoria na tabela `curation_audit`.

---

## ⚙️ Componentes implementados

### ✅ Widget Interativo (prefixo ↔ projeto)

- Dropdowns sincronizados: seleção por `prefix` ou `project_name`;
- Listagem dos arquivos disponíveis no `storage_audit`;
- Classificação automática por tipo de arquivo (extensão);
- Exibição agrupada por “cardápio” (tipo de dado).

### ✅ Nome de bucket padronizado: `curated-unique`

- Arquivos curados serão salvos com prefixo `curado_`;
- Ex: `curado_2000-01-24_-1.png`;
- Organização por tipo de dado:
  ```
  FDL/curated-unique/imagens/
  FDL/curated-unique/numerico/
  ```

### ✅ Registro em `curation_audit`

Cada ação de curadoria será documentada com:

- Nome final do arquivo;
- Projeto/prefix;
- Tipo de dado;
- Status do tratamento;
- Data de curadoria.

---

## 🚧 Próxima etapa (definida)

Começar o desenvolvimento dos pipelines de curadoria **por tipo de dado**.

### Decisão estratégica:

- Cada tipo será desenvolvido em seu próprio notebook:
  - `curadoria_imagens.ipynb`, `curadoria_numerico.ipynb`, etc.
- Quando estabilizado, será salvo como `.py`:
  - `imagens.py`, `numerico.py`, etc.
- O notebook `c-curadoria.ipynb` **apenas orquestrará** as chamadas para essas funções.

---

## ✅ Justificativa da abordagem

- Clareza e modularidade;
- Fácil versionamento e testes;
- Pipelines independentes e reutilizáveis;
- Permite adição de novos tipos de dado no futuro com facilidade.

---

## 📌 Status atual: PRONTO PARA COMEÇAR A CURADORIA

Primeiro tipo a ser tratado: **imagens** (por ser o mais simples).

Fluxo confirmado, interface funcionando, padrão de nome validado. A seguir: desenvolvimento do pipeline `curadoria_imagens.ipynb`.