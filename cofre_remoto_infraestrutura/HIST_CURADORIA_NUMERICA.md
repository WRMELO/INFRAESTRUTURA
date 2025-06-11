# 📘 Curadoria Numérica — Histórico e Estratégia

📅 Atualizado em: 2025-06-01 20:44:50


## 1. Objetivo do Notebook

O notebook `curadoria_numerico` foi desenvolvido para realizar o tratamento, auditoria e validação de arquivos numéricos (como `.csv`, `.xls`, `.parquet`) presentes no bucket `staging-unique`, e gerar uma versão estruturada e consistente no bucket `curated-unique`.

Esse processo é essencial para garantir que os dados estejam em conformidade com os requisitos esperados por diferentes tipos de modelos analíticos, como Machine Learning, Deep Learning, Reinforcement Learning, BI e outros.



## 2. Etapas Realizadas

### 🔹 Curadoria Leve
- Leitura dos arquivos
- Validação mínima de estrutura
- Armazenamento em `staging-unique`
- Registro de auditoria em `curation_audit` com status `not_processed`

### 🔹 Diagnóstico Técnico
- Detecção de colunas booleanas, categóricas, datas disfarçadas, nulos
- Identificação de padrões por tipo de análise (`tipo_analise`)
- Interface interativa para configuração dos parâmetros (`crit_params`)

### 🔹 Curadoria Pesada
- Aplicação das transformações com base em `crit_params`
- Geração do `.parquet` e envio para `curated-unique`
- Registro em `curation_audit` com status `processed`, somente após sucesso



## 3. Estratégia por Tipo de Serviço Posterior

| Tipo de Análise          | Tratamento de Nulos | Booleanos | Categóricas      | Datas              | Normalização |
|--------------------------|---------------------|-----------|------------------|---------------------|---------------|
| Machine Learning         | Imputação / Remoção | Sim       | One-Hot Encoding | Sim (extração)     | Sim           |
| Deep Learning            | Remoção             | Sim       | Remoção          | Sim (parcial)      | Sim           |
| Reinforcement Learning   | Remoção             | Sim       | Encoding Opcional| Sim (completa)     | Sim           |
| Business Intelligence    | Imputação leve      | Sim       | Preservação      | Extração parcial   | Opcional      |
| Análise Estatística      | Remoção             | Sim       | Remoção ou Label | Conversão          | Não           |
| Séries Temporais         | Interpolação        | Sim       | Não se aplica    | Extração completa  | Sim           |



## 4. Controle de Consistência

Durante os testes, validamos que:

- Apenas arquivos `.csv` foram processados
- Apenas `.parquet` foram salvos em `curated-unique`
- O audit manteve apenas 1 entrada por arquivo, por tipo de curadoria
- Registros duplicados mais antigos foram eliminados via SQL com `ctid`
- A rastreabilidade entre `source_path` e `full_path` foi mantida




## 5. Considerações Finais

Este notebook cumpre um papel central na arquitetura de dados, padronizando e auditando a curadoria numérica para posterior uso em serviços de modelagem, análise e visualização. O pipeline está pronto para expansão futura com novas camadas de validação estatística e monitoramento.
