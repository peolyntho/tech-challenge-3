# Registro de Decisões Técnicas e Analíticas

Este documento registra as principais decisões tomadas durante o desenvolvimento do Tech Challenge da Fase 3.

O objetivo é manter a rastreabilidade das escolhas relacionadas aos dados, preparação, modelagem, avaliação e interpretação dos resultados.

As decisões serão registradas conforme o projeto evoluir, evitando justificativas construídas apenas ao final do trabalho.

---

## DEC-001 — Separação do projeto da Fase 3

**Status:** Aprovada

**Contexto:**
O Tech Challenge da Fase 3 dá continuidade ao trabalho desenvolvido na Fase 2, porém possui foco diferente. Enquanto a etapa anterior concentrou-se na construção e organização da arquitetura de dados, a nova fase tem como foco análise exploratória, Machine Learning, avaliação, otimização e interpretação dos modelos.

**Decisão:**
Criar um novo repositório denominado `tech-challenge-fase3`, mantendo o repositório da Fase 2 preservado.

**Justificativa:**
A separação permite manter o histórico da solução de Engenharia de Dados da Fase 2 e organizar a nova etapa de Ciência de Dados e Machine Learning de maneira independente.

**Impacto:**
Os dados tratados e integrados na Fase 2 serão utilizados como fonte para o desenvolvimento da Fase 3, sem misturar as responsabilidades dos dois projetos.

---

## DEC-002 — Utilização dos dados da Fase 2 como ponto de partida

**Status:** Em análise

**Contexto:**
O Tech Challenge orienta a utilização dos dados tratados na etapa anterior como base para o desenvolvimento das análises e modelos da Fase 3.

**Decisão:**
A definição do dataset de modelagem será realizada somente após uma auditoria das bases produzidas na Fase 2.

**Justificativa:**
Antes de definir features, target ou algoritmos, é necessário confirmar:

* granularidade dos dados;
* unidade de análise;
* período disponível;
* qualidade dos registros;
* variáveis disponíveis;
* existência de informações individuais ou agregadas;
* possibilidade de construção da variável-alvo;
* possíveis riscos de data leakage.

**Impacto:**
Nenhum modelo será treinado antes da conclusão da auditoria dos dados.

---

## DEC-003 — Estratégia de desenvolvimento

**Status:** Aprovada

**Contexto:**
Projetos de Machine Learning podem concentrar preparação, exploração e modelagem em notebooks extensos, dificultando manutenção e reprodutibilidade.

**Decisão:**
Utilizar notebooks para exploração, análise e experimentação, mantendo código reutilizável e consolidado dentro de `src/`.

**Estrutura:**

* `notebooks/`: exploração e experimentos;
* `src/preprocessing/`: preparação e transformação dos dados;
* `src/modeling/`: treinamento e otimização;
* `src/evaluation/`: avaliação e métricas;
* `src/visualization/`: visualizações reutilizáveis;
* `reports/`: documentação técnica e decisões;
* `images/`: gráficos utilizados na documentação.

**Justificativa:**
Essa separação melhora organização, legibilidade, reutilização e reprodutibilidade.

---

## DEC-004 — Prevenção de data leakage

**Status:** Diretriz aprovada

**Contexto:**
O Tech Challenge exige atenção explícita ao risco de data leakage durante preparação, seleção de variáveis e modelagem.

**Decisão:**
Toda variável candidata à modelagem será avaliada quanto ao risco de utilizar informações que não estariam disponíveis no momento real da previsão ou que sejam derivadas direta ou indiretamente da variável-alvo.

As transformações aprendidas a partir dos dados deverão ser ajustadas apenas sobre os dados de treinamento.

**Justificativa:**
Data leakage pode produzir métricas artificialmente elevadas e comprometer a capacidade de generalização do modelo.

**Impacto:**
Durante a auditoria será criado um dicionário classificando as variáveis, quando aplicável, em:

* variável-alvo;
* identificador;
* feature candidata;
* feature suspeita;
* leakage;
* variável não utilizada.

---

## DEC-005 — Uso de Pipeline para preparação e modelagem

**Status:** Diretriz aprovada

**Contexto:**
O projeto poderá exigir diferentes tratamentos para variáveis numéricas e categóricas, além de imputação, encoding, scaling e outras transformações.

**Decisão:**
Priorizar `Pipeline` e `ColumnTransformer` do Scikit-learn para integrar preprocessing e modelagem.

**Justificativa:**
Essa estratégia:

* reduz risco de data leakage;
* garante aplicação consistente das transformações;
* facilita validação cruzada;
* facilita otimização de hiperparâmetros;
* melhora a reprodutibilidade.

**Impacto:**
As transformações definitivas não serão realizadas manualmente sobre todo o dataset antes da separação entre treino e teste.

---

# Decisões pendentes

As decisões abaixo serão preenchidas conforme avançarmos no projeto.

## DEC-006 — Definição da unidade de análise e variável-alvo

**Status:** Pendente

A definir após auditoria dos dados.

---

## DEC-007 — Estratégia de separação entre treino e teste

**Status:** Pendente

A definir após análise da estrutura, período e distribuição da variável-alvo.

---

## DEC-008 — Métrica principal de avaliação

**Status:** Pendente

A definir após análise da distribuição das classes e do impacto dos diferentes tipos de erro.

---

## DEC-009 — Algoritmos candidatos

**Status:** Pendente

A definir após EDA e construção do baseline.

---

## DEC-010 — Estratégia de validação cruzada

**Status:** Pendente

A definir considerando estrutura e distribuição dos dados.

---

## DEC-011 — Estratégia de otimização de hiperparâmetros

**Status:** Pendente

A definir após avaliação inicial dos modelos candidatos.

---

## DEC-012 — Seleção do modelo final

**Status:** Pendente

A decisão deverá considerar desempenho, generalização, estabilidade e interpretabilidade.

---

## DEC-013 — Estratégia de interpretabilidade

**Status:** Pendente

A definir de acordo com o modelo final, considerando Feature Importance e/ou SHAP.

---

## DEC-014 — Análises complementares

**Status:** Pendente

Será avaliada a viabilidade e utilidade de análises complementares, como:

* agrupamento de municípios ou regiões;
* identificação de perfis semelhantes;
* análise temporal;
* avaliação de risco de não atingimento de metas futuras.

A utilização dessas técnicas dependerá da estrutura e qualidade dos dados disponíveis.
