"""
app.py
------
Ponto de entrada do dashboard Streamlit de análise salarial
no mercado de dados.

Para rodar localmente:
    streamlit run app.py
"""

import sys
from pathlib import Path

import streamlit as st

# Adiciona 'src/' ao path para permitir importação dos módulos locais
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_loader import load_data, filter_data, compute_kpis  # noqa: E402
from charts import (  # noqa: E402
    chart_top_cargos,
    chart_distribuicao_salarios,
    chart_tipo_trabalho,
    chart_top_paises,
    chart_mapa_data_scientist,
)

# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Carregamento dos dados (cache automático do Streamlit)
# ---------------------------------------------------------------------------
try:
    df = st.cache_data(load_data)()
except FileNotFoundError as exc:
    st.error(str(exc))
    st.stop()

# ---------------------------------------------------------------------------
# Barra lateral — filtros interativos
# ---------------------------------------------------------------------------
st.sidebar.header("🔍 Filtros de Análise")

anos_disponiveis = sorted(df["ano"].unique())
anos_selecionados = st.sidebar.multiselect(
    "Ano", anos_disponiveis, default=anos_disponiveis
)

senioridades_disponiveis = sorted(df["senioridade"].unique())
senioridades_selecionadas = st.sidebar.multiselect(
    "Senioridade", senioridades_disponiveis, default=senioridades_disponiveis
)

contratos_disponiveis = sorted(df["contrato"].unique())
contratos_selecionados = st.sidebar.multiselect(
    "Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis
)

tamanhos_disponiveis = sorted(df["tamanho_empresa"].unique())
tamanhos_selecionados = st.sidebar.multiselect(
    "Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis
)

# ---------------------------------------------------------------------------
# Filtragem do DataFrame
# ---------------------------------------------------------------------------
df_filtrado = filter_data(
    df,
    anos=anos_selecionados,
    senioridades=senioridades_selecionadas,
    contratos=contratos_selecionados,
    tamanhos=tamanhos_selecionados,
)

# ---------------------------------------------------------------------------
# Cabeçalho principal
# ---------------------------------------------------------------------------
st.title("📊 Análise Salarial do Mercado de Dados")
st.markdown(
    """
    Bem-vindo ao dashboard interativo que explora a evolução dos salários na área de dados.
    Utilize os **filtros na barra lateral** para descobrir tendências salariais por cargo,
    senioridade, tipo de contrato e tamanho da empresa.
    """
)
st.markdown("---")

# ---------------------------------------------------------------------------
# KPIs — visão geral do mercado
# ---------------------------------------------------------------------------
st.header("Visão Geral do Mercado")

if df_filtrado.empty:
    st.info(
        "Nenhum registro encontrado para os filtros selecionados. "
        "Por favor, ajuste suas escolhas."
    )
    st.stop()

kpis = compute_kpis(df_filtrado)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Maior Salário", f"${kpis['salario_maximo']:,.0f}")
col2.metric("Salário Médio", f"${kpis['salario_medio']:,.0f}")
col3.metric("Menor Salário", f"${kpis['salario_minimo']:,.0f}")
col4.metric("Total de Registros", f"{kpis['total_registros']:,}")
col5.metric("Cargo Mais Frequente", kpis["cargo_mais_frequente"])

st.markdown("---")

# ---------------------------------------------------------------------------
# Seção: Análise Detalhada dos Salários
# ---------------------------------------------------------------------------
st.header("Análise Detalhada dos Salários")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.plotly_chart(chart_top_cargos(df_filtrado), use_container_width=True)
    st.markdown(
        "**Insight:** Este gráfico mostra as 10 posições com maior remuneração média "
        "no mercado de dados. Ele serve como um guia para identificar **cargos de alto "
        "valor** e planejar o desenvolvimento de carreira."
    )

with col_graf2:
    st.plotly_chart(chart_distribuicao_salarios(df_filtrado), use_container_width=True)
    st.markdown(
        "**Insight:** A distribuição de salários revela a concentração de profissionais "
        "em determinadas faixas de remuneração, indicando os **salários mais comuns** e "
        "a presença de outliers com salários significativamente mais altos."
    )

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    st.plotly_chart(chart_tipo_trabalho(df_filtrado), use_container_width=True)
    st.markdown(
        "**Insight:** A análise da proporção entre trabalho remoto e presencial é crucial "
        "para entender a **flexibilidade do mercado**. Este gráfico mostra como a dinâmica "
        "de trabalho se distribui no setor de dados."
    )

with col_graf4:
    st.plotly_chart(chart_top_paises(df_filtrado), use_container_width=True)
    st.markdown(
        "**Insight:** Este gráfico destaca as **oportunidades de trabalho mais bem pagas** "
        "globalmente, ajudando a identificar mercados com alta remuneração."
    )

# ---------------------------------------------------------------------------
# Seção: Análise Geográfica
# ---------------------------------------------------------------------------
st.markdown("---")
st.header("Análise Geográfica de Salários")
st.markdown("Explore o salário médio por país, focado na profissão de **Cientista de Dados**.")

fig_mapa = chart_mapa_data_scientist(df_filtrado)
if fig_mapa is not None:
    st.plotly_chart(fig_mapa, use_container_width=True)
    st.markdown(
        "**Insight:** O mapa mostra a distribuição geográfica dos salários para Cientistas "
        "de Dados, revelando as **disparidades salariais globais** e onde a profissão é "
        "mais valorizada financeiramente."
    )
else:
    st.warning(
        "Nenhum dado de Cientista de Dados para exibir no mapa com os filtros atuais."
    )

# ---------------------------------------------------------------------------
# Seção: Dados brutos filtrados
# ---------------------------------------------------------------------------
st.markdown("---")
st.header("Dados Detalhados")
st.markdown(
    "A tabela abaixo mostra os dados filtrados. "
    "Utilize a ordenação das colunas para explorar informações específicas."
)
st.dataframe(df_filtrado, use_container_width=True)