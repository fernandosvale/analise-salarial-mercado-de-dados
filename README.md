# 📊 Dashboard de Análise Salarial no Mercado de Dados

> Dashboard interativo construído com **Python + Streamlit** para explorar tendências salariais globais na área de dados — por cargo, senioridade, tipo de contrato e localização geográfica.

---

## 🎯 Objetivo

O mercado de dados cresceu exponencialmente nos últimos anos, mas **entender a real dinâmica salarial** desse setor não é trivial. Este projeto responde perguntas como:

- Quais cargos pagam mais no mercado de dados?
- Como a senioridade e o tipo de contrato impactam a remuneração?
- Quais países oferecem os maiores salários para Cientistas de Dados?
- A tendência de trabalho remoto está correlacionada a salários mais altos?

---

## 🖼️ Preview

> O dashboard é 100% interativo. Os filtros na barra lateral atualizam todos os gráficos e métricas em tempo real.

| Seção | Descrição |
|---|---|
| **KPIs** | Salário máximo, médio, mínimo, total de registros e cargo mais frequente |
| **Top 10 Cargos** | Ranking de cargos por salário médio anual |
| **Distribuição** | Histograma de frequência por faixa salarial |
| **Tipo de Trabalho** | Proporção entre remoto, híbrido e presencial |
| **Top Países** | Países com maior remuneração média |
| **Mapa Geográfico** | Choropleth com salários de Cientistas de Dados por país |

---

## 🛠️ Tecnologias e Bibliotecas

| Tecnologia | Uso |
|---|---|
| **Python 3.11+** | Linguagem principal |
| **Streamlit 1.44** | Framework de dashboard web |
| **Pandas 2.2** | Manipulação e análise de dados |
| **Plotly 5.24** | Visualizações interativas |
| **python-dotenv 1.0** | Gerenciamento de variáveis de ambiente |
| **pytest 8.3** | Testes unitários |

---

## 📁 Estrutura do Projeto

```
cenario_area_dados/
│
├── app.py                  # Ponto de entrada do dashboard Streamlit
│
├── src/
│   ├── data_loader.py      # Carregamento, filtragem e KPIs
│   └── charts.py           # Funções de visualização (Plotly)
│
├── data/
│   ├── raw/                # Dataset original (não versionado)
│   └── processed/          # Dados transformados (não versionado)
│
├── notebooks/              # Análises exploratórias (EDA)
│
├── tests/
│   └── test_data_loader.py # Testes unitários (pytest)
│
├── .env.example            # Template de variáveis de ambiente
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Como Rodar Localmente

### Pré-requisitos

- Python 3.11 ou superior
- pip

### 1. Clone o repositório

```bash
git clone https://github.com/fernandosvale/analise-salarial-mercado-de-dados.git
cd cenario_area_dados
```

### 2. Crie e ative o ambiente virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
# Copie o template e edite se necessário
copy .env.example .env   # Windows
cp .env.example .env     # Linux/macOS
```

O valor padrão já aponta para `data/raw/dados-imersao-final.csv`. Basta colocar o dataset nesse caminho.

### 5. Adicione o dataset

Coloque o arquivo `dados-imersao-final.csv` em:

```
data/raw/dados-imersao-final.csv
```

> 📌 O dataset não está versionado no repositório por ser um arquivo grande (~11 MB). Ele pode ser obtido em: [AI Jobs Salaries — Kaggle](https://www.kaggle.com/datasets/hummaamqaasim/jobs-in-data)

### 6. Execute o dashboard

```bash
streamlit run app.py
```

O dashboard abrirá automaticamente em `http://localhost:8501`.

---

## 🧪 Executando os Testes

```bash
pytest tests/ -v
```

---

## 🚀 Próximos Passos

- [ ] **Análise temporal** — gráfico de evolução salarial ano a ano com linha de tendência
- [ ] **Filtro por cargo** — permitir selecionar cargos específicos além dos filtros existentes
- [ ] **Comparativo de moedas** — converter salários para BRL usando taxa de câmbio em tempo real
- [ ] **Notebook de EDA** — análise exploratória detalhada com estatísticas descritivas avançadas
- [ ] **Deploy no Streamlit Cloud** — publicar o dashboard online gratuitamente

---

## 📄 Fonte dos Dados

Dataset: **Jobs and Salaries in Data Science** — disponível no [Kaggle](https://www.kaggle.com/datasets/hummaamqaasim/jobs-in-data).

Os dados contêm registros de salários anuais (em USD) de profissionais da área de dados ao redor do mundo, coletados entre 2020 e 2023.

---

## 📬 Contato

Feito por **Fernando Silva Vale** — [LinkedIn](https://www.linkedin.com/in/fernandosilvavale) | [GitHub](https://github.com/fernandosvale)
