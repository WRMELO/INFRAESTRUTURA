l# 🚩 Documentação de Progresso — Projeto de Movimentação e Auditoria de Arquivos no MinIO

## 📅 **Período:** Este documento resume todas as ações realizadas no chat corrente.

---

## 🧠 **Objetivo Geral do Trabalho**

Construir um pipeline robusto, auditável e seguro para:

- ✔️ Movimentação de arquivos do bucket `recepcao-raw` (temporário para os arquivos, mas permanente como bucket) para o bucket definitivo `storage-unique` no MinIO.
- ✔️ Controle rigoroso de unicidade de arquivos.
- ✔️ Auditoria completa via PostgreSQL.
- ✔️ Possibilidade de seleção ou criação de projetos que são usados para organizar a estrutura no bucket destino.
- ✔️ **Persistência dos metadados dos arquivos recebidos na tabela `reception_audit`**, garantindo rastreabilidade mesmo após remoção física dos arquivos do `recepcao-raw`.
- ✔️ Preservação do bucket de recepção **(estrutura permanente, porém sem obrigação de manter os arquivos após processamento)**.

---

## 🏗️ **Decisões Arquiteturais Tomadas**

1. **Separação dos buckets:**
   - `recepcao-raw` → Bucket de recepção permanente, usado para upload inicial. Os arquivos são temporários, mas os metadados ficam registrados na tabela `reception_audit`.
   - `storage-unique` → Bucket definitivo de armazenamento único e auditável.

2. **Controle de projetos:**
   - Criação de uma tabela PostgreSQL chamada `projects_registry` para registrar projetos e seus prefixos.
   - O prefixo do projeto é usado na estruturação dos arquivos no bucket definitivo.

3. **Auditoria dos arquivos de movimentação:**
   - Criação da tabela `storage_audit` no PostgreSQL para registrar:
     - Prefixo do projeto.
     - Nome do projeto.
     - Caminho completo no bucket destino.
     - Tamanho.
     - Data de movimentação.
     - Bucket de origem.
   - Auditoria é essencial para garantir unicidade e rastreabilidade.

4. **Auditoria da recepção:**
   - Criação da tabela `reception_audit` no PostgreSQL para registrar:
     - Bucket de origem (`recepcao-raw`).
     - Nome do arquivo.
     - Caminho completo dentro do bucket.
     - Data de upload.
     - Tamanho do arquivo.
   - Este registro permite rastreabilidade completa dos arquivos recebidos, **independentemente de serem posteriormente excluídos do bucket `recepcao-raw`.**

5. **Pipeline com verificação dupla:**
   - ✔️ Verifica se o arquivo já está registrado no banco `storage_audit`.
   - ✔️ Verifica se o arquivo existe fisicamente no bucket `storage-unique`.
   - 🔥 **Se ambos forem verdadeiros → não copia.**
   - 🔥 **Se qualquer um estiver ausente → copia e registra.**

---

## ⚙️ **Desafios e Dificuldades Enfrentadas**

- 🚩 Problema de conexão entre containers Jupyter ↔ PostgreSQL e Jupyter ↔ MinIO:
  - ➝ Corrigido usando o nome dos containers na rede Docker (`postgres_db`, `minio`), evitando `localhost`.

- 🚩 Erro no uso de `copy_object`:
  - ➝ Faltava encapsular o objeto de origem com `CopySource`.
  - ✔️ Solução aplicada com sucesso.

- 🚩 Problemas na persistência das variáveis globais no notebook:
  - ➝ Detectado que variáveis como `projeto_prefix` e `projeto_nome` não persistem entre execuções isoladas.
  - ✔️ Solução: Unificar **seleção/criação do projeto e pipeline de movimentação na mesma célula.**

- 🚩 Compreensão do comportamento da barra de progresso (`tqdm`):
  - ➝ Mesmo sem cópia, a barra avança, pois reflete a iteração sobre os objetos, e não a ação de cópia em si.
  - ✔️ Decisão: Implementação de **contadores dinâmicos** de:
    - Arquivos efetivamente copiados.
    - Arquivos detectados como repetidos.

- 🚩 Validação de comportamento:
  - ✔️ Testamos rodar o pipeline duas vezes.
  - ✔️ Na segunda execução, **nenhum arquivo foi copiado**, e a contagem de "repetidos" refletiu corretamente os arquivos já processados.

---

## 🏁 **Estado Atual do Projeto**

| Item                          | Status                            |
|-------------------------------|------------------------------------|
| Bucket `recepcao-raw`         | ✅ Permanente, funcional, com auditoria na tabela `reception_audit` |
| Bucket `storage-unique`       | ✅ Pronto, funcionando, com auditoria ativa |
| Tabela `projects_registry`    | ✅ Operacional, permitindo seleção e cadastro de projetos |
| Tabela `storage_audit`        | ✅ Funcionando, com rastreabilidade da movimentação |
| Tabela `reception_audit`      | ✅ Funcionando, registrando todos os arquivos recebidos |
| Pipeline de movimentação      | ✅ 100% funcional, robusto e auditável |

---

## 🔥 **Operação de Reset Realizada com Sucesso**

- ✔️ Limpamos:
  - Bucket `storage-unique`.
  - Tabela `storage_audit`.
  - Tabela `projects_registry`.
- ✔️ **Mantivemos:**
  - Bucket `recepcao-raw` como fonte de dados (estrutura permanente).
  - Tabela `reception_audit` como registro histórico dos arquivos que passaram pela recepção.

---

## 🧠 **Melhorias Implementadas no Pipeline**

- 🔧 Inclusão de contadores dinâmicos para:
  - Quantidade de arquivos copiados.
  - Quantidade de arquivos ignorados por já existirem.

- 🔧 Mensagens claras na barra de progresso:
  - ✔️ Alterado de “Movendo arquivos” → para “Copiando arquivos” (✅ mais preciso tecnicamente).

- 🔧 Pipeline unificado:
  - ✔️ Seleção ou criação de projeto.
  - ✔️ Movimentação dos arquivos.
  - ✔️ Auditoria no PostgreSQL (`storage_audit` e `reception_audit`).
  - ✔️ Feedback em tempo real.

---

## 🚦 **Próxima Etapa Planejada**

- ✔️ Implementar a **limpeza controlada do bucket `recepcao-raw`**, com garantia de que os metadados dos arquivos estejam devidamente registrados na tabela `reception_audit` antes da remoção física dos arquivos.

---

## 🚩 **Observações Importantes para Continuidade (Novo Chat)**

- ✔️ Todo o ambiente está operacional, funcionando, testado e validado.
- ✔️ A estrutura de dados (buckets e tabelas) está alinhada.
- ✔️ O pipeline está funcionando de acordo com os requisitos definidos neste chat.
- ✔️ O próximo chat deve considerar este estado como **o ponto de partida.**
- ✔️ Este documento garante a rastreabilidade técnica e de decisões, servindo como base para retomada de atividades sem perda de contexto.

---

## 📜 **Fim do Documento**
