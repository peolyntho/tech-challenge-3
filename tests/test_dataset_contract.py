"""
Testes do contrato e da validação do dataset de modelagem.

Utilizam dados sintéticos no mesmo schema do dataset real, sem dependência
de BigQuery ou AWS. Podem ser executados com:

    python -m tests.test_dataset_contract
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.preprocessing.dataset_contract import (
    get_expected_columns,
)
from src.preprocessing.validate_dataset import (
    validate_dataset,
)


def build_synthetic_dataset(rows: int = 1_000) -> pd.DataFrame:
    """
    Constrói um dataset sintético válido no schema do contrato.

    Os primeiros 5% dos registros simulam alunos sem histórico
    municipal de 2023 (flag 0 e features históricas nulas).
    """

    rng = np.random.default_rng(42)

    missing_rows = rows // 20

    flag = np.ones(rows, dtype="int8")
    flag[:missing_rows] = 0

    taxa = rng.uniform(20, 95, rows).astype("float64")
    media = rng.uniform(650, 800, rows).astype("float64")

    taxa[:missing_rows] = np.nan
    media[:missing_rows] = np.nan

    dataset = pd.DataFrame(
        {
            "ano": np.full(rows, 2024),
            "id_aluno": [
                f"aluno_{i:07d}" for i in range(rows)
            ],
            "id_municipio": rng.choice(
                ["3550308", "3304557", "2927408"],
                rows,
            ),
            "id_escola": rng.choice(
                ["11000001", "22000002", "33000003"],
                rows,
            ),
            "rede": rng.choice(
                ["Municipal", "Estadual"],
                rows,
                p=[0.87, 0.13],
            ),
            "peso_aluno": rng.uniform(0.5, 2.0, rows),
            "alfabetizado": rng.choice(
                [0, 1],
                rows,
                p=[0.4, 0.6],
            ).astype("int8"),
            "taxa_alfabetizacao_2023": taxa,
            "media_portugues_2023": media,
            "historico_2023_disponivel": flag,
        }
    )

    return dataset[get_expected_columns()]


def test_dataset_valido_passa_sem_strict():
    dataset = build_synthetic_dataset()

    report = validate_dataset(
        dataset,
        strict_counts=False,
    )

    assert report["valido"], report["errors"]


def test_contagens_exatas_exigidas_no_modo_strict():
    dataset = build_synthetic_dataset()

    report = validate_dataset(
        dataset,
        strict_counts=True,
    )

    # O sintético não possui 1.851.852 linhas,
    # portanto o modo estrito deve falhar.
    assert not report["valido"]


def test_duplicidade_de_id_aluno_reprovada():
    dataset = build_synthetic_dataset()

    dataset.loc[1, "id_aluno"] = dataset.loc[0, "id_aluno"]

    report = validate_dataset(
        dataset,
        strict_counts=False,
    )

    assert not report["valido"]
    assert report["checks"]["unicidade_id_aluno"]


def test_target_nulo_reprovado():
    dataset = build_synthetic_dataset()

    dataset["alfabetizado"] = (
        dataset["alfabetizado"].astype("float64")
    )
    dataset.loc[0, "alfabetizado"] = np.nan

    report = validate_dataset(
        dataset,
        strict_counts=False,
    )

    assert not report["valido"]
    assert report["checks"]["target"]


def test_target_fora_do_dominio_reprovado():
    dataset = build_synthetic_dataset()

    dataset.loc[0, "alfabetizado"] = 2

    report = validate_dataset(
        dataset,
        strict_counts=False,
    )

    assert not report["valido"]
    assert report["checks"]["target"]


def test_incoerencia_flag_e_nulos_reprovada():
    dataset = build_synthetic_dataset()

    # Registro com histórico disponível, porém feature nula.
    dataset.loc[
        dataset.index[-1],
        "taxa_alfabetizacao_2023",
    ] = np.nan

    report = validate_dataset(
        dataset,
        strict_counts=False,
    )

    assert not report["valido"]
    assert report["checks"]["historico_2023"]


def test_schema_incompleto_reprovado():
    dataset = build_synthetic_dataset()

    dataset = dataset.drop(
        columns=["peso_aluno"]
    )

    report = validate_dataset(
        dataset,
        strict_counts=False,
    )

    assert not report["valido"]
    assert report["checks"]["schema"]


def _run_all() -> None:
    tests = [
        value
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    ]

    for test in tests:
        test()
        print(f"OK - {test.__name__}")

    print(f"\n{len(tests)}/{len(tests)} testes passaram.")


if __name__ == "__main__":
    _run_all()
