# Tech Challenge - Fase 3

## Predição e Inteligência Analítica para Alfabetização no Brasil

Projeto desenvolvido durante a Fase 3 da Pós-Tech Data & AI Scientist.

## Sobre o projeto

O objetivo deste Tech Challenge é utilizar os dados tratados e integrados durante a Fase 2 para desenvolver análises exploratórias e modelos de Machine Learning aplicados ao problema da alfabetização no Brasil.

A solução será desenvolvida de forma reproduzível, contemplando preparação dos dados, treinamento, validação, otimização, avaliação e interpretação dos modelos.

> **Status:** Em desenvolvimento.

---

## Objetivo analítico

O objetivo principal é desenvolver um modelo supervisionado capaz de prever a condição de alfabetização a partir das informações disponíveis na base de dados.

Durante o desenvolvimento, também serão investigados fatores associados à alfabetização e possibilidades de utilização dos resultados para geração de inteligência analítica.

A definição final da variável-alvo, unidade de análise e features utilizadas será documentada após a auditoria dos dados provenientes da Fase 2.

---

## Origem dos dados

Este projeto dá continuidade ao pipeline de Engenharia de Dados desenvolvido no Tech Challenge da Fase 2.

Os datasets utilizados na modelagem serão definidos após a auditoria da camada Gold e das bases integradas produzidas anteriormente.

---

## Metodologia

O desenvolvimento será organizado nas seguintes etapas:

1. Auditoria e entendimento dos dados;
2. Análise Exploratória de Dados (EDA);
3. Definição da variável-alvo e das features;
4. Identificação e prevenção de data leakage;
5. Preparação e transformação dos dados;
6. Construção da pipeline de Machine Learning;
7. Desenvolvimento de modelos baseline;
8. Treinamento e comparação de modelos;
9. Validação cruzada;
10. Otimização de hiperparâmetros;
11. Avaliação de generalização;
12. Seleção e avaliação do modelo final;
13. Interpretabilidade e explicabilidade;
14. Geração de insights;
15. Discussão de aplicações em políticas públicas.

---

## Estrutura do projeto

```text
tech-challenge-fase3/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── gold/
│
├── notebooks/
│
├── src/
│   ├── preprocessing/
│   ├── modeling/
│   ├── evaluation/
│   └── visualization/
│
├── reports/
├── images/
├── requirements.txt
├── README.md
└── .gitignore
```

### Diretórios

* `data/`: dados utilizados durante o desenvolvimento;
* `notebooks/`: análises exploratórias e experimentos;
* `src/preprocessing/`: processamento e transformação dos dados;
* `src/modeling/`: treinamento e otimização dos modelos;
* `src/evaluation/`: métricas e avaliação;
* `src/visualization/`: funções e recursos de visualização;
* `reports/`: documentação técnica, decisões analíticas e resultados;
* `images/`: gráficos e imagens utilizados na documentação.

---

## Modelagem

Esta seção será atualizada durante o desenvolvimento com:

* definição do problema de Machine Learning;
* variável-alvo;
* features selecionadas;
* estratégias de preprocessing;
* algoritmos avaliados;
* estratégia de validação;
* otimização de hiperparâmetros;
* modelo selecionado.

---

## Avaliação

As métricas serão definidas de acordo com a distribuição das classes e o impacto dos diferentes tipos de erro no contexto educacional.

Os resultados de treinamento, validação e teste serão documentados nesta seção.

---

## Interpretabilidade

Serão utilizadas técnicas de interpretabilidade para compreender a influência das variáveis nas previsões do modelo.

As técnicas e resultados serão documentados após a seleção do modelo final.

---

## Insights e aplicação em políticas públicas

Os resultados serão analisados sob a perspectiva de apoio à tomada de decisão e identificação de fatores associados à alfabetização.

Esta seção será construída a partir das evidências encontradas durante a análise e modelagem.

---

## Limitações

As limitações relacionadas aos dados, metodologia e capacidade de generalização dos modelos serão registradas durante o desenvolvimento.

---

## Reprodutibilidade

As instruções completas para instalação das dependências e execução do projeto serão adicionadas após a consolidação do ambiente.

---

## Evoluções futuras

Possíveis extensões e melhorias serão documentadas ao final do projeto.
