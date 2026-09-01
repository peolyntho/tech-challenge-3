from __future__ import annotations

import pandas as pd


HISTORY_YEAR = 2023
TARGET_YEAR = 2024

VALID_NETWORKS = [
    "Estadual",
    "Municipal",
]


def build_municipal_gold_features(
    indicador_gold: pd.DataFrame,
) -> pd.DataFrame:
    """
    Constrói features educacionais históricas municipais
    a partir da camada Gold da Fase 2.

    Apenas informações de 2023 são utilizadas para
    contextualizar a previsão dos alunos de 2024.

    Parameters
    ----------
    indicador_gold : pd.DataFrame
        Gold indicador_alfabetizacao_municipio.

    Returns
    -------
    pd.DataFrame
        Features municipais históricas sem informação
        contemporânea ao target de 2024.
    """

    df = indicador_gold.copy()

    # Histórico anterior ao target
    df = df.loc[
        (df["ano"] == HISTORY_YEAR)
        & (df["rede"].isin(VALID_NETWORKS))
    ].copy()

    # Mantém somente informações elegíveis
    columns = [
        "id_municipio",
        "id_municipio_nome",
        "rede",
        "taxa_alfabetizacao",
        "media_portugues",
        "percentual_participacao",
        "meta_alfabetizacao_2024",
    ]

    df = df[columns].copy()

    # Explicita temporalidade e granularidade
    df = df.rename(
        columns={
            "taxa_alfabetizacao":
                "taxa_alfabetizacao_municipio_2023",

            "media_portugues":
                "media_portugues_municipio_2023",

            "percentual_participacao":
                "percentual_participacao_municipio_2023",

            "meta_alfabetizacao_2024":
                "meta_alfabetizacao_municipio_2024",
        }
    )

    # Gap conhecido antes do resultado de 2024
    df["gap_para_meta_municipio_2024"] = (
        df["meta_alfabetizacao_municipio_2024"]
        - df["taxa_alfabetizacao_municipio_2023"]
    )

    # Validação da chave
    key_columns = [
        "id_municipio",
        "rede",
    ]

    duplicated = df.duplicated(
        subset=key_columns,
        keep=False,
    )

    if duplicated.any():
        duplicated_count = (
            df.loc[duplicated, key_columns]
            .drop_duplicates()
            .shape[0]
        )

        raise ValueError(
            "Foram encontradas "
            f"{duplicated_count} chaves duplicadas "
            "nas features municipais Gold."
        )

    return df.reset_index(drop=True)

def build_performance_gold_features(
    desempenho_gold: pd.DataFrame,
) -> pd.DataFrame:
    """
    Constrói features históricas de desempenho educacional
    a partir da camada Gold da Fase 2.

    Utiliza somente dados de 2023 para contextualizar
    a previsão individual de alfabetização em 2024.

    Parameters
    ----------
    desempenho_gold : pd.DataFrame
        Gold desempenho_alunos_municipio.

    Returns
    -------
    pd.DataFrame
        Features históricas de desempenho por município e rede.
    """

    df = desempenho_gold.copy()

    # Apenas histórico anterior ao ano do target
    df = df.loc[
        (df["ano"] == HISTORY_YEAR)
        & (df["rede"].isin(VALID_NETWORKS))
    ].copy()

    columns = [
        "id_municipio",
        "id_municipio_nome",
        "rede",
        "total_alunos",
        "pct_alfabetizados",
        "taxa_alfabetizacao_municipio",
        "proficiencia_media_ponderada",
    ]

    df = df[columns].copy()

    # Nomes explícitos para evitar ambiguidade temporal
    df = df.rename(
        columns={
            "total_alunos":
                "total_alunos_municipio_2023",

            "pct_alfabetizados":
                "pct_alfabetizados_municipio_2023",

            "taxa_alfabetizacao_municipio":
                "taxa_alfabetizacao_desempenho_2023",

            "proficiencia_media_ponderada":
                "proficiencia_media_ponderada_2023",
        }
    )

    # Validação da granularidade esperada
    key_columns = [
        "id_municipio",
        "rede",
    ]

    duplicated = df.duplicated(
        subset=key_columns,
        keep=False,
    )

    if duplicated.any():
        duplicated_count = (
            df.loc[duplicated, key_columns]
            .drop_duplicates()
            .shape[0]
        )

        raise ValueError(
            "Foram encontradas "
            f"{duplicated_count} chaves duplicadas "
            "nas features de desempenho Gold."
        )

    return df.reset_index(drop=True)

def build_municipal_target_features(
    metas_gold: pd.DataFrame,
) -> pd.DataFrame:
    """
    Constrói features municipais relacionadas à meta de alfabetização
    de 2024 utilizando exclusivamente resultados conhecidos de 2023.

    Parameters
    ----------
    metas_gold : pd.DataFrame
        Gold comparativo_metas_resultados.

    Returns
    -------
    pd.DataFrame
        Features de meta por município e rede.
    """

    df = metas_gold.copy()

    df = df.loc[
        (df["nivel_geografico"] == "municipio")
        & (df["ano"] == HISTORY_YEAR)
        & (df["ano_meta"] == TARGET_YEAR)
        & (df["rede"].isin(VALID_NETWORKS))
    ].copy()

    columns = [
        "id_municipio",
        "id_municipio_nome",
        "rede",
        "taxa_alfabetizacao",
        "meta_alfabetizacao",
        "gap_para_meta",
        "atingiu_meta",
    ]

    df = df[columns].copy()

    df = df.rename(
        columns={
            "taxa_alfabetizacao":
                "taxa_alfabetizacao_meta_base_2023",

            "meta_alfabetizacao":
                "meta_alfabetizacao_municipio_2024",

            "gap_para_meta":
                "gap_para_meta_municipio_2024",

            "atingiu_meta":
                "atingiu_meta_municipio_2024",
        }
    )

    key_columns = [
        "id_municipio",
        "rede",
    ]

    duplicated = df.duplicated(
        subset=key_columns,
        keep=False,
    )

    if duplicated.any():
        raise ValueError(
            "Foram encontradas chaves duplicadas "
            "nas features municipais de metas."
        )

    return df.reset_index(drop=True)

UF_CODE_TO_SIGLA = {
    "11": "RO",
    "12": "AC",
    "13": "AM",
    "14": "RR",
    "15": "PA",
    "16": "AP",
    "17": "TO",
    "21": "MA",
    "22": "PI",
    "23": "CE",
    "24": "RN",
    "25": "PB",
    "26": "PE",
    "27": "AL",
    "28": "SE",
    "29": "BA",
    "31": "MG",
    "32": "ES",
    "33": "RJ",
    "35": "SP",
    "41": "PR",
    "42": "SC",
    "43": "RS",
    "50": "MS",
    "51": "MT",
    "52": "GO",
    "53": "DF",
}


def add_uf_from_municipality_code(
    df: pd.DataFrame,
    municipality_column: str = "id_municipio",
) -> pd.DataFrame:
    """
    Deriva a sigla da UF a partir do código IBGE do município.
    """

    result = df.copy()

    uf_code = (
        result[municipality_column]
        .astype(str)
        .str.zfill(7)
        .str[:2]
    )

    result["sigla_uf"] = uf_code.map(UF_CODE_TO_SIGLA)

    return result

def build_uf_socioeconomic_features(
    metas_gold: pd.DataFrame,
) -> pd.DataFrame:
    """
    Constrói features socioeconômicas estaduais a partir da
    camada Gold comparativo_metas_resultados da Fase 2.

    Os indicadores de IDHM são constantes entre redes dentro
    de uma mesma UF. Portanto, a granularidade final é uma
    linha por UF.

    Parameters
    ----------
    metas_gold : pd.DataFrame
        Gold comparativo_metas_resultados.

    Returns
    -------
    pd.DataFrame
        Features socioeconômicas com uma linha por UF.
    """

    df = metas_gold.copy()

    df = df.loc[
        (df["nivel_geografico"] == "uf")
        & (df["ano"] == HISTORY_YEAR)
        & (df["ano_meta"] == TARGET_YEAR),
        [
            "sigla_uf",
            "sigla_uf_nome",
            "idhm",
            "idhm_educacao",
            "idhm_renda",
            "idhm_longevidade",
        ],
    ].copy()

    # Como os valores de IDHM são iguais entre redes,
    # removemos as repetições e mantemos uma linha por UF.
    df = df.drop_duplicates()

    # Validação: deve existir somente um conjunto de
    # indicadores socioeconômicos por UF.
    duplicated = df.duplicated(
        subset=["sigla_uf"],
        keep=False,
    )

    if duplicated.any():
        duplicated_ufs = (
            df.loc[duplicated, "sigla_uf"]
            .unique()
            .tolist()
        )

        raise ValueError(
            "Foram encontrados valores socioeconômicos "
            "divergentes para as UFs: "
            f"{duplicated_ufs}"
        )

    return df.reset_index(drop=True)

def build_consolidated_gold_features(
    indicador_gold: pd.DataFrame,
    desempenho_gold: pd.DataFrame,
    metas_gold: pd.DataFrame,
) -> pd.DataFrame:
    """
    Consolida as principais features educacionais, de metas e
    socioeconômicas provenientes da camada Gold da Fase 2.

    A granularidade final é município + rede.

    As features educacionais utilizam histórico de 2023 e as
    metas representam o objetivo de alfabetização para 2024.

    Parameters
    ----------
    indicador_gold : pd.DataFrame
        Gold indicador_alfabetizacao_municipio.

    desempenho_gold : pd.DataFrame
        Gold desempenho_alunos_municipio.

    metas_gold : pd.DataFrame
        Gold comparativo_metas_resultados.

    Returns
    -------
    pd.DataFrame
        Features Gold consolidadas por município e rede.
    """

    # 1. Indicadores educacionais
    municipal = build_municipal_gold_features(
        indicador_gold
    )

    # As metas serão obtidas da Gold específica de metas.
    # Evitamos manter informações redundantes.
    municipal = municipal.drop(
        columns=[
            "meta_alfabetizacao_municipio_2024",
            "gap_para_meta_municipio_2024",
        ]
    )

    # 2. Desempenho histórico
    performance = build_performance_gold_features(
        desempenho_gold
    )

    # A taxa de alfabetização é idêntica à presente
    # na Gold de indicadores e, portanto, é redundante.
    performance = performance.drop(
        columns=[
            "id_municipio_nome",
            "taxa_alfabetizacao_desempenho_2023",
        ]
    )

    consolidated = municipal.merge(
        performance,
        on=["id_municipio", "rede"],
        how="left",
        validate="one_to_one",
    )

    # 3. Metas municipais
    targets = build_municipal_target_features(
        metas_gold
    )

    targets = targets.drop(
        columns=[
            "id_municipio_nome",
            "taxa_alfabetizacao_meta_base_2023",
        ]
    )

    consolidated = consolidated.merge(
        targets,
        on=["id_municipio", "rede"],
        how="left",
        validate="one_to_one",
    )

    # 4. Derivação territorial município -> UF
    consolidated = add_uf_from_municipality_code(
        consolidated
    )

    # 5. Contexto socioeconômico estadual
    socioeconomic = build_uf_socioeconomic_features(
        metas_gold
    )

    consolidated = consolidated.merge(
        socioeconomic,
        on="sigla_uf",
        how="left",
        validate="many_to_one",
    )

    # 6. Validações finais de granularidade
    key_columns = [
        "id_municipio",
        "rede",
    ]

    if consolidated.duplicated(
        subset=key_columns
    ).any():
        raise ValueError(
            "A consolidação Gold gerou duplicidades "
            "na chave município + rede."
        )

    if consolidated["sigla_uf"].isna().any():
        raise ValueError(
            "Existem municípios sem UF identificada."
        )

    return consolidated.reset_index(drop=True)