import os
import requests
from dotenv import load_dotenv

# Carregar o token do arquivo .env
load_dotenv()
TOKEN = os.getenv('TOKEN')
HEADERS = {'Authorization': f'JWT {TOKEN}'}


def fetch_planilhao_data(date):
    """Obtém os dados do planilhão para a data especificada."""
    params = {'data_base': date}
    response = requests.get(
        'https://laboratoriodefinancas.com/api/v1/planilhao', params=params, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('dados', [])
    else:
        print(f"Erro ao obter dados do planilhão: {response.status_code}")
        return []


def fetch_stock_prices(ticker, start_date, end_date):
    """Obtém os preços ajustados da ação entre as datas especificadas."""
    params = {'ticker': ticker, 'data_ini': start_date, 'data_fim': end_date}
    response = requests.get(
        'https://laboratoriodefinancas.com/api/v1/preco-corrigido', params=params, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('dados', [])
    else:
        print(f"Erro ao obter preços para {ticker}: {response.status_code}")
        return []


def fetch_ibovespa_prices(start_date, end_date):
    """Obtém os preços do IBOVESPA entre as datas especificadas."""
    params = {'ticker': 'ibov', 'data_ini': start_date, 'data_fim': end_date}
    response = requests.get(
        'https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('dados', [])
    else:
        print(f"Erro ao obter preços do IBOVESPA: {response.status_code}")
        return []
