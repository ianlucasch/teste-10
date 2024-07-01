import pandas as pd
import sqlite3
from datetime import datetime

pd.options.display.max_columns = None

df = pd.read_json('../data/dados.jsonl', lines=True)

df['preco_antigo_reais'] = df['preco_antigo_reais'].fillna(0).astype(float)
df['preco_antigo_centavos'] = df['preco_antigo_centavos'].fillna(0).astype(float)
df['preco_atual_reais'] = df['preco_atual_reais'].fillna(0).astype(float)
df['preco_atual_centavos'] = df['preco_atual_centavos'].fillna(0).astype(float)
df['numero_de_avaliacoes_de_comentarios'] = df['numero_de_avaliacoes_de_comentarios'].fillna(0).astype(float)

df['quantidade_de_avaliacoes'] = df['quantidade_de_avaliacoes'].str.replace('[\(\)]', '', regex=True)
df['quantidade_de_avaliacoes'] = df['quantidade_de_avaliacoes'].fillna(0).astype(int)

df['preco_antigo'] = df['preco_antigo_reais'] + df['preco_antigo_centavos'] / 100
df['preco_atual'] = df['preco_atual_reais'] + df['preco_atual_centavos'] / 100

df['_data_coleta'] = datetime.now()
df['_fonte'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

df.drop(columns=['preco_antigo_reais', 'preco_antigo_centavos', 'preco_atual_reais', 'preco_atual_centavos'], inplace=True)

conectar = sqlite3.connect('../data/quotes.db')

df.to_sql('mercadolivre_produtos', conectar, if_exists='replace', index=False)

conectar.close()

print(df.head())