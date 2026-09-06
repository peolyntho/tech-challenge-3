"""
Contrato do dataset de modelagem da Fase 3.

Formaliza em código a definição da seção "Dataset de modelagem definido"
do documento de status do grupo, construída sobre o pipeline existente
(`src.preprocessing.pipeline`), sem alterá-lo.

O contrato declara:

- os grupos de colunas e seus papéis (identificação, amostral, target,
  histórico e controle de ausência);
- os resultados esperados da validação final do artefato
  `data/processed/modeling_dataset_2024.parquet`.
"""
from __future__ import annotations


# ------------------------------------------------------------
# Grupos de colunas do dataset de modelagem
# ------------------------------------------------------------

COLUMN_GROUPS: dict[str, dict[str, object]] = {
    "identificacao_contexto": {
        "colunas": [
            "ano",
            "id_aluno",
            "id_municipio",
            "id_escola",
            "rede",
        ],
        "uso": "Rastreabilidade e segmentação",
    },
    "informacao_amostral": {
        "colunas": [
            "peso_aluno",
        ],
        "uso": "Peso da observação",
    },
    "target": {
        "colunas": [
            "alfabetizado",
        ],
        "uso": "Variável a ser prevista",
    },
    "historico_2023": {
        "colunas": [
            "taxa_alfabetizacao_2023",
            "media_portugues_2023",
        ],
        "uso": "Features temporais",
    },
    "controle_ausencia": {
        "colunas": [
            "historico_2023_disponivel",
        ],
        "uso": "Flag para ausência do histórico",
    },
}


TARGET_COLUMN = "alfabetizado"

HISTORY_FLAG_COLUMN = "historico_2023_disponivel"

HISTORY_FEATURE_COLUMNS = [
    "taxa_alfabetizacao_2023",
    "media_portugues_2023",
]

UNIQUE_KEY_COLUMN = "id_aluno"


# ------------------------------------------------------------
# Resultado final validado (valores de referência)
# ------------------------------------------------------------

EXPECTED_ROWS = 1_851_852

EXPECTED_COLUMNS = 10

EXPECTED_HISTORY_AVAILABLE = 1_816_270

EXPECTED_HISTORY_MISSING = 35_582

EXPECTED_TARGET_VALUES = {0, 1}


def get_expected_columns() -> list[str]:
    """
    Retorna a lista ordenada de colunas esperadas
    no dataset de modelagem.

    Returns
    -------
    list[str]
        Colunas de todos os grupos do contrato.
    """

    columns: list[str] = []

    for group in COLUMN_GROUPS.values():
        columns.extend(group["colunas"])

    return columns


def describe_contract() -> str:
    """
    Retorna uma descrição textual do contrato,
    no formato da tabela do documento do grupo.

    Returns
    -------
    str
        Descrição legível dos grupos de colunas.
    """

    lines = [
        "Contrato do dataset de modelagem (Fase 3):",
        "",
    ]

    for group_name, group in COLUMN_GROUPS.items():
        columns = ", ".join(group["colunas"])

        lines.append(
            f"- {group_name}: {columns} "
            f"({group['uso']})"
        )

    lines.extend(
        [
            "",
            f"Linhas esperadas: {EXPECTED_ROWS:,}",
            f"Colunas esperadas: {EXPECTED_COLUMNS}",
            (
                "Histórico disponível esperado: "
                f"{EXPECTED_HISTORY_AVAILABLE:,}"
            ),
            (
                "Histórico indisponível esperado: "
                f"{EXPECTED_HISTORY_MISSING:,}"
            ),
        ]
    )

    return "\n".join(lines)
