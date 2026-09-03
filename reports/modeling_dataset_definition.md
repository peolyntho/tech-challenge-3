# Dataset de Modelagem Definido

Este documento formaliza a definição do dataset de modelagem da Fase 3 e o
mecanismo de validação do artefato, construídos sobre o pipeline existente
(`src/preprocessing/pipeline.py`) sem alterá-lo.

---

## Definição do dataset

| Grupo | Colunas | Uso |
|---|---|---|
| Identificação/contexto | `ano`, `id_aluno`, `id_municipio`, `id_escola`, `rede` | Rastreabilidade e segmentação |
| Informação amostral | `peso_aluno` | Peso da observação |
| Target | `alfabetizado` | Variável a ser prevista |
| Histórico 2023 | `taxa_alfabetizacao_2023`, `media_portugues_2023` | Features temporais |
| Controle de ausência | `historico_2023_disponivel` | Flag para ausência do histórico |

A definição está codificada em `src/preprocessing/dataset_contract.py`, que
serve como fonte única do schema para validação e para as próximas etapas
(EDA e modelagem).

---

## Resultado final validado (valores de referência)

- Shape: **1.851.852 linhas × 10 colunas**;
- Duplicidades de `id_aluno`: **0**;
- Target nulo: **0** (domínio restrito a `{0, 1}`);
- Histórico disponível: **1.816.270** registros;
- Histórico indisponível: **35.582** registros;
- Nulos nas duas features históricas: **exatamente 35.582**, coerentes com a
  flag de disponibilidade.

---

## Como reproduzir e validar

1. Construir o artefato local (fonte oficial: BigQuery / Base dos Dados,
   conforme DEC-015):

```bash
python -m src.preprocessing.pipeline
```

2. Validar o artefato contra o contrato (não requer BigQuery):

```bash
python -m src.preprocessing.validate_dataset
```

O validador executa as verificações de schema, shape, unicidade do
`id_aluno`, integridade do target e coerência entre a flag
`historico_2023_disponivel` e os nulos das features históricas, falhando com
erro explícito caso qualquer critério não seja atendido.

---

## Testes

A lógica de validação é coberta por testes com dados sintéticos no mesmo
schema do dataset real, sem dependência de BigQuery ou AWS:

```bash
python -m tests.test_dataset_contract
```

Casos cobertos: dataset válido, contagens exatas no modo estrito,
duplicidade de `id_aluno`, target nulo, target fora do domínio,
incoerência entre flag e nulos e schema incompleto.
