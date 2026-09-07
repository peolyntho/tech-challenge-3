# Tech Challenge - Fase 3

## Predição e Inteligência Analítica para Alfabetização no Brasil

Projeto desenvolvido durante a **Fase 3 da Pós-Tech Data & AI Scientist**, com foco na aplicação de técnicas de Machine Learning para predição da alfabetização individual a partir de dados educacionais, territoriais e socioeconômicos.

> **Status:** Em desenvolvimento — preparação dos dados e Análise Exploratória de Dados (EDA) concluídas. Modelagem supervisionada em desenvolvimento.

---

## Sobre o projeto

Este projeto dá continuidade ao pipeline de Engenharia de Dados desenvolvido durante o **Tech Challenge da Fase 2**.

Na etapa anterior foram construídas pipelines para ingestão, tratamento, integração e disponibilização dos dados em diferentes camadas, incluindo a **camada Gold**, utilizada agora como principal fonte de features analíticas para a modelagem.

O objetivo da Fase 3 é transformar os dados tratados anteriormente em uma solução de **Machine Learning supervisionado**, capaz de estimar a probabilidade de um aluno ser classificado como alfabetizado.

Além da capacidade preditiva, o projeto busca gerar inteligência analítica sobre fatores educacionais, territoriais e socioeconômicos associados à alfabetização.

---

## Objetivo analítico

O problema foi estruturado como uma tarefa de **classificação binária supervisionada**.

A unidade de análise corresponde ao **aluno avaliado em 2024**.

A variável-alvo utilizada é:

- `0`: não alfabetizado;
- `1`: alfabetizado.

O objetivo do modelo é estimar a condição de alfabetização individual utilizando informações históricas e contextuais disponíveis sem utilizar o resultado contemporâneo da avaliação do próprio aluno.

A hipótese central é que a combinação entre:

- histórico educacional do município e da rede;
- contexto territorial;
- indicadores socioeconômicos;
- metas educacionais;

contém informação relevante para estimar a probabilidade de alfabetização individual.

---

## Arquitetura e origem dos dados

A Fase 3 reutiliza os dados tratados e integrados durante o **Tech Challenge da Fase 2**.

Na Fase 2, os dados originais foram obtidos principalmente por meio da **Base dos Dados / Google BigQuery**, processados pelo pipeline de Engenharia de Dados e posteriormente disponibilizados em diferentes camadas.

Para a Fase 3, as **features educacionais, territoriais e socioeconômicas utilizadas na modelagem são provenientes da camada Gold desenvolvida na Fase 2**, armazenada no Amazon S3.

As principais tabelas Gold utilizadas são:

- `indicador_alfabetizacao_municipio`;
- `comparativo_metas_resultados`;
- `evolucao_temporal_indicador`;
- `desempenho_alunos_municipio`.

Essas tabelas foram auditadas quanto à:

- granularidade;
- cobertura;
- temporalidade;
- consistência das chaves;
- valores ausentes;
- redundância entre indicadores;
- disponibilidade de informações territoriais e socioeconômicas.

A integração dessas fontes resultou em uma camada consolidada de features históricas utilizada na construção do dataset de modelagem.

---

## Estratégia temporal

O target corresponde à classificação individual observada em **2024**.

Para reduzir o risco de **data leakage**, os principais indicadores educacionais utilizados como preditores representam informações históricas referentes a **2023**.

Entre eles estão:

- taxa de alfabetização do município/rede em 2023;
- média de Português em 2023;
- percentual de participação em 2023;
- total de alunos no contexto município/rede;
- percentual histórico de alfabetizados;
- proficiência média ponderada;
- indicadores socioeconômicos;
- metas educacionais disponíveis para 2024.

Variáveis contemporâneas derivadas diretamente do desempenho observado dos alunos em 2024 não são utilizadas como preditores.

---

## Dataset de modelagem

O dataset final possui granularidade individual e contém:

- **1.851.828 alunos**;
- **24 colunas**;
- ausência de duplicidades em `id_aluno`;
- ausência de valores nulos na variável-alvo.

A distribuição da variável-alvo é aproximadamente:

- **59,8% alfabetizados**;
- **40,2% não alfabetizados**.

A população analisada está distribuída entre:

- **86,98% rede Municipal**;
- **13,02% rede Estadual**.

A integração com o contexto histórico da camada Gold apresentou cobertura de aproximadamente **98,08% dos alunos**.

O dataset materializado localmente é armazenado em:

```text
data/processed/modeling_dataset_2024_gold.parquet
```

O arquivo não é versionado no GitHub por representar um artefato derivado de grande volume que pode ser reproduzido a partir do pipeline do projeto.

O contrato e as regras de validação estão em
[Definição do dataset Gold](reports/modeling_dataset_definition.md).
Para validar o parquet já disponível localmente, sem acessar as fontes:

```bash
python -m src.preprocessing.validate_dataset
```

Os testes sintéticos independem de credenciais e do parquet:

```bash
python -m tests.test_dataset_contract
```


---

## Features disponíveis

As features candidatas à modelagem incluem diferentes dimensões.

### Contexto educacional histórico

- `taxa_alfabetizacao_municipio_2023`;
- `media_portugues_municipio_2023`;
- `percentual_participacao_municipio_2023`;
- `total_alunos_municipio_2023`;
- `pct_alfabetizados_municipio_2023`;
- `proficiencia_media_ponderada_2023`.

### Metas educacionais

- `meta_alfabetizacao_municipio_2024`;
- `gap_para_meta_municipio_2024`;
- `atingiu_meta_municipio_2024`.

### Contexto territorial

- `rede`;
- `sigla_uf`.

### Contexto socioeconômico

- `idhm`;
- `idhm_educacao`;
- `idhm_renda`;
- `idhm_longevidade`.

### Variáveis auxiliares

Identificadores como `id_aluno`, `id_escola`, `id_municipio` e nomes geográficos são preservados para rastreabilidade e análises, mas não serão utilizados diretamente como features preditivas.

A variável `peso_aluno`, relacionada à ponderação amostral, também não será utilizada inicialmente como feature. Seu possível uso como `sample_weight` será avaliado durante a modelagem.

---

## Análise Exploratória de Dados

A EDA foi realizada no notebook:

```text
notebooks/01_eda.ipynb
```

A análise contemplou:

1. visão geral e granularidade do dataset;
2. qualidade dos dados;
3. análise da variável-alvo;
4. distribuições das variáveis numéricas;
5. análise das variáveis categóricas;
6. investigação de outliers;
7. relações entre features e target;
8. análise territorial;
9. correlações e redundância;
10. auditoria de data leakage;
11. definição das hipóteses para modelagem.

---

## Principais resultados da EDA

### Histórico educacional

Os indicadores educacionais históricos apresentaram as associações mais relevantes com a classificação individual observada em 2024.

A taxa histórica de alfabetização do município/rede apresentou diferença média de aproximadamente **7,8 pontos percentuais** entre os contextos associados a alunos alfabetizados e não alfabetizados.

Também foram observadas diferenças relevantes nas medidas históricas de proficiência e percentual de alfabetizados.

### Relação temporal

A segmentação dos alunos em quintis de acordo com a taxa de alfabetização do município/rede em 2023 revelou uma relação monotônica com o resultado individual observado em 2024.

A proporção de alunos alfabetizados evoluiu aproximadamente de:

- **42,6%** no menor quintil histórico;
- **54,7%** no segundo quintil;
- **59,8%** no terceiro quintil;
- **65,1%** no quarto quintil;
- **77,1%** no maior quintil histórico.

A diferença entre os extremos é de aproximadamente **34,5 pontos percentuais**.

Esse resultado reforça a hipótese de que o contexto educacional histórico contém sinal preditivo relevante.

### Contexto territorial

Foram observadas diferenças expressivas na proporção de alunos classificados como alfabetizados entre as UFs presentes no dataset.

Essas diferenças representam exclusivamente a população analisada e **não devem ser interpretadas como indicadores oficiais das taxas estaduais de alfabetização**.

Os resultados sugerem que o contexto territorial pode contribuir para a capacidade preditiva quando combinado com fatores educacionais e socioeconômicos.

### Contexto socioeconômico

Os indicadores de IDHM apresentaram associações individuais mais moderadas com o target.

Como essas informações possuem granularidade estadual, os mesmos valores são compartilhados por grande número de alunos. Sua contribuição será avaliada principalmente em combinação com as demais características do dataset.

---

## Valores ausentes

Os valores ausentes foram preservados durante a construção do dataset.

As principais taxas observadas foram:

- aproximadamente **1,92%** de ausência no contexto histórico principal;
- aproximadamente **4,70%** em algumas informações relacionadas à participação e metas;
- aproximadamente **23,18%** em algumas features provenientes do desempenho agregado.

Nenhuma imputação foi realizada durante a EDA.

O tratamento será realizado diretamente no **pipeline de Machine Learning**, permitindo que os parâmetros de imputação sejam aprendidos exclusivamente a partir do conjunto de treinamento e evitando vazamento de informações entre treino, validação e teste.

---

## Outliers

A EDA identificou forte assimetria principalmente em:

- `peso_aluno`;
- `total_alunos_municipio_2023`.

A investigação mostrou que os maiores valores de `total_alunos_municipio_2023` estão associados a grandes redes de ensino, representando diferenças reais de escala e não erros nos dados.

Os valores extremos de `peso_aluno` também foram preservados.

Nenhuma remoção automática de outliers foi realizada.

---

## Correlação e redundância

A análise identificou forte correlação entre algumas features.

Os principais casos encontrados foram:

- `media_portugues_municipio_2023` × `proficiencia_media_ponderada_2023`: aproximadamente **0,999**;
- `taxa_alfabetizacao_municipio_2023` × `pct_alfabetizados_municipio_2023`: aproximadamente **0,971**;
- `idhm` × `idhm_renda`: aproximadamente **0,957**;
- `idhm` × `idhm_educacao`: aproximadamente **0,926**.

A seleção final das features será avaliada de acordo com o algoritmo utilizado, desempenho, capacidade de generalização e interpretabilidade.

---

## Prevenção de data leakage

A temporalidade das features foi auditada antes da modelagem.

Foi confirmado que as principais features educacionais utilizadas representam informações históricas de 2023 ou informações contextuais disponíveis independentemente do resultado individual observado em 2024.

Também foi validado que:

```text
gap_para_meta_municipio_2024
=
meta_alfabetizacao_municipio_2024
-
taxa_alfabetizacao_municipio_2023
```

e que:

```text
atingiu_meta_municipio_2024
=
taxa_alfabetizacao_municipio_2023
>=
meta_alfabetizacao_municipio_2024
```

A validação apresentou correspondência de **100%** para a condição de atingimento da meta.

Dessa forma, essas variáveis não utilizam o resultado individual observado em 2024. Entretanto, por serem derivadas de outras features, sua redundância será considerada durante a seleção de variáveis.

---

## Metodologia

O desenvolvimento do projeto está organizado nas seguintes etapas:

1. auditoria e entendimento dos dados;
2. validação da camada Gold da Fase 2;
3. consolidação das features históricas;
4. construção do dataset individual de modelagem;
5. Análise Exploratória de Dados;
6. análise e prevenção de data leakage;
7. definição das features candidatas;
8. separação dos conjuntos de treino, validação e teste;
9. construção do pipeline de pré-processamento;
10. desenvolvimento do modelo baseline;
11. treinamento e comparação de modelos supervisionados;
12. validação e otimização de hiperparâmetros;
13. avaliação de generalização e overfitting;
14. seleção do modelo final;
15. interpretabilidade e explicabilidade;
16. geração de insights analíticos;
17. discussão de aplicações em políticas públicas.

---

## Status do projeto

### Concluído

- [x] Estruturação inicial do repositório
- [x] Auditoria das fontes da Fase 2
- [x] Recuperação das tabelas Gold
- [x] Validação de granularidade e cobertura
- [x] Validação da temporalidade dos dados
- [x] Consolidação das features Gold
- [x] Integração com a população individual de 2024
- [x] Construção do dataset de modelagem
- [x] Análise Exploratória de Dados
- [x] Análise de valores ausentes
- [x] Análise de outliers
- [x] Análise territorial
- [x] Análise socioeconômica
- [x] Análise das relações entre features e target
- [x] Análise de correlações e redundância
- [x] Auditoria de data leakage
- [x] Definição das hipóteses iniciais de modelagem

### Em desenvolvimento

- [ ] Estratégia de separação treino/validação/teste
- [ ] Pipeline de pré-processamento
- [ ] Modelo baseline
- [ ] Comparação de modelos supervisionados
- [ ] Otimização de hiperparâmetros
- [ ] Avaliação de generalização e overfitting
- [ ] Seleção do modelo final
- [ ] Interpretabilidade e explicabilidade
- [ ] Feature Importance / SHAP
- [ ] Insights orientados às perguntas de negócio
- [ ] Documentação técnica final
- [ ] Apresentação e vídeo executivo

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
│   ├── 00_test_build_modeling_dataset.ipynb
│   ├── 00_test_gold_integration.ipynb
│   └── 01_eda.ipynb
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

- `data/`: artefatos de dados utilizados durante o desenvolvimento;
- `notebooks/`: auditorias, análises exploratórias e experimentos;
- `src/preprocessing/`: leitura, integração, preparação e transformação dos dados;
- `src/modeling/`: treinamento, pipelines e otimização dos modelos;
- `src/evaluation/`: métricas e avaliação;
- `src/visualization/`: funções e recursos de visualização;
- `reports/`: documentação técnica, decisões analíticas e resultados;
- `images/`: gráficos e imagens utilizados na documentação.

---

## Modelagem

A etapa de modelagem será estruturada como um problema de classificação binária supervisionada.

O pré-processamento será incorporado diretamente ao pipeline de Machine Learning, incluindo:

- imputação de valores numéricos ausentes;
- tratamento das variáveis categóricas;
- encoding;
- eventuais transformações numéricas;
- seleção de features;
- treinamento do estimador.

Serão avaliados modelos baseline e algoritmos supervisionados mais robustos, com comparação baseada em desempenho, capacidade de generalização e interpretabilidade.

A estratégia completa será documentada conforme os experimentos forem executados.

---

## Avaliação

Os dados serão separados em conjuntos independentes de treinamento, validação e teste.

As métricas serão selecionadas considerando a natureza do problema de classificação e o impacto dos diferentes tipos de erro.

Além do desempenho global, serão avaliados:

- capacidade de generalização;
- diferença entre treino e validação;
- possíveis sinais de overfitting;
- desempenho por classe;
- matriz de confusão;
- estabilidade das previsões.

As métricas definitivas serão documentadas durante a etapa de modelagem.

---

## Interpretabilidade

Após a seleção do modelo final, serão utilizadas técnicas de interpretabilidade para compreender os fatores mais relevantes nas previsões.

Entre as técnicas previstas estão:

- Feature Importance;
- análise de importância das variáveis;
- SHAP, quando compatível com o modelo selecionado.

A interpretação será utilizada tanto para compreensão técnica do modelo quanto para geração de insights relacionados ao problema educacional.

---

## Insights e aplicação em políticas públicas

Os resultados serão analisados sob a perspectiva de apoio à tomada de decisão.

Entre as questões que serão investigadas estão:

- quais fatores apresentam maior associação com alfabetização;
- quais contextos territoriais apresentam maior risco;
- quais municípios ou regiões possuem características semelhantes;
- quais fatores mais influenciam as previsões;
- quais contextos apresentam maior risco de não atingir metas educacionais.

Os resultados serão apresentados como suporte analítico e não como evidência causal.

---

## Limitações

Algumas limitações já identificadas incluem:

- parte das features possui granularidade municipal/rede ou estadual, enquanto o target possui granularidade individual;
- alguns indicadores apresentam valores ausentes;
- os indicadores socioeconômicos disponíveis atualmente possuem granularidade estadual;
- algumas features educacionais apresentam forte correlação entre si;
- associações encontradas não representam necessariamente relações causais;
- a capacidade de generalização dependerá da estratégia de validação e da representatividade dos dados disponíveis.

Novas limitações serão documentadas conforme a modelagem avançar.

---

## Reprodutibilidade

O projeto foi estruturado para permitir reprodução das principais etapas por meio dos scripts e notebooks versionados no repositório.

Os arquivos derivados de grande volume, incluindo o dataset final de modelagem, não são versionados diretamente no GitHub.

Para reproduzir o projeto é necessário:

1. Python compatível com o ambiente do projeto;
2. dependências instaladas a partir de `requirements.txt`;
3. acesso autorizado às fontes de dados necessárias;
4. configuração das credenciais por meio de variáveis de ambiente;
5. execução das etapas de integração e preparação descritas no projeto.

Credenciais e arquivos `.env` **não devem ser versionados no repositório**.

As instruções de reprodução serão refinadas conforme a pipeline de modelagem for consolidada.

---

## Evoluções futuras

Possíveis extensões incluem:

- enriquecimento com novas variáveis socioeconômicas e territoriais;
- incorporação de indicadores em granularidades mais detalhadas;
- avaliação temporal com novos ciclos da avaliação;
- monitoramento de drift;
- criação de pipelines automatizados de treinamento e inferência;
- disponibilização das previsões por meio de aplicações analíticas;
- expansão das análises voltadas à identificação de regiões e grupos prioritários.

---

## Tecnologias

O projeto utiliza principalmente:

- Python;
- Pandas;
- NumPy;
- Scikit-learn;
- Jupyter Notebook;
- Parquet;
- Amazon S3;
- Google BigQuery;
- Git;
- GitHub.

Outras bibliotecas serão incorporadas conforme as etapas de modelagem, otimização e interpretabilidade forem desenvolvidas.