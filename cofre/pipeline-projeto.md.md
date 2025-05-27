
📝 Modelo Obsidian: pipeline-projeto.md

  

# 🗺️ Pipeline do Projeto — Documentação Técnica

  

## 🔗 Infraestrutura Ativa

  

- ☁️ **MinIO** — Armazenamento de objetos

- Buckets:

- `recepcao-raw`

- `teste-raw`

- `raw`

  

- 🗄️ **PostgreSQL** — Banco de dados relacional

- Tabela principal de auditoria:

- `reception_audit`

  

- 🧠 **Ambiente de Desenvolvimento**

- Jupyter Notebook (no container `jupyter-cpu`)

- VSCode Desktop

- Obsidian (documentação e gestão de conhecimento)

  

---

  

## 🔍 Fluxo do Pipeline

  

```mermaid

graph TD

A[Bucket recepcao-raw] --> B[Tabela reception_audit]

B --> C[Verificação de hash SHA256]

C --> D[Validação de unicidade]

D --> E[Backup no Bucket raw]

D --> F[Backup no Bucket teste-raw]

B --> G[Registro de auditoria no PostgreSQL]

  

🧠 Observações

  

🔐 Toda movimentação de arquivos é auditada na tabela reception_audit.

  

📦 O bucket raw funciona como backup consolidado.

  

🧪 O bucket teste-raw é usado para testes, validações e simulações.

  

📑 Próximos Passos

  

Validar consistência entre reception_audit e os buckets.

  

Automatizar backups de recepcao-raw para raw.

  

Implementar rotina de limpeza controlada no bucket teste-raw.

  

Documentar processos de ingestão, auditoria e versionamento dos dados.

  

📂 Links Relacionados

  

[[Documentação MinIO]]

  

[[Documentação PostgreSQL]]

  

[[Instruções de Backup]]

  

[[Roadmap do Projeto]]

  

✍️ Histórico de Alterações

Data Descrição Autor

2025-05-26 Criação inicial do pipeline. WRM

2025-05-27 🔄 Adicionado fluxo de backup. IA GPT

🏁 FIM DO DOCUMENTO

  
  

---

  

## ✅ **Instruções:**

  

1. Crie um arquivo chamado, por exemplo, `pipeline-projeto.md` na sua vault do Obsidian.

2. Cole todo o conteúdo acima.

3. No Obsidian, abra o arquivo e ative o modo **Preview**.

4. O diagrama Mermaid e todo o texto serão renderizados automaticamente.

  

---

  

## 🔥 **Expansão:**

Este arquivo já está no formato para você adicionar:

- ✔️ Novos fluxos.

- ✔️ Novas tabelas.

- ✔️ Novos buckets.

- ✔️ Tarefas de acompanhamento (`[ ]`).

  

---

  

Se desejar, posso gerar:

- ✔️ O arquivo `.md` diretamente pronto para download.

- ✔️ A continuação desse documento com processos SQL, Bash, pipelines de automação.

  

👉 **Quer que eu envie o arquivo direto ou expandimos mais?**

  

Você disse:

bacana, mas não vou fazer afgora. n~çao tenho vault formatado ainda. vou continuar com o desenvolvimento como vinha fazendo. me dia aonde paramos.

O ChatGPT disse:

  

Perfeito. ✔️ Aqui vai um resumo exato e auditável de onde paramos, 100% alinhado ao protocolo:

✅ 📍 Status Atual — Checkpoint do Projeto

🔗 MinIO — Status

  

Buckets Existentes:

  

🟩 recepcao-raw → 📦 73 MiB, 23.883 objetos → ✅ Completo, origem dos dados atuais.

  

🟨 teste-raw → 📦 50 MiB, 15.410 objetos → 🔧 Backup/ambiente de testes.

  

⬜ raw → 📦 Vazio (0B) → 🔥 Você decidiu transformá-lo em backup consolidado dos dados de recepcao-raw.

  

✔️ Backup do recepcao-raw → raw foi executado corretamente via comando:

  

mc mirror myminio/recepcao-raw myminio/raw

  

🗄️ PostgreSQL — Status

  

Banco utilizado: postgres (único ativo).

  

Schema: public.

  

🔍 Tabelas Existentes:

Tabela Status

🗑️ arquivos_processados ❌ Deletada (estava vazia)

🗑️ projetos ❌ Deletada (estava vazia)

✅ reception_audit Ativa e funcional

  

✔️ A tabela reception_audit está corretamente povoada, funcionando como registro de auditoria dos arquivos processados.

🔗 Colunas principais da tabela reception_audit:

  

id — PK

  

diretorio_origem

  

caminho_relativo

  

nome_arquivo

  

hash_sha256

  

tamanho_bytes

  

data_processamento

  

caminho_minio

  

✔️ Registros confirmados:

  

Arquivos CSV (treino.csv, teste.csv), imagens (.png), e HTML (visualizacao.html) vinculados ao ativo BBAS3.SA (e outros ativos similares estruturados da mesma forma).

  

🔧 Ferramentas Configuradas e Operacionais:

  

🐳 Containers:

  

jupyter-cpu → notebooks, Python.

  

minio → armazenamento S3-like.

  

postgres → banco de dados relacional.

  

✅ mc → funcionando perfeitamente no Ubuntu (acesso ao MinIO).

  

✅ pgcli → acesso ao PostgreSQL com CLI avançado.

  

✅ 🔥 Obsidian instalado, mas ainda sem Vault configurado. (✔️ Pronto para futura estruturação documental.)