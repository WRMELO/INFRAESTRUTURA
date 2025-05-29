# Fundamentos da Estratégia de EDA e Pré-Tratamento

##  Repositório: `WRMELO/INFRAESTRUTURA`

Este repositório serve como a espinha dorsal da infraestrutura do projeto, organizando de forma modular e documentada os componentes necessários para ingestão, armazenamento e preparação de dados.

---

## Estrutura de Diretórios

- **`notebooks/`**: Contém os notebooks Jupyter responsáveis pelas etapas de ingestão e movimentação de dados.
    
    - `a-recepcao-raw.ipynb`: Notebook que realiza a cópia dos arquivos do Google Drive para o bucket MinIO `recepcao-raw` e registra auditorias na tabela `reception_audit`.
        
    - `b-storage-movimentacao-unico.ipynb`: Notebook que assegura a unicidade dos arquivos e projetos, atualizando as tabelas `projetos` e `arquivos`.
        
- **`cofre/`**: Armazena documentos de referência e planejamento.
    
    - `HUB_INFRAESTRUTURA.md`: Documento central que resume a infraestrutura do projeto, incluindo detalhes sobre os serviços Docker utilizados, estrutura de buckets e tabelas, e decisões técnicas tomadas.
        
- **`docker/`**: Contém arquivos de configuração para orquestração dos serviços Docker, como MinIO, PostgreSQL e Jupyter.
    

---

## Componentes Técnicos Principais

- **MinIO**: Serviço de armazenamento de objetos utilizado para armazenar os arquivos recebidos e processados.
    
- **PostgreSQL**: Banco de dados relacional utilizado para armazenar metadados e informações de auditoria dos arquivos.
    
- **Jupyter**: Ambiente interativo para desenvolvimento e execução dos notebooks de processamento de dados.
    

---

## Tabelas de Auditoria e Controle

- **`reception_audit`**: Tabela que registra informações sobre os arquivos recebidos, como nome, caminho, tamanho, checksum, data de recebimento, fonte, status de processamento e mensagens de erro, se houver.
    
- **`projetos`**: Tabela que mantém a unicidade dos projetos, evitando duplicações.
    
- **`arquivos`**: Tabela que mantém a unicidade dos arquivos, assegurando que cada arquivo seja processado uma única vez.
    

---

## Fluxo de Dados

1. **Ingestão**: Arquivos são copiados do Google Drive para o bucket MinIO `recepcao-raw` utilizando o notebook `a-recepcao-raw.ipynb`.
    
2. **Auditoria**: Informações sobre os arquivos recebidos são registradas na tabela `reception_audit`.
    
3. **Movimentação**: O notebook `b-storage-movimentacao-unico.ipynb` processa os arquivos, garantindo a unicidade e atualizando as tabelas `projetos` e `arquivos`.
    
4. **Armazenamento**: Arquivos curados são armazenados em buckets específicos, mantendo o nome original completo para facilitar a identificação e rastreamento.
    

---

Este documento serve como base para compreender a infraestrutura atual do projeto e orientar as próximas etapas de desenvolvimento, incluindo a implementação de estratégias de EDA e pré-tratamento de dados.

---