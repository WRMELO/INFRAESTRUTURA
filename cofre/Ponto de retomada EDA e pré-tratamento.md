
# ✅ Ponto de Retomada do Projeto: EDA e Pré-Tratamento

> **Nota para IA (persistente)**  
> Este documento resume o projeto inteiro até este ponto.  
> Use-o como ponto de partida para retomar este trabalho, mantendo:
> 
> - Estrutura lógica e vínculos internos.
> - Nomes das tabelas, buckets, containers e caminhos reais.
> - Imagens referenciadas (se necessárias, anexar posteriormente).
> - Continue **exatamente a partir daqui**.

---

## 📦 Infraestrutura Base – Repositório `WRMELO/INFRAESTRUTURA`

Conforme descrito em `Descrição da INFRA para desenvolvimento do EDA.md`:

### Diretórios

- `notebooks/`:  
  - `a-recepcao-raw.ipynb`: recebe arquivos e registra na `reception_audit`.
  - `b-storage-movimentacao-unico.ipynb`: valida unicidade e preenche `projetos` e `arquivos`.
- `cofre/`: armazena documentos técnicos e de planejamento.
- `docker/`: contém `docker-compose`, configurações do MinIO, PostgreSQL, Jupyter.

### Serviços Docker

- **MinIO**: Armazenamento de objetos (`recepcao-raw`, outros).
- **PostgreSQL**: Armazenamento de metadados e controle.
- **Jupyter**: Execução e exploração de notebooks.

### Tabelas de Controle

- `reception_audit`: arquivos recebidos.
- `projetos`: unicidade de projetos.
- `arquivos`: unicidade de arquivos.

### Fluxo Atual

1. **Ingestão**: Google Drive → Bucket `recepcao-raw`.
2. **Auditoria**: Registro na tabela `reception_audit`.
3. **Movimentação**: `b-storage-movimentacao-unico.ipynb`.
4. **Armazenamento Curado**: buckets separados, mantendo nome original.

---

## 🧠 Estratégia de EDA e Pré-Tratamento

Conforme detalhado em `Estratégia de EDA e Pré-Tratamento de Dados.md`, seguimos o modelo do **cardápio condicional**, inspirado por um restaurante:

### Abordagens

- **Genérica**: única pipeline universal.
- **Condicional (adotada)**: pipeline adaptado ao tipo de dado.

### Estrutura do Cardápio

| Tipo de Dado | Entradas (Pré-processamento)                      | Primeiro Prato (EDA básica)                 | Segundo Prato (Tratamento Avançado)            | Sobremesa (Entrega Final)                          | Serviço Complementar                            |
| ------------ | ------------------------------------------------- | ------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ------------------------------------------------ |
| CSV/Excel    | Remoção de NaNs, encoding, colunas inúteis        | Distribuições, outliers, correlações        | Feature Eng., Normalização                     | CSV/Parquet curado no bucket (nome original)       | Identificação das partes do nome                |
| Texto/PDF    | OCR, limpeza, parsing                             | Word Cloud, entidades nomeadas              | Embeddings, NLP clássico                       | JSON curado com estrutura padronizada              | Idem                                             |
| Imagem/Áudio | Resize, metadados, padronização                   | Histogramas, espectrogramas, clustering     | Denoise, Normalização de formato               | Formatos padrão organizados por origem            | Idem                                             |

---

## 🧩 Integração dos Documentos

Conforme `HUB_EDA_PRE-TRATAMENTO.md`, a base de tudo está interligada:

1. Infraestrutura: `Descrição da INFRA para desenvolvimento do EDA`
2. Estratégia de EDA: `Estratégia de EDA e Pré-Tratamento de Dados`
3. Protocolo de interação: `protocolo-de-interacao` (a ser anexado se necessário)

---

## 🔁 Status Atual e Próximos Passos

- ✅ Repositório estruturado e funcional.
- ✅ Pipelines de recepção e movimentação testados.
- 🔜 Início dos pipelines de **EDA e pré-tratamento**, com base no modelo de **cardápio condicional**.

---

## 🧭 Próxima Etapa Recomendada

> Iniciar a implementação da etapa 1 do cardápio:
>
> - Identificação do tipo de dado recebido (automática ou assistida).
> - Direcionamento para pipeline específico (condicional).
> - Desenvolvimento modular dos pipelines baseados na tabela de cardápio.

---

## 📍 Final do Registro

**Atenção IA: continue exatamente a partir deste ponto. Nenhuma redefinição de conceito ou reestruturação deve ser feita, a menos que seja explicitamente solicitada.**