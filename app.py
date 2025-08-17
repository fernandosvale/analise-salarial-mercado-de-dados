import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# --- Carregamento dos dados ---
# Nota: É uma boa prática usar um st.cache_data para datasets que não mudam
@st.cache_data
def load_data():
    df = pd.read_csv("dados-imersao-final.csv")
    return df

df = load_data()

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros de Análise")

# Filtro de Ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect(
    "Ano", anos_disponiveis, default=anos_disponiveis
)

# Filtro de Senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect(
    "Senioridade", senioridades_disponiveis, default=senioridades_disponiveis
)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect(
    "Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis
)

# Filtro por Tamanho da Empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect(
    "Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis
)

# --- Filtragem do DataFrame ---
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

# --- Conteúdo Principal: Título e Introdução ---
st.title("📊 Análise Salarial do Mercado de Dados")
st.markdown("""
Bem-vindo ao dashboard interativo que explora a evolução dos salários na área de dados.
Utilize os **filtros na barra lateral** para descobrir tendências salariais por cargo, senioridade, tipo de contrato e tamanho da empresa.
""")
st.markdown("---")

# --- Métricas Principais (KPIs) ---
st.header("Visão Geral do Mercado")

if df_filtrado.empty:
    st.info("Nenhum registro encontrado para os filtros selecionados. Por favor, ajuste suas escolhas.")
    st.stop()  # Interrompe a execução para não mostrar gráficos vazios

# Cálculo das métricas
salario_medio = df_filtrado['usd'].mean()
salario_maximo = df_filtrado['usd'].max()
salario_minimo = df_filtrado['usd'].min()
total_registros = df_filtrado.shape[0]
cargo_mais_frequente = df_filtrado["cargo"].mode()[0]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Maior Salário", f"${salario_maximo:,.0f}")
col2.metric("Salário Médio", f"${salario_medio:,.0f}")
col3.metric("Menor Salário", f"${salario_minimo:,.0f}")
col4.metric("Total de Registros", f"{total_registros:,}")
col5.metric("Cargo Mais Frequente", cargo_mais_frequente)

st.markdown("---")

# --- Análise Detalhada com Gráficos ---
st.header("Análise Detalhada dos Salários")
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    # Gráfico de top 10 cargos por salário médio
    top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
    grafico_cargos = px.bar(
        top_cargos,
        x='usd',
        y='cargo',
        orientation='h',
        title="Top 10 Cargos por Salário Médio",
        labels={'usd': 'Média Salarial Anual (USD)', 'cargo': ''},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(grafico_cargos, use_container_width=True)
    st.markdown("""
    **Insight:** Este gráfico mostra as 10 posições com maior remuneração média no mercado de dados. Ele serve como um guia para identificar **cargos de alto valor** e planejar o desenvolvimento de carreira.
    """)

with col_graf2:
    # Gráfico de distribuição de salários
    grafico_hist = px.histogram(
        df_filtrado,
        x='usd',
        nbins=30,
        title="Distribuição de Salários Anuais",
        labels={'usd': 'Faixa Salarial (USD)', 'count': 'Frequência'},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    grafico_hist.update_layout(title_x=0.1)
    st.plotly_chart(grafico_hist, use_container_width=True)
    st.markdown("""
    **Insight:** A distribuição de salários revela a concentração de profissionais em determinadas faixas de remuneração, indicando os **salários mais comuns** e a presença de outliers com salários significativamente mais altos.
    """)

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    # Gráfico de Proporção de Tipos de Trabalho
    remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
    remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
    grafico_remoto = px.pie(
        remoto_contagem,
        names='tipo_trabalho',
        values='quantidade',
        title='Proporção dos Tipos de Trabalho',
        hole=0.5
    )
    grafico_remoto.update_traces(textinfo='percent+label', marker=dict(colors=px.colors.qualitative.Plotly))
    grafico_remoto.update_layout(title_x=0.1)
    st.plotly_chart(grafico_remoto, use_container_width=True)
    st.markdown("""
    **Insight:** A análise da proporção entre trabalho remoto e presencial é crucial para entender a **flexibilidade do mercado**. Este gráfico mostra como a dinâmica de trabalho se distribui no setor de dados.
    """)

with col_graf4:
    # Gráfico de Top 10 países
    top_paises = df_filtrado.groupby('residencia_iso3')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
    grafico_top_paises = px.bar(
        top_paises,
        x='usd',
        y='residencia_iso3',
        orientation='h',
        title="Top 10 Países por Salário Médio Anual",
        labels={'usd': 'Média Salarial Anual (USD)', 'residencia_iso3': 'País'},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    grafico_top_paises.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(grafico_top_paises, use_container_width=True)
    st.markdown("""
    **Insight:** Este gráfico destaca as **oportunidades de trabalho mais bem pagas** globalmente, ajudando a identificar mercados com alta remuneração.
    """)

# --- Gráfico de Mapa (último gráfico antes da tabela) ---
st.header("Análise Geográfica de Salários")
st.markdown("Explore o salário médio por país, focado na profissão de **Cientista de Dados**.")

df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
if not df_ds.empty:
    media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
    grafico_paises = px.choropleth(
        media_ds_pais,
        locations='residencia_iso3',
        color='usd',
        color_continuous_scale='RdYlGn',
        title='Salário Médio de Cientista de Dados por País',
        labels={'usd': 'Salário Médio (USD)', 'residencia_iso3': 'País'}
    )
    grafico_paises.update_layout(title_x=0.1)
    st.plotly_chart(grafico_paises, use_container_width=True)
    st.markdown("""
    **Insight:** O mapa mostra a distribuição geográfica dos salários para Cientistas de Dados, revelando as **disparidades salariais globais** e onde a profissão é mais valorizada financeiramente.
    """)
else:
    st.warning("Nenhum dado de Cientista de Dados para exibir no mapa com os filtros atuais.")

# --- Tabela de Dados Detalhados ---
st.markdown("---")
st.header("Dados Detalhados")
st.markdown("A tabela abaixo mostra os dados brutos filtrados. Utilize a barra de busca e a ordenação para explorar informações específicas.")
st.dataframe(df_filtrado)