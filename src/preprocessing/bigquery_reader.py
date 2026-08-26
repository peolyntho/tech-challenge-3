from __future__ import annotations

import pandas as pd
from google.cloud import bigquery


def run_query(
    query: str,
    project_id: str,
) -> pd.DataFrame:
    """
    Executa uma consulta SQL no Google BigQuery
    e retorna o resultado como DataFrame.

    Parameters
    ----------
    query : str
        Consulta SQL a ser executada.

    project_id : str
        ID do projeto Google Cloud utilizado
        para execução e faturamento da consulta.

    Returns
    -------
    pd.DataFrame
        Resultado da consulta.
    """

    client = bigquery.Client(project=project_id)

    query_job = client.query(query)

    dataframe = query_job.to_dataframe()

    return dataframe