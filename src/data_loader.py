"""
src/data_loader.py
------------------
Módulo responsável pelo carregamento e pré-processamento do dataset
de salários na área de dados.
"""

import os
import pandas as pd
from pathlib import Path


# Caminho padrão para o dataset (pode ser sobrescrito via variável de ambiente)
_DEFAULT_DATA_PATH = Path(__file__).parent.parent / "data" / "raw" / "dados-imersao-final.csv"
DATA_PATH = Path(os.getenv("DATA_PATH", _DEFAULT_DATA_PATH))


def load_data() -> pd.DataFrame:
    """
    Carrega o dataset principal a partir do caminho definido em DATA_PATH.

    O caminho pode ser configurado via variável de ambiente ``DATA_PATH``.
    Por padrão, aponta para ``data/raw/dados-imersao-final.csv``.

    Returns
    -------
    pd.DataFrame
        DataFrame com os dados de salários sem transformações adicionais.

    Raises
    ------
    FileNotFoundError
        Se o arquivo não for encontrado no caminho configurado.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset não encontrado em: {DATA_PATH}\n"
            "Verifique se o arquivo está em 'data/raw/' ou ajuste a variável "
            "de ambiente DATA_PATH no seu arquivo .env."
        )
    return pd.read_csv(DATA_PATH)


def filter_data(
    df: pd.DataFrame,
    anos: list,
    senioridades: list,
    contratos: list,
    tamanhos: list,
) -> pd.DataFrame:
    """
    Aplica filtros ao DataFrame principal.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame original carregado por ``load_data``.
    anos : list
        Anos a incluir no filtro.
    senioridades : list
        Níveis de senioridade a incluir.
    contratos : list
        Tipos de contrato a incluir.
    tamanhos : list
        Tamanhos de empresa a incluir.

    Returns
    -------
    pd.DataFrame
        DataFrame filtrado.
    """
    mask = (
        df["ano"].isin(anos)
        & df["senioridade"].isin(senioridades)
        & df["contrato"].isin(contratos)
        & df["tamanho_empresa"].isin(tamanhos)
    )
    return df[mask]


def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Calcula os KPIs principais a partir de um DataFrame filtrado.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame (já filtrado) com os dados de salários.

    Returns
    -------
    dict
        Dicionário com as métricas: salario_medio, salario_maximo,
        salario_minimo, total_registros, cargo_mais_frequente.
    """
    return {
        "salario_medio": df["usd"].mean(),
        "salario_maximo": df["usd"].max(),
        "salario_minimo": df["usd"].min(),
        "total_registros": len(df),
        "cargo_mais_frequente": df["cargo"].mode()[0],
    }
