# Auditoria de Dados e Contrato do Dataset de Modelagem

## 1. Objetivo

Esta etapa tem como objetivo avaliar a adequação dos dados produzidos na
Fase 2 para utilização em modelos de Machine Learning na Fase 3.

A auditoria não substitui os tratamentos realizados nas camadas Silver e
Gold. Seu objetivo é identificar características específicas do processo
de modelagem, principalmente:

- definição da população de estudo;
- definição da variável alvo;
- identificação de data leakage;
- seleção inicial de features;
- avaliação de cobertura temporal;
- validação das chaves de integração;
- definição do dataset de modelagem.

---

## 2. População de modelagem

O modelo principal utilizará alunos avaliados em 2024.

Foram considerados somente registros que atendem aos critérios:

- ano = 2024;
- presença na avaliação;
- prova preenchida.

População resultante:

- 1.851.852 alunos;
- 1.851.852 identificadores distintos;
- nenhuma duplicidade.

Cada observação do dataset representa um aluno avaliado em 2024.

---

## 3. Variável alvo

A variável alvo definida para o problema de classificação é:

`alfabetizado`

Distribuição na população selecionada:

- Alfabetizados: 1.107.119 (59,78%);
- Não alfabetizados: 744.733 (40,22%).

O problema é tratado inicialmente como classificação binária
supervisionada.

---

## 4. Auditoria de leakage

### 4.1 Proficiência

A análise da variável `proficiencia` mostrou uma relação direta com a
classificação de alfabetização.

Os alunos classificados como alfabetizados apresentam proficiência a
partir de aproximadamente 743 pontos, indicando que a variável participa
diretamente da determinação do resultado da avaliação.

Por esse motivo, `proficiencia` do mesmo ciclo da avaliação não será
utilizada como feature do modelo.

Classificação:

**Leakage direto.**

### 4.2 Taxa de alfabetização municipal

Foi reconstruída a taxa de alfabetização municipal a partir dos registros
individuais dos alunos.

A taxa ponderada utilizando `peso_aluno` apresentou correlação de:

- 0,99944 em 2023;
- 0,99969 em 2024;

com a taxa oficial municipal.

O erro médio absoluto foi aproximadamente:

- 0,046 ponto percentual em 2023;
- 0,030 ponto percentual em 2024.

Os resultados indicam que a taxa municipal do mesmo ano contém informação
agregada diretamente relacionada ao target dos alunos daquele ciclo.

Por esse motivo, indicadores municipais contemporâneos à avaliação não
serão utilizados como features.

Classificação:

**Leakage agregado / informação pós-evento.**

---

## 5. Estratégia temporal

Para evitar leakage, foi definida uma estratégia de utilização de
informações históricas.

Para prever o resultado dos alunos avaliados em 2024, serão utilizadas
informações municipais referentes a 2023.

A integração é realizada pelas chaves:

- `id_municipio`;
- `rede`.

Foi validado que essa combinação é única na tabela municipal de 2023,
evitando multiplicação de registros durante o JOIN.

---

## 6. Cobertura histórica

Dos 1.851.852 alunos selecionados em 2024:

- 1.816.270 possuem histórico municipal de 2023;
- 35.582 não possuem histórico;
- cobertura total: 98,08%.

Cobertura por rede:

- Estadual: 88,67%;
- Municipal: 99,49%;
- Privada: 0% (24 registros).

Os alunos sem histórico não serão removidos automaticamente.

As features históricas permanecerão ausentes nesses casos e o tratamento
será realizado posteriormente dentro do pipeline de Machine Learning,
evitando vazamento de informação entre treino e teste.

Também será avaliada a criação da variável:

`historico_2023_disponivel`

para identificar registros que possuem informações históricas.

---

## 7. Features candidatas

### Contexto de 2024

- rede.

### Histórico municipal de 2023

- taxa_alfabetizacao_2023;
- media_portugues_2023;
- proporcao_nivel_0_2023;
- proporcao_nivel_1_2023;
- proporcao_nivel_2_2023;
- proporcao_nivel_3_2023;
- proporcao_nivel_4_2023;
- proporcao_nivel_5_2023;
- proporcao_nivel_6_2023;
- proporcao_nivel_7_2023;
- proporcao_nivel_8_2023.

### Feature auxiliar

- historico_2023_disponivel.

---

## 8. Variáveis não utilizadas diretamente como features

| Variável | Motivo |
|---|---|
| alfabetizado | Target |
| proficiencia_2024 | Leakage direto |
| taxa_alfabetizacao_2024 | Leakage agregado |
| media_portugues_2024 | Informação contemporânea/pós-evento |
| proporções dos níveis 2024 | Informação contemporânea/pós-evento |
| presenca | Utilizada como filtro da população |
| preenchimento_caderno | Utilizada como filtro da população |
| serie | Sem variabilidade relevante na população |
| caderno | Instrumento da avaliação |
| id_aluno | Identificador |
| id_municipio | Chave de integração |
| id_escola | Identificador/contexto a ser avaliado |

`peso_aluno` será avaliado separadamente como possível `sample_weight`
durante treinamento e avaliação dos modelos.

---

## 9. Contrato v1 do dataset

**Nome lógico:** `modeling_dataset_2024`

**Granularidade:** uma linha por aluno avaliado em 2024.

**População:** alunos presentes e com prova preenchida.

**Target:** `alfabetizado`.

**Estratégia temporal:** features históricas de 2023 para previsão de 2024.

**Cobertura histórica:** 98,08%.

**Duplicidades:** nenhuma.

**Tratamento de dados ausentes:** deverá ocorrer dentro do pipeline de
Machine Learning.

**Prevenção de leakage:** variáveis derivadas ou resultantes da avaliação
de 2024 não serão fornecidas ao modelo.

---

## 10. Próximas etapas

1. Construção reproduzível do dataset de modelagem;
2. Análise exploratória dos dados;
3. definição da estratégia de treino e teste;
4. criação do pipeline de pré-processamento;
5. desenvolvimento de modelos baseline;
6. treinamento e comparação dos modelos;
7. otimização de hiperparâmetros;
8. avaliação;
9. interpretabilidade dos resultados;
10. documentação das conclusões.