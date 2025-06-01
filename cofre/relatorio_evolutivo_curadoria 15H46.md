
# 📘 Relatório Evolutivo do Projeto de Curadoria de Imagens

## 1. Onde Iniciamos

O projeto teve início com a construção de uma infraestrutura para ingestão de imagens oriundas de diferentes fontes, com foco em garantir **unicidade dos arquivos**, **registro de metadados** e a preparação para dois tipos de curadoria: leve (pré-processamento técnico) e pesada (análise e refinamento para uso em DL ou RL).

No início, utilizávamos apenas os buckets `recepcao-raw` e `storage-unique`, e a tabela `storage_audit` no PostgreSQL, que controlava os metadados dos arquivos únicos.

---

## 2. Filosofia e Escopo Naquele Momento

A filosofia era criar um pipeline **modular e auditável**, com ingestão manual em lotes e registro completo dos metadados. As decisões eram guiadas por:

- Garantia de unicidade baseada em hash.
- Armazenamento padronizado em MinIO com separação por bucket.
- Auditoria via PostgreSQL para rastreabilidade.
- Nenhum processamento automático: o fluxo era guiado por notebooks, sob controle do analista.

---

## 3. Como Caminhamos

O pipeline foi evoluindo com os seguintes notebooks e fases:

- `a-recepcao-raw.ipynb`: ingestão manual de arquivos do Google Drive para MinIO (bucket `recepcao-raw`) e auditoria inicial (`reception_audit`).
- `b-storage-movimentacao-unico.ipynb`: validação de unicidade via hash, movimentação para `storage-unique`, e preenchimento da tabela `storage_audit`.
- `c-curadoria-imagens.ipynb`: criação de vetores para processamento de imagens, e execução da curadoria leve e pesada, com registro em `staging_audit` e `curation_audit`.

Ao longo do caminho, implementamos widgets para seleção de projeto e tipo de curadoria (`DL` ou `RL`), além de indicadores visuais de progresso (barra `tqdm`).

---

## 4. Dificuldades Enfrentadas

- Falta de campos adequados em `staging_audit` e `curation_audit` para registrar tipo de curadoria (`curation_type`) e status de processamento (`curation_status`).
- Tentativas anteriores de renomear arquivos com prefixos como `arranjado_` e `curado_`, o que gerava confusão na rastreabilidade.
- Problemas em tentar forçar `NOT NULL` com `CHECK` em colunas com registros anteriores.
- Erros de execução ao rodar comandos SQL com sessões abertas em estado inconsistente (`InFailedSqlTransaction`).
- Execução de códigos que não respeitavam a arquitetura modular ou linguagem Python válida (uso de pseudo-blocos internos).

---

## 5. Como Resolvemos

- Adotamos a política de manter `filename` e `full_path` **inalterados em todos os buckets e auditorias**.
- Introduzimos os campos `curation_type` (`DL` ou `RL`) e `curation_status` (`processed`, `not_processed`) em ambas as tabelas de auditoria (staging e curation), com preenchimento controlado apenas pelo sistema.
- Corrigimos todos os notebooks para que usem **nome de arquivo consistente** e nunca dependam de renomeações externas.
- Optamos por realizar a curadoria leve e pesada em células distintas, mas no mesmo notebook (`c-curadoria-imagens.ipynb`), seguindo um fluxo sequencial e modular.

---

## 6. Avanços Conquistados

- Infraestrutura de buckets estável: `recepcao-raw`, `storage-unique`, `staging-unique`, `storage-curated`.
- Tabelas PostgreSQL auditáveis e alinhadas com o pipeline: `reception_audit`, `storage_audit`, `staging_audit`, `curation_audit`.
- Widget de seleção de projeto e tipo de curadoria operacional.
- Processo de curadoria leve já funcional, com preenchimento automático de auditorias.
- Política clara de versão, consistência e execução controlada por notebooks.

---

## 7. Ponto Exato em que Estamos Agora

- ✅ Notebooks A* e B* estão completos e congelados.
- ✅ Curadoria leve (1ª célula do C*) está validada.
- ✅ Campos de controle (`curation_type` e `curation_status`) adicionados e operacionais.
- 🟡 Curadoria pesada (2ª célula do C*) ainda não foi executada após zerar o `staging_audit` e `storage-curated`.

---

## 8. Filosofia e Escopo Atual

A filosofia foi consolidada para **maximizar rastreabilidade, modularidade e controle manual**, permitindo repetição segura de qualquer etapa. Mudanças importantes:

- Nenhum prefixo artificial no nome dos arquivos.
- Toda a lógica de curadoria é sequencial, modular e auditada.
- O notebook é o ponto central de controle da pipeline, e os `.py` gerados serão apenas versões consolidadas para reuso.

---

## 9. Sugestões para os Próximos Passos

1. ✅ Executar novamente a 1ª célula de curadoria leve no `c-curadoria-imagens.ipynb` com o novo modelo de auditoria.
2. ⏩ Executar a 2ª célula (curadoria pesada) validando todos os registros e gerando o `curation_audit`.
3. 🧪 Criar testes automatizados (em notebook ou script) para verificar integridade entre auditorias.
4. 📦 Consolidar o código atual em `curadoria_imagens.py` para uso dentro do container `c-curadoria`.
5. 🧭 Expandir o pipeline para aceitar curadorias adicionais, como vetores de texto e arquivos numéricos (com controle por tipo).

---

> Este documento foi gerado automaticamente para fins de rastreabilidade, documentação de projeto e transição de chats. Versão: `v1.0 - 2025-05-31`
