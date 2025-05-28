%%markdown
# 📑 Documento Técnico — Pipeline-Padrão de Dados  
*Versão: 2025-05-27*

---

## 0. Prompt-Origem do Gerente de Projeto (Você)

> **“O que estou fazendo é a criação de uma infraestrutura que me permita padronizar o máximo possível a fase de staging/eda/limpeza/curadoria dos dados recebidos de diversos processos e projetos e que serão usados para RL, DL, ML, imagem, engenharia, etc… dependendo do que for o objeto do projeto contratado.  
> […] DÚVIDA: dados esse tipo informação, podemos escolher os melhores (ou mais recomendados) tratamentos que o mercado usa e definirmos como nosso pipeline padrão?”**

Esse pedido disparou a análise e as decisões técnicas registradas abaixo.

---

## 1. Decisões Técnicas Consolidadas

| Tema | Decisão | Motivação |
|------|---------|-----------|
| **Stack de processamento** | **pandas + Polars** (Spark fora do pipeline-padrão). | Volumes previstos \< 100 GB; Polars entrega alta performance sem complexidade de cluster. |
| **Validação de dados** | **Great Expectations** em contêiner Alpine/Python. | Projeto open-source, integra com pandas/Polars, gera relatórios HTML, atende compliance. |
| **Versionamento / Linhagem** | **DVC** com *remote* `dvc-remote` no MinIO. | Mantém Git enxuto, usa hashes compatíveis com `storage_audit`, reprodutibilidade simples. |
| **Formato da camada curated** | Tabular em **Parquet** (Snappy, particionado `projeto/ano=mês=`).<br>Imagens em hierarquia simples no MinIO. | Parquet é padrão column-store; hierarquia de imagens preserva SHA-256 no Postgres. |
| **Nulos & outliers (tabular)** | Imputação por mediana + Winsorization (1º/99º pct).<br>Categóricos: categoria “missing”. | Estratégia robusta, 100 % automática e reversível por projeto. |
| **Reprodutibilidade** | **CLI** (`datapiper`) instalável via `pip install -e .` + notebooks apenas como tutoriais. | Idempotência, CI/CD amigável; evita divergência de lógica em notebooks. |

---

## 2. Arquitetura de Pastas & Controle de Versão

repo-root/
├── data/ # Controlado por DVC
│ ├── raw/ # Espelha recepcao-raw (MinIO)
│ ├── staging/
│ ├── validated/
│ └── curated/
├── src/
│ └── datapiper/ # Pacote CLI
├── dvc.yaml # Pipeline DVC
└── notebooks/ # EDA exploratório


### Prefixos no MinIO

storage-unique/
└── curated/
└── <project>/
├── tabular/year=2025/month=05/*.parquet
└── images/{train,test}/…


---

## 3. Comandos-Chave do CLI `datapiper`

| Comando | Ações principais | Persistência |
|---------|-----------------|--------------|
| `datapiper ingest --project X` | • Copia de `recepcao-raw` → `staging/` <br>• Registra no `reception_audit` | Arquivos locais + Postgres |
| `datapiper validate --project X` | • Executa expectativas GE <br>• Move bons arquivos → `validated/` | Relatório GE + status |
| `datapiper transform --project X` | • Limpeza/FE default <br>• Gera Parquet/imagens padronizadas | `storage_audit` + MinIO |
| **Pipeline completo** | `dvc repro` | Idempotente; push/pull via DVC remote |

---

## 4. Acesso Colab → MinIO (Dados Curados)

1. **Padrão oficial:** túnel Cloudflare Zero-Trust → URL HTTPS pública restrita.  
   ```python
   from minio import Minio
   client = Minio(
       "minio.<domínio-túnel>.com",
       access_key="admin",
       secret_key="*****",
       secure=True,
   )
    lternativas:

        rclone sync para Google Drive (duplica storage).

        Mirror para bucket GCS / S3 (custo extra).

5. Próximos Artefatos a Entregar

    pyproject.toml com entry-points datapiper-*.

    dvc.yaml inicial com as três etapas.

    Guia Cloudflare Tunnel + variáveis de ambiente Colab.

(Aguardando OK do Gerente para iniciar esses arquivos.)
6. Observações Gerenciais Registradas

    Spark removido por não haver volumes > 100 GB.

    Licenças: preferir sempre código aberto; GE cumpre.

    DVC Remote em MinIO aprovado; MongoDB disponível como opção futura de artefatos.

    Sem exigência de Delta Lake.

    Tratamentos default aceitáveis, mas ajustáveis por projeto.

7. Linha do Tempo de Discussão (resumida)

    Solicitação inicial de padronização de pipeline.

    Proposta de blocos reutilizáveis → seis questões levantadas.

    Ajuste conforme protocolo (IA decide “como”) → decisões técnicas definidas.

    Confirmações gerenciais (licença OSS, sem Spark, etc.).

    Detalhamento do fluxo CLI + Colab/MinIO.

    Este documento .md consolidado.

    %%markdown
## 8. Ajuste para Contexto de Pesquisa / P&D  
*(foco: prototipar rapidamente o melhor modelo, sem sobrecarga de “produção”)*

### 8.1 Revisão dos Componentes

| Componente | Situação anterior | Decisão para P&D | Racional |
|------------|------------------|------------------|----------|
| **Stack de processamento** | pandas + Polars | **Mantido** | Continuidade da produtividade e performance local; dispensa Spark. |
| **Validação de dados** | Great Expectations | **Opcional** → trocar por **ydata-profiling** (antes pandas-profiling) | GE pode ser exagerado para pesquisa; profiling rápido já sinaliza problemas. |
| **Versionamento de dados** | DVC + MinIO Remote | **Opcional** → pode ser substituído por **MLflow Tracking** (artefatos) ou simples timestamp em pasta | Menos fricção durante experimentação; MLflow já agrega métricas de modelo. |
| **CLI `datapiper`** | Pipeline idempotente | **Descartado nesta fase**; usar funções utilitárias dentro do notebook | Notebook interativo é melhor no ciclo explorar-ajustar-testar. |
| **Nulos & outliers** | Mediana + Winsorization (default) | **Mantido (default)**, mas facilmente modificável na célula de limpeza | Estratégia segura; ajuste livre por experimento. |
| **Arquitetura de pastas** | raw / staging / validated / curated (DVC) | **Simplificada** para `raw/` e `processed/` dentro do projeto | Menos camadas até ter modelo final. |
| **Acesso Colab → MinIO** | Túnel Cloudflare + MinIO | **Mantido** | Único ponto realmente necessário para compartilhar dados sem duplicação. |

---

### 8.2 Pipeline Minimalista Sugerido

1. **Notebook único** por projeto:  
   - `Imports & utils` (funções em `utils.py`).  
   - **Load raw** do MinIO.  
   - **EDA / Profiling** (`ydata-profiling.ProfileReport`).  
   - **Data-Cleaning & Feature-Engineering** (pandas / Polars).  
   - **Modelagem + Tracking** (MLflow opcional).  
2. **Versionamento leve**:  
   - Commit do notebook + `requirements.txt` no Git.  
   - Artefatos de modelo/dataset, se necessário, via MLflow ou pasta `artifacts/2025-05-27T15-34/`.  
3. **Dados**:  
   - Permanecem em MinIO → Prefixos `raw/` e `processed/`.  
   - Hashes ainda podem ir para Postgres, mas **não bloqueiam** a execução científica.

---

### 8.3 Conclusão

> **Para o ciclo de P&D, mantemos pandas + Polars e o acesso MinIO; substituímos GE / DVC / CLI por ferramentas mais leves (ydata-profiling, MLflow ou simples pasta de artefatos) e rodamos tudo diretamente no notebook.**  
> Quando (e se) o modelo precisar virar produção, reativamos o pipeline “robusto” previamente especificado.
