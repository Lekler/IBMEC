import matplotlib.pyplot as plt
import yfinance as yf
import requests
import pandas as pd

# Insira o seu access token aqui
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5NDA1MjIyLCJqdGkiOiI4MDQwOTU0ZWZmN2Q0ZDlhODk5OGJiYWNkYmFkNzExNiIsInVzZXJfaWQiOjUxfQ.ODsnYxXBwULvWJs9FNZhqoP3fdxsXdVEn1RIqwTLLzE"

headers = {
    'Authorization': f'JWT {token}'
}

params = {
    'data_base': '2024-09-18'
}

url = 'https://laboratoriodefinancas.com/api/v1/planilhao'

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    
    # Converter 'roe' para numérico
    df['roe'] = pd.to_numeric(df['roe'], errors='coerce')
    
    # Remover linhas com ROE nulo
    df = df.dropna(subset=['roe'])
    
    # Ordenar por ROE em ordem decrescente
    df_top_roe = df.sort_values(by='roe', ascending=False)
    
    # Selecionar as top 10 ações
    top10_roe = df_top_roe.head(10)
    
    # Exibir as top 10 ações com seus respectivos ROEs
    print("Top 10 ações por ROE em 01/04/2023:")
    print(top10_roe[['ticker', 'roe']])
else:
    print(f"Erro na requisição: {response.status_code}")
    print(response.text)



ibovespa = yf.download('^BVSP', start='2023-04-01', end='2024-09-18')

# Lista dos tickers das top 10 ações
tickers = top10_roe['ticker'].tolist()

# Ajustar os tickers para o formato do Yahoo Finance, se necessário (por exemplo, acrescentar '.SA' para ações brasileiras)
tickers = [ticker + '.SA' for ticker in tickers]

# Obter dados históricos de preços
precos = yf.download(tickers, start='2023-04-01', end='2024-04-01')

# Exibir os preços de fechamento ajustados
precos_fechamento = precos['Adj Close']
print(precos_fechamento)


# Calcular retornos diários das ações
retornos_acoes = precos_fechamento.pct_change()

# Calcular o retorno médio diário da carteira
retorno_carteira = retornos_acoes.mean(axis=1)

# Obter dados do IBOVESPA
ibovespa = yf.download('^BVSP', start='2023-04-01', end='2024-04-01')
retorno_ibovespa = ibovespa['Adj Close'].pct_change()

# Calcular retornos acumulados
retorno_carteira_acumulado = (1 + retorno_carteira).cumprod()
retorno_ibovespa_acumulado = (1 + retorno_ibovespa).cumprod()

# Plotar os retornos acumulados
plt.figure(figsize=(12, 6))
plt.plot(retorno_carteira_acumulado, label='Carteira Top 10 ROE')
plt.plot(retorno_ibovespa_acumulado, label='IBOVESPA')
plt.legend()
plt.title('Desempenho da Carteira vs IBOVESPA')
plt.xlabel('Data')
plt.ylabel('Retorno Acumulado')
plt.show()

# Converter 'p_l' para numérico
df['p_l'] = pd.to_numeric(df['p_l'], errors='coerce')

# Remover linhas com P/L nulo ou negativo
df = df[(df['p_l'] > 0) & (df['p_l'].notnull())]

# Calcular rankings
df['rank_roe'] = df['roe'].rank(ascending=False)
df['rank_pl'] = df['p_l'].rank(ascending=True)

# Soma dos rankings
df['rank_total'] = df['rank_roe'] + df['rank_pl']

# Ordenar pelo ranking total
df_magic_formula = df.sort_values('rank_total')

# Selecionar as top 10 ações pela Magic Formula
top10_magic = df_magic_formula.head(10)

# Exibir as top 10 ações
print("Top 10 ações pela Magic Formula:")
print(top10_magic[['ticker', 'roe', 'p_l', 'rank_total']])
