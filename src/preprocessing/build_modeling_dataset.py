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