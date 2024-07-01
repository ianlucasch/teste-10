import streamlit as st
import pandas as pd
import sqlite3

conectar = sqlite3.connect('../data/quotes.db')

df = pd.read_sql_query("SELECT * FROM mercadolivre_produtos", conectar)

conectar.close()

st.title("Pesquisa de Mercado - Tênis Esportivos no Mercado Livre")
st.subheader("KPIs principais do sistema")

col1, col2, col3 = st.columns(3)

total_produtos = df.shape[0]
col1.metric(label="Número Total de Produtos", value=total_produtos)

marcas_unicas = df['marca'].nunique()
col2.metric(label="Número Total de Marcas Únicas", value=marcas_unicas)

media_preco_atual = df['preco_atual'].mean()
col3.metric(label="Média do Preço Atual (R$)", value=f"{media_preco_atual:.2f}")

st.subheader("Marcas mais encontradas até a página 10")
col1, col2 = st.columns([4, 2])
top_10_marcas = df['marca'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_marcas)
col2.write(top_10_marcas)

st.subheader("Preço médio por marca")
col1, col2 = st.columns([4, 2])
media_preco_por_marca = df.groupby('marca')['preco_atual'].mean().sort_values(ascending=False)
col1.bar_chart(media_preco_por_marca)
col2.write(media_preco_por_marca)

st.subheader('Satisfação do cliente por marca')
col1, col2 = st.columns([4, 2])
df_avaliacoes_sem_zero = df[df['numero_de_avaliacoes_de_comentarios'] > 0]
satisfacao_por_marca = df_avaliacoes_sem_zero.groupby('marca')['numero_de_avaliacoes_de_comentarios'].mean().sort_values(ascending=False)
col1.bar_chart(satisfacao_por_marca)
col2.write(satisfacao_por_marca)