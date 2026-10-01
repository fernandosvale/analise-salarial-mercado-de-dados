"""
tests/test_data_loader.py
--------------------------
Testes unitários básicos para o módulo src/data_loader.py.

Execute com:
    pytest tests/
"""

import pandas as pd
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_loader import filter_data, compute_kpis


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def df_sample() -> pd.DataFrame:
    """DataFrame sintético com estrutura idêntica ao dataset real."""
    return pd.DataFrame(
        {
            "ano": [2022, 2022, 2023, 2023, 2023],
            "senioridade": ["SE", "MI", "SE", "EN", "MI"],
            "contrato": ["FT", "FT", "PT", "FT", "CT"],
            "tamanho_empresa": ["L", "M", "S", "L", "M"],
            "cargo": ["Data Scientist", "Data Engineer", "Data Analyst", "Data Scientist", "ML Engineer"],
            "usd": [120000, 90000, 70000, 130000, 110000],
            "remoto": ["Remote", "Hybrid", "On-site", "Remote", "Remote"],
            "residencia_iso3": ["USA", "BRA", "GBR", "USA", "CAN"],
        }
    )


# ---------------------------------------------------------------------------
# Testes: filter_data
# ---------------------------------------------------------------------------

class TestFilterData:
    def test_filter_by_ano(self, df_sample):
        result = filter_data(df_sample, anos=[2022], senioridades=["SE", "MI", "EN"], contratos=["FT", "PT", "CT"], tamanhos=["L", "M", "S"])
        assert list(result["ano"].unique()) == [2022]
        assert len(result) == 2

    def test_filter_returns_empty_when_no_match(self, df_sample):
        result = filter_data(df_sample, anos=[2099], senioridades=["SE"], contratos=["FT"], tamanhos=["L"])
        assert result.empty

    def test_filter_all_selected_returns_full_df(self, df_sample):
        result = filter_data(
            df_sample,
            anos=[2022, 2023],
            senioridades=["SE", "MI", "EN"],
            contratos=["FT", "PT", "CT"],
            tamanhos=["L", "M", "S"],
        )
        assert len(result) == len(df_sample)


# ---------------------------------------------------------------------------
# Testes: compute_kpis
# ---------------------------------------------------------------------------

class TestComputeKpis:
    def test_salario_maximo(self, df_sample):
        kpis = compute_kpis(df_sample)
        assert kpis["salario_maximo"] == 130000

    def test_salario_minimo(self, df_sample):
        kpis = compute_kpis(df_sample)
        assert kpis["salario_minimo"] == 70000

    def test_salario_medio(self, df_sample):
        kpis = compute_kpis(df_sample)
        assert kpis["salario_medio"] == pytest.approx(104000.0)

    def test_total_registros(self, df_sample):
        kpis = compute_kpis(df_sample)
        assert kpis["total_registros"] == 5

    def test_cargo_mais_frequente(self, df_sample):
        kpis = compute_kpis(df_sample)
        assert kpis["cargo_mais_frequente"] == "Data Scientist"
