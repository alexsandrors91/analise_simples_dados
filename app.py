# app.py
import streamlit as st
import plotly.express as px
import pandas as pd
from data_analysis import load_data, preprocess, aggregate_by

st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")
st.title("Dashboard de Análise de Dados")

# Carregar dados
DATA_PATH = "data/sample_data.csv"
df = load_data(DATA_PATH)
df = preprocess(df)

# Sidebar - filtros
st.sidebar.header("Filtros")
min_date = df["date"].min()
max_date = df["date"].max()
date_range = st.sidebar.date_input("Período", value=(min_date.date(), max_date.date()))
cat_options = st.sidebar.multiselect("Categorias", options=df["category"].unique(), default=list(df["category"].unique()))

# Aplicar filtros
start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
mask = (df["date"] >= start) & (df["date"] <= end) & (df["category"].isin(cat_options))
filtered = df.loc[mask]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Registros", len(filtered))
col2.metric("Valor total", f"{filtered['value'].sum():,.2f}")
col3.metric("Usuários únicos", filtered["user_id"].nunique())

st.markdown("----")

# Série temporal
st.subheader("Série temporal (valor por dia)")
time_agg = aggregate_by(filtered, ["date"], "value", "sum")
fig_time = px.line(time_agg, x="date", y="value", title="Valor por dia", markers=True)
st.plotly_chart(fig_time, use_container_width=True)

# Distribuição por categoria
st.subheader("Distribuição por categoria")
cat_agg = aggregate_by(filtered, ["category"], "value", "sum")
fig_cat = px.bar(cat_agg, x="category", y="value", title="Valor por categoria")
st.plotly_chart(fig_cat, use_container_width=True)

# Tabela
st.subheader("Dados (amostra)")
st.dataframe(filtered.sample(min(100, len(filtered))).reset_index(drop=True))

# Download dos dados filtrados
@st.cache_data
def to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

csv = to_csv(filtered)
st.download_button("Baixar dados filtrados (CSV)", data=csv, file_name="filtered_data.csv", mime="text/csv")
