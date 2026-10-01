"""
src/charts.py
-------------
Módulo de visualizações: todas as funções que criam figuras Plotly
para o dashboard de salários na área de dados.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Paleta padrão usada em todos os gráficos para consistência visual
_COLOR_SEQUENCE = px.colors.qualitative.Plotly


def chart_top_cargos(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de barras horizontais com os 10 cargos de maior salário médio.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame filtrado com colunas 'cargo' e 'usd'.

    Returns
    -------
    go.Figure
    """
    top_cargos = (
        df.groupby("cargo")["usd"]
        .mean()
        .nlargest(10)
        .sort_values(ascending=True)
        .reset_index()
    )
    fig = px.bar(
        top_cargos,
        x="usd",
        y="cargo",
        orientation="h",
        title="Top 10 Cargos por Salário Médio",
        labels={"usd": "Média Salarial Anual (USD)", "cargo": ""},
        color_discrete_sequence=_COLOR_SEQUENCE,
    )
    fig.update_layout(title_x=0.1, yaxis={"categoryorder": "total ascending"})
    return fig


def chart_distribuicao_salarios(df: pd.DataFrame) -> go.Figure:
    """
    Histograma da distribuição de salários anuais.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame filtrado com coluna 'usd'.

    Returns
    -------
    go.Figure
    """
    fig = px.histogram(
        df,
        x="usd",
        nbins=30,
        title="Distribuição de Salários Anuais",
        labels={"usd": "Faixa Salarial (USD)", "count": "Frequência"},
        color_discrete_sequence=_COLOR_SEQUENCE,
    )
    fig.update_layout(title_x=0.1)
    return fig


def chart_tipo_trabalho(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de rosca (donut) com a proporção dos tipos de trabalho (remoto/híbrido/presencial).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame filtrado com coluna 'remoto'.

    Returns
    -------
    go.Figure
    """
    contagem = df["remoto"].value_counts().reset_index()
    contagem.columns = ["tipo_trabalho", "quantidade"]
    fig = px.pie(
        contagem,
        names="tipo_trabalho",
        values="quantidade",
        title="Proporção dos Tipos de Trabalho",
        hole=0.5,
    )
    fig.update_traces(
        textinfo="percent+label",
        marker=dict(colors=_COLOR_SEQUENCE),
    )
    fig.update_layout(title_x=0.1)
    return fig


def chart_top_paises(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de barras horizontais com os 10 países de maior salário médio.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame filtrado com colunas 'residencia_iso3' e 'usd'.

    Returns
    -------
    go.Figure
    """
    top_paises = (
        df.groupby("residencia_iso3")["usd"]
        .mean()
        .nlargest(10)
        .sort_values(ascending=True)
        .reset_index()
    )
    fig = px.bar(
        top_paises,
        x="usd",
        y="residencia_iso3",
        orientation="h",
        title="Top 10 Países por Salário Médio Anual",
        labels={"usd": "Média Salarial Anual (USD)", "residencia_iso3": "País"},
        color_discrete_sequence=_COLOR_SEQUENCE,
    )
    fig.update_layout(title_x=0.1, yaxis={"categoryorder": "total ascending"})
    return fig


def chart_mapa_data_scientist(df: pd.DataFrame) -> go.Figure | None:
    """
    Mapa coroplético com o salário médio de Cientistas de Dados por país.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame filtrado com colunas 'cargo', 'residencia_iso3' e 'usd'.

    Returns
    -------
    go.Figure ou None
        Retorna None se não houver registros de 'Data Scientist' no DataFrame.
    """
    df_ds = df[df["cargo"] == "Data Scientist"]
    if df_ds.empty:
        return None

    media_por_pais = df_ds.groupby("residencia_iso3")["usd"].mean().reset_index()
    fig = px.choropleth(
        media_por_pais,
        locations="residencia_iso3",
        color="usd",
        color_continuous_scale="RdYlGn",
        title="Salário Médio de Cientista de Dados por País",
        labels={"usd": "Salário Médio (USD)", "residencia_iso3": "País"},
    )
    fig.update_layout(title_x=0.1)
    return fig
