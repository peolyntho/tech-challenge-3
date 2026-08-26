QUERY_ALUNOS_2024 = """
SELECT
    ano,
    id_municipio,
    id_escola,
    id_aluno,
    rede,
    alfabetizado,
    peso_aluno
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
WHERE
    ano = 2024
    AND presenca = '1'
    AND preenchimento_caderno = '1'
"""


QUERY_MUNICIPIO_2023 = """
SELECT
    ano,
    id_municipio,
    rede,
    taxa_alfabetizacao,
    media_portugues
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.municipio`
WHERE ano = 2023
"""