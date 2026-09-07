# Dataset de modelagem Gold vigente

## Origem e escopo

**Requisito do Tech Challenge:** o PDF oficial da Fase 3 (páginas 2 a 5)
exige uso dos dados da camada Gold da Fase 2, predição supervisionada da
alfabetização individual e tratamento de data leakage.

**Decisão específica do grupo:** integrar features Gold históricas de 2023
por município + rede aos alunos avaliados em 2024, nas redes Estadual e
Municipal. O artefato vigente é
`data/processed/modeling_dataset_2024_gold.parquet`.
O schema e as contagens abaixo são decisões/referências do projeto, não
quantidades prescritas pela FIAP.

Fluxo atual:

```text
Gold Fase 2 (S3)
  -> gold_reader.py
  -> gold_features.py / build_consolidated_gold_features
  -> build_modeling_dataset.py / build_modeling_dataset_from_gold + alunos 2024
  -> modeling_dataset_2024_gold.parquet
  -> dataset_contract.py -> validate_dataset.py -> dataset validado
```

A execução da integração e materialização está em
`notebooks/00_test_gold_integration.ipynb`. Atualmente esse notebook recupera
os atributos individuais dos alunos do artefato legado
`modeling_dataset_2024.parquet`, produzido pelo pipeline de consultas BigQuery.
Esse arquivo é somente uma entrada intermediária: suas features antigas não
são reutilizadas pelo builder Gold e ele não é o dataset vigente da modelagem.
Executar apenas `python -m src.preprocessing.pipeline` não produz o Gold final.

## Schema confirmado

Confirmado contra `gold_features.py`, `build_modeling_dataset_from_gold`,
a saída da célula 37 do notebook de integração e `df.info()` da célula 6 de
`notebooks/01_eda.ipynb` (índices de células iniciando em zero).
São **24 colunas**, sem divergência entre essas fontes.
`dataset_contract.py` é a definição formal consumida pelo validador.
A ordem física das colunas é livre; nomes ausentes, extras ou repetidos falham.
Os dtypes específicos de uma versão de pandas/Parquet não são fixados.

| Grupo | Colunas | Papel |
|---|---|---|
| Identificação | `ano`, `id_aluno`, `id_municipio`, `id_escola`, `id_municipio_nome`, `sigla_uf_nome` | Rastreabilidade |
| Target | `alfabetizado` | Classificação individual de 2024, domínio {0, 1} |
| Informação amostral | `peso_aluno` | Peso da observação |
| Contexto categórico | `rede`, `sigla_uf` | Rede e território |
| Histórico 2023 | `taxa_alfabetizacao_municipio_2023`, `media_portugues_municipio_2023`, `percentual_participacao_municipio_2023`, `total_alunos_municipio_2023`, `pct_alfabetizados_municipio_2023`, `proficiencia_media_ponderada_2023` | Indicadores educacionais Gold |
| Metas/contexto | `meta_alfabetizacao_municipio_2024`, `gap_para_meta_municipio_2024`, `atingiu_meta_municipio_2024` | Meta de 2024 comparada ao histórico de 2023 |
| Socioeconômicas | `idhm`, `idhm_educacao`, `idhm_renda`, `idhm_longevidade` | Indicadores estaduais Gold |
| Disponibilidade | `gold_historico_disponivel` | Correspondência no join Gold |

A presença no contrato não define a seleção final de features, X, y, groups,
pesos amostrais ou split. Essas decisões pertencem à próxima etapa.

## Referências do artefato auditado

- 1.851.828 linhas e 24 colunas; uma linha por aluno avaliado em 2024.
- Zero IDs de aluno duplicados ou nulos; target sem nulos, apenas {0, 1}.
- 1.816.270 alunos com Gold (98,08%) e 35.558 sem Gold (1,92%).
- Target: 1.107.103 na classe 1 (59,78%) e 744.725 na classe 0 (40,22%).

`strict_counts=True` exige o total de linhas e as duas contagens de cobertura.
`strict_counts=False` dispensa somente essas contagens, mantendo schema,
quantidade de colunas, unicidade, target e coerência de missingness.
A proporção de classes é descritiva, não uma restrição de validação.

## Missingness e leakage

A flag é binária e não nula, obtida do indicador de correspondência do
left join, e não da completude de todas as features.

- Flag 0: todas as 16 colunas trazidas pela Gold devem estar nulas, inclusive
  nomes geográficos, UF, metas e IDHM. As chaves e os atributos individuais
  vêm do lado dos alunos e não são incluídos nessa regra.
- Flag 1: o núcleo auditado deve estar preenchido: taxa de alfabetização,
  média de Português, nome do município, sigla/nome da UF e os quatro IDHMs.
  Essa restrição formaliza o artefato auditado na EDA (células 10 e 15),
  e não uma garantia universal de qualquer fonte Gold futura.
- Participação, desempenho agregado e metas podem ser nulos com flag 1.
  A EDA registra 87.097 nulos em participação/metas e 429.286 em desempenho;
  essas contagens descritivas não são impostas como alinhamentos entre fontes.

Nenhuma imputação ou alteração de dados é executada pelo validador.
O schema exato rejeita também a inclusão de atributos individuais contemporâneos
além dos sete selecionados pelo builder. Isso não substitui uma auditoria da
origem dos valores. Conforme a EDA, gap e atingimento comparam a meta de 2024
à taxa de 2023; o contrato não inicia seleção definitiva ou treinamento.

## Validação local e testes

Com o parquet Gold disponível na pasta esperada, execute na raiz:

```bash
python -m src.preprocessing.validate_dataset
```

Esse comando apenas lê o parquet local e não precisa de credenciais AWS/GCP
nem reexecuta a origem. Ausência de arquivo ou violação do contrato produz
falha explícita, sem fallback para o legado. A reprodução da origem pelo
notebook de integração requer acesso autorizado ao S3 e à entrada de alunos;
a regeneração dessa entrada via BigQuery requer o ambiente GCP correspondente.

Os testes usam exclusivamente dados sintéticos em memória, inclusive a
integração entre os builders Gold existentes e o contrato:

```bash
python -m tests.test_dataset_contract
# Alternativamente, se pytest estiver instalado:
python -m pytest
```

Cobrem schema incompleto/extra/repetido, ordem livre, cada feature Gold,
ID duplicado/nulo, target inválido/nulo, flag inválida (sem coerção),
missingness nas duas direções, nulos parciais permitidos, preservação dos
dados e contagens estritas. O teste positivo estrito usa referências pequenas
substituídas apenas durante o teste; não fabrica o artefato real.

Sem o parquet local, esses testes validam o código, mas a validação integral
do artefato continua pendente até sua disponibilização.
