## Objetivo do Documento

Este documento descreve uma abordagem estruturada para realização de Análise Exploratória de Dados (EDA) e pré-tratamento dos dados recebidos no projeto atual, inspirado por uma analogia prática de atendimento em restaurante.

---

## Conceitos Fundamentais

Existem duas abordagens principais para organizar a pré-análise e tratamento de dados:

### 1. Padronização Universal (Genérica)

* Consiste em ter um único pipeline pré-definido aplicável a todos os tipos de dados.
* Bom para alta automação e consistência inicial.
* Limitado para explorar insights específicos ou complexos.

### 2. Padronização Condicional (Cardápio)

* Inicia com identificação rápida do tipo de dado ou fonte.
* Aplica posteriormente um conjunto específico e pré-definido de pipelines adaptados ao dado identificado.
* Combina padronização e flexibilidade, garantindo eficiência e capacidade de insights profundos.

---

## Implementação Sugerida: Estrutura do Cardápio

Inspirado pelo exemplo de um serviço de restaurante, onde após a escolha inicial (ex.: peixe, carne ou massa), é apresentado um cardápio específico com opções adequadas de entradas, pratos, sobremesas e bebidas. A implementação técnica desta ideia para EDA e pré-tratamento seria estruturada assim:

### 1. Identificação Inicial dos Dados Recebidos

* Categorize rapidamente por tipo ou formato:

  * Banco de Dados
  * Arquivos Estruturados (CSV, Excel, JSON, Parquet)
  * Documentos (PDF, Word, Markdown)
  * Multimídia (Imagens, Áudio, Vídeo)

### 2. Definição do Cardápio Específico

* Para cada categoria principal identificada, é desenvolvido um conjunto padronizado de tratamentos e análises, exemplificado abaixo:

| Tipo de Dado | Entradas (Pré-processamento)                      | Primeiro Prato (EDA básica)                                            | Segundo Prato (Tratamento Avançado)                    | Sobremesa (Entrega Final)                                                                          | Serviço Complementar                            |
| ------------ | ------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| CSV/Excel    | Remoção de NaNs, colunas vazias, encoding correto | Distribuições, outliers, correlações básicas                           | Feature Engineering, Encoding categórico, Normalização | Dados curados em parquet, CSV padronizado armazenados em bucket(s) mantendo nome original completo | Identificação e documentação das partes do nome |
| Texto/PDF    | OCR, Parsing, Quebra de páginas, limpeza inicial  | Word Cloud, Frequências de termos, extração de entidades               | NLP (lematização, embeddings)                          | Arquivo limpo em JSON estruturado armazenado em bucket(s) mantendo nome original completo          | Identificação e documentação das partes do nome |
| Imagem/Áudio | Redimensionamento, ajuste resolução, metadata     | Histogramas de cores, espectrogramas, identificação inicial de objetos | Normalização de formatos, remoção de ruído             | Arquivos curados em formatos padrão armazenados em bucket(s) mantendo nome original completo       | Identificação e documentação das partes do nome |

### 3. Automação Condicional

* Após a identificação inicial dos dados, cada conjunto segue automaticamente para o pipeline adaptado à categoria específica previamente definida.

---

Este documento estabelece uma estrutura conceitual sólida e clara para garantir eficiência, clareza e flexibilidade no tratamento inicial e exploração analítica dos dados do projeto.
