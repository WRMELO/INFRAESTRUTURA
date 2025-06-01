# 🧠 Relatório de Evolução — Curadoria de Imagens Técnicas
**Data:** 2025-05-31 21:25:45

---

## 1. Onde iniciamos

Iniciamos o projeto com uma estrutura de curadoria clássica dividida em duas etapas: curadoria leve e curadoria pesada. Os dados estavam armazenados em buckets MinIO no estágio `staging-unique`, sendo processados via notebook Jupyter rodando dentro de um container Docker. O objetivo era realizar a triagem e validação técnica das imagens para uso em pipelines de Deep Learning (DL) e Reinforcement Learning (RL), em especial no ambiente do Google Colab com GPU T4.

---

## 2. Filosofia e escopo naquele momento

- Manter a separação clara entre as etapas leve (validação mínima) e pesada (validação técnica rigorosa)
- Operar com banco PostgreSQL como repositório de auditoria (`staging_audit`, `curation_audit`)
- Garantir auditabilidade total via tabelas com campos controlados
- Não repetir processamento para arquivos já auditados
- Rejeitar silenciosamente apenas imagens inválidas de fato (não decodificáveis)
- Preparar o dataset para pipelines compatíveis com GPU Colab

---

## 3. Como caminhamos

- Criamos e testamos os notebooks `curadoria_imagens.ipynb` e `c-curadoria.ipynb`
- Construímos a célula final da curadoria leve, com validação de imagem via `PIL`
- Implementamos critérios técnicos na curadoria pesada com base em resolução, aspecto, tamanho, canais e variância
- Descobrimos que as imagens eram uniformemente 100x333, monocanal, com aspect ratio baixo
- Adicionamos mecanismo de diagnóstico automatizado antes da curadoria pesada
- Incorporamos widgets interativos para definir os parâmetros técnicos antes da execução
- Garantimos compatibilidade com a tabela real `curation_audit` com todos os campos obrigatórios

---

## 4. Dificuldades enfrentadas

- Mismatch entre os campos definidos e os realmente existentes nas tabelas de auditoria
- Constraint SQL do `curation_status` que aceitava apenas dois valores (`processed`, `not_processed`)
- Rejeição de 100% das imagens por critérios rígidos demais (aspect ratio < 0.5, resolução ≥ 224x224)
- Lentidão ao processar 25 mil imagens sem diagnóstico prévio
- Repetição de registros `staging_audit` ao rodar curadorias múltiplas sem reset

---

## 5. Como resolvemos

- Alinhamos os campos obrigatórios via reflexão com SQLAlchemy
- Padronizamos os valores de `curation_status = 'processed'` mesmo para rejeitados
- Ajustamos os critérios técnicos para refletir a realidade das imagens FIAP (100x333, modo `L`)
- Criamos célula de diagnóstico que calcula: resolução, aspect ratio, tamanho, canal, variância
- Adicionamos histograma e widgets com sugestões baseadas em percentis reais dos dados

---

## 6. Avanços conquistados

- Pipeline auditável e controlado com curadoria leve e pesada funcionando
- Célula de diagnóstico robusta com visualização e sugestão de parâmetros
- Registro confiável em `curation_audit` com campos `curation_details` e `bucket_curated`
- Processamento seguro por tipo de curadoria (`DL`, `RL`) com controle via widgets
- Infraestrutura MinIO e PostgreSQL validada para armazenamento e rastreio

---

## 7. Ponto exato em que estamos agora

✅ 100% funcional:
- Diagnóstico técnico e visual completo
- Geração de parâmetros com `crit_params` para curadoria pesada
- Widgets interativos para controle fino
- Auditoria final completa e compatível

🧪 Em finalização:
- Aplicação dos `crit_params` diretamente na célula de curadoria pesada

---

## 8. Filosofia e escopo atual

Adotamos um modelo adaptativo baseado em **diagnóstico exploratório técnico dos dados reais**. Abandonamos a estratégia rígida de parâmetros fixos para diferentes projetos. A curadoria agora é **guiada estatisticamente**, com participação ativa do usuário via widgets após diagnóstico.

---

## 9. Sugestões para os próximos passos

1. Aplicar o `crit_params` definido interativamente na célula da curadoria pesada.
2. Armazenar os critérios usados na auditoria (`curation_details`) como JSON serializado.
3. Gerar relatórios automáticos com percentuais de aprovação/rejeição por projeto.
4. Criar célula para exportação estruturada de imagens aprovadas para Colab.
5. Opcionalmente criar uma terceira etapa de curadoria semiautomática (interface de validação visual).

---

**Relatório gerado automaticamente via assistente técnico no notebook curadoria_imagens.ipynb**.
