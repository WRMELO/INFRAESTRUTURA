# 🧠 Relatório Técnico de Evolução — Projeto de Curadoria Numérica
📅 Gerado em: 2025-06-01 17:09:36

---

## 1. Onde Iniciamos

O projeto teve origem a partir da infraestrutura já consolidada para curadoria de imagens técnicas. A partir do sucesso da pipeline de imagens, decidiu-se expandir a arquitetura para tratar **dados numéricos estruturados** provenientes de fontes tabulares (como `.csv`, `.xlsx`, `.parquet`), com o objetivo de aplicar diferentes processos analíticos (ML, DL, RL, BI, etc.).

---

## 2. Filosofia e Escopo Naquele Momento

A estrutura da curadoria numérica seguiu a **filosofia modular, auditável e reversível**, já aplicada na curadoria de imagens:
- Uso de buckets separados por estágio (`storage-unique`, `staging-unique`, `curated-unique`);
- Registro completo em tabelas de auditoria no PostgreSQL;
- Processo dividido entre curadoria leve e curadoria pesada;
- Interface interativa via Jupyter com widgets, barras de progresso e rastreabilidade visual.

---

## 3. Como Caminhamos

As etapas foram estruturadas seguindo os seguintes notebooks e scripts:
- `a-recepcao-raw.ipynb` (adaptado): ingestão bruta de arquivos numéricos do Google Drive.
- `b-storage-movimentacao-unico.ipynb`: hash, unicidade e separação técnica dos dados em `storage-unique`.
- `curadoria_numerico.ipynb` (início em junho/2025):
  - Widgets para seleção de projeto e destino analítico;
  - Leitura e validação automática com pandas;
  - Criação de buckets e tabelas de teste (`staging-teste`, `curated-teste`, `*_audit_teste`);
  - Execução da curadoria leve com 100% de sucesso sobre 8 arquivos reais.

---

## 4. Dificuldades Enfrentadas

- ❌ Erros por falta de importações (`os`, `Path`) nas primeiras execuções;
- ❌ Uso conflituoso de buckets (`recepcao-raw` vs `reception-raw`);
- ⚠️ Erros silenciosos de `CheckViolation` no PostgreSQL devido a `curation_status` fora do domínio permitido;
- ❌ Curadoria pesada ainda inexistente para arquivos numéricos;
- ❗ Inexistência de separação entre curadoria por tipo de análise final (ML, RL, etc.).

---

## 5. Como Resolvemos

- ✅ Refatoração total da célula de curadoria leve com leitura robusta, tratamento de erro, validação de colunas;
- ✅ Introdução da variável `prefix_dropdown` e interface reusável por projeto;
- ✅ Criação formal das tabelas `staging_audit_teste` e `curation_audit_teste`;
- ✅ Definição consensual de que os testes devem ocorrer em buckets `*-teste` para garantir reversibilidade;
- ✅ Introdução de uma taxonomia analítica com 9 categorias de curadoria pesada.

---

## 6. Avanços Conquistados

- ✅ Execução da curadoria leve com 100% de aprovação sobre arquivos reais;
- ✅ Auditoria populada e bucket `staging-teste` corretamente alimentado;
- ✅ Framework técnico para criação de curadorias pesadas personalizadas por destino final;
- ✅ Estrutura de widgets interativos reaproveitada da curadoria de imagens;
- ✅ Plano unificado de curadoria numérica com versionamento.

---

## 7. Ponto Exato em Que Estamos Agora

| Etapa                      | Status              |
|---------------------------|---------------------|
| Curadoria leve numérica   | ✅ funcional         |
| staging-teste preenchido  | ✅ com 8 arquivos    |
| staging_audit_teste       | ✅ populada          |
| curadoria pesada          | ❌ ainda não iniciada |
| integração com destino (ML, DL, RL, BI) | ❌ não implementado |

---

## 8. Filosofia e Escopo Atual

A estratégia atual é:

- Evitar qualquer operação destrutiva sobre buckets e tabelas oficiais;
- Garantir rastreabilidade por meio de ambientes de teste auditáveis;
- Implementar curadorias pesadas ramificadas de acordo com o **tipo de processo analítico final**;
- Utilizar `curation_type = "numerico"` e `curation_status` conforme constraints do banco.

---

## 9. Sugestões para os Próximos Passos

1. ✅ Finalizar a célula de **curadoria pesada numérica**, com validação estatística e filtros configuráveis;
2. ✅ Criar auditoria em `curation_audit_teste`, com diagnóstico técnico salvo em JSON;
3. ✅ Substituir os buckets `*-teste` pelos reais (`staging-unique`, `curated-unique`) após validação;
4. ✅ Implementar lógica condicional por tipo de análise (ML, DL, RL, BI...);
5. ✅ Consolidar versão final do notebook `curadoria_numerico.ipynb`, com código limpo e comentado;
6. ❓ (Opcional) Implementar painel de visualização de distribuição de dados para apoiar filtros técnicos.

---

