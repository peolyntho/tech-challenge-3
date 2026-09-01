from __future__ import annotations

import pandas as pd


TARGET_YEAR = 2024
HISTORY_YEAR = 2023


def build_modeling_dataset(
    alunos_df: pd.DataFrame,
    municipio_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Constrói o dataset de modelagem da Fase 3.

    Estratégia:
    - utiliza alunos avaliados em 2024;
    - considera somente a população previamente filtrada
      como presente e com prova preenchida;
    - utiliza indicadores municipais de 2023 como histórico;
    - realiza integração por id_municipio e rede;
    - evita variáveis contemporâneas associadas ao resultado
      da avaliação de 2024.

    Parameters
    ----------
    alunos_df : pd.DataFrame
        Alunos válidos de 2024.

    municipio_df : pd.DataFrame
        Indicadores municipais históricos.

    Returns
    -------
    pd.DataFrame
        Dataset preparado para EDA e modelagem.
    """

    alunos = alunos_df.copy()
    municipio = municipio_df.copy()

    # 1. Valida o ano da população de modelagem
    alunos = alunos.loc[
        alunos["ano"] == TARGET_YEAR
    ].copy()

    # 2. Mantém somente as colunas necessárias
    aluno_columns = [
        "ano",
        "id_aluno",
        "id_municipio",
        "id_escola",
        "rede",
        "peso_aluno",
        "alfabetizado",
    ]

    alunos = alunos[aluno_columns].copy()

    # 3. Seleciona o histórico municipal
    municipio = municipio.loc[
        municipio["ano"] == HISTORY_YEAR
    ].copy()

    municipio_columns = [
        "id_municipio",
        "rede",
        "taxa_alfabetizacao",
        "media_portugues",
    ]

    municipio = municipio[municipio_columns].copy()

    # 4. Valida unicidade da chave histórica
    key_columns = ["id_municipio", "rede"]

    duplicated_keys = municipio.duplicated(
        subset=key_columns,
        keep=False,
    )

    if duplicated_keys.any():
        duplicated_count = (
            municipio.loc[duplicated_keys, key_columns]
            .drop_duplicates()
            .shape[0]
        )

        raise ValueError(
            "Foram encontradas "
            f"{duplicated_count} chaves duplicadas "
            "para id_municipio + rede."
        )

    # 5. Explicita temporalidade das features
    municipio = municipio.rename(
        columns={
            "taxa_alfabetizacao":
                "taxa_alfabetizacao_2023",
            "media_portugues":
                "media_portugues_2023",
        }
    )

    # 6. Join temporal
    dataset = alunos.merge(
        municipio,
        on=key_columns,
        how="left",
        validate="many_to_one",
    )

    # 7. Flag de disponibilidade histórica
    dataset["historico_2023_disponivel"] = (
        dataset["taxa_alfabetizacao_2023"]
        .notna()
        .astype("int8")
    )

    # 8. Normaliza target
    dataset["alfabetizado"] = (
        dataset["alfabetizado"]
        .astype(str)
        .map(
            {
                "0": 0,
                "1": 1,
                "Não": 0,
                "Nao": 0,
                "não": 0,
                "Sim": 1,
                "sim": 1,
            }
        )
    )

    if dataset["alfabetizado"].isna().any():
        raise ValueError(
            "Foram encontrados valores inesperados "
            "na variável 'alfabetizado'."
        )

    dataset["alfabetizado"] = (
        dataset["alfabetizado"].astype("int8")
    )

    # 9. Valida granularidade
    if dataset["id_aluno"].duplicated().any():
        duplicate_count = (
            dataset["id_aluno"].duplicated().sum()
        )

        raise ValueError(
            f"Foram encontrados {duplicate_count} "
            "alunos duplicados após a integração."
        )

    return dataset.reset_index(drop=True)

NETWORK_MAPPING = {
    "2": "Estadual",
    "3": "Municipal",
    "4": "Privada",
}

VALID_MODELING_NETWORKS = [
    "Estadual",
    "Municipal",
]


def build_modeling_dataset_from_gold(
    alunos_df: pd.DataFrame,
    gold_features_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Constrói o dataset de modelagem da Fase 3 utilizando
    features provenientes da camada Gold da Fase 2.

    Estratégia:
    - utiliza alunos avaliados em 2024 como granularidade individual;
    - preserva apenas identificadores, peso amostral e target do aluno;
    - utiliza exclusivamente features históricas/contextuais
      provenientes da Gold da Fase 2;
    - normaliza a identificação da rede de ensino;
    - restringe a modelagem às redes Estadual e Municipal;
    - integra alunos e Gold por id_municipio + rede;
    - preserva alunos mesmo quando algumas features históricas
      não estão disponíveis;
    - cria flag indicando existência de correspondência na Gold;
    - evita features contemporâneas que possam causar data leakage.

    Parameters
    ----------
    alunos_df : pd.DataFrame
        Base individual de alunos avaliados em 2024.

    gold_features_df : pd.DataFrame
        Features consolidadas provenientes da Gold da Fase 2.

    Returns
    -------
    pd.DataFrame
        Dataset individual preparado para EDA e modelagem.
    """

    alunos = alunos_df.copy()
    gold = gold_features_df.copy()

    # 1. Mantém somente o ano-alvo
    alunos = alunos.loc[
        alunos["ano"] == TARGET_YEAR
    ].copy()

    # 2. Mantém somente atributos individuais necessários
    aluno_columns = [
        "ano",
        "id_aluno",
        "id_municipio",
        "id_escola",
        "rede",
        "peso_aluno",
        "alfabetizado",
    ]

    alunos = alunos[aluno_columns].copy()

    # 3. Normaliza rede
    alunos["rede"] = (
        alunos["rede"]
        .astype(str)
        .replace(NETWORK_MAPPING)
    )

    # 4. Mantém somente redes compatíveis com a Gold histórica
    alunos = alunos.loc[
        alunos["rede"].isin(VALID_MODELING_NETWORKS)
    ].copy()

    # 5. Normaliza target
    alunos["alfabetizado"] = (
        alunos["alfabetizado"]
        .astype(str)
        .map(
            {
                "0": 0,
                "1": 1,
                "Não": 0,
                "Nao": 0,
                "não": 0,
                "Sim": 1,
                "sim": 1,
            }
        )
    )

    if alunos["alfabetizado"].isna().any():
        raise ValueError(
            "Foram encontrados valores inesperados "
            "na variável 'alfabetizado'."
        )

    alunos["alfabetizado"] = (
        alunos["alfabetizado"]
        .astype("int8")
    )

    # 6. Valida unicidade dos alunos
    if alunos["id_aluno"].duplicated().any():
        duplicate_count = (
            alunos["id_aluno"]
            .duplicated()
            .sum()
        )

        raise ValueError(
            f"Foram encontrados {duplicate_count} "
            "alunos duplicados antes da integração."
        )

    # 7. Valida unicidade das chaves da Gold
    key_columns = [
        "id_municipio",
        "rede",
    ]

    duplicated_gold_keys = gold.duplicated(
        subset=key_columns,
        keep=False,
    )

    if duplicated_gold_keys.any():
        duplicated_count = (
            gold.loc[
                duplicated_gold_keys,
                key_columns,
            ]
            .drop_duplicates()
            .shape[0]
        )

        raise ValueError(
            "Foram encontradas "
            f"{duplicated_count} chaves duplicadas "
            "na Gold para id_municipio + rede."
        )

    # 8. Integra alunos às features Gold
    dataset = alunos.merge(
        gold,
        on=key_columns,
        how="left",
        validate="many_to_one",
        indicator=True,
    )

    # 9. Flag de existência de contexto Gold
    dataset["gold_historico_disponivel"] = (
        dataset["_merge"]
        .eq("both")
        .astype("int8")
    )

    dataset = dataset.drop(
        columns="_merge"
    )

    # 10. Valida granularidade final
    if dataset["id_aluno"].duplicated().any():
        duplicate_count = (
            dataset["id_aluno"]
            .duplicated()
            .sum()
        )

        raise ValueError(
            f"Foram encontrados {duplicate_count} "
            "alunos duplicados após a integração Gold."
        )

    return dataset.reset_index(drop=True)