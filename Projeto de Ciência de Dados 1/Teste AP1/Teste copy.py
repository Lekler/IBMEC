import pandas as pd
import re
import os
import requests
from dotenv import load_dotenv

# Carregar o token do arquivo .env ou solicitar ao usuário
load_dotenv()
token = os.getenv('TOKEN')

if not token:
    import getpass
    token = getpass.getpass('Insira seu access token: ')

headers = {'Authorization': f'JWT {token}'}


def obter_dados_planilhao(data_base):
    """Função para obter os dados do planilhão."""
    params = {'data_base': data_base}
    try:
        response = requests.get(
            'https://laboratoriodefinancas.com/api/v1/planilhao', params=params, headers=headers)
        response.raise_for_status()
        return response.json()["dados"]
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados do planilhão: {e}")
        return None


def obter_preco_acoes(ticker, data_ini, data_fim):
    """Função para obter os dados de preço de ações."""
    params = {'ticker': ticker, 'data_ini': data_ini, 'data_fim': data_fim}
    try:
        response = requests.get(
            'https://laboratoriodefinancas.com/api/v1/preco-corrigido', params=params, headers=headers)
        response.raise_for_status()
        return response.json()["dados"]
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter preço da ação {ticker}: {e}")
        return None


def obter_preco_ibovespa(data_ini, data_fim):
    """Função para obter os dados do IBOVESPA."""
    params = {'ticker': 'ibov', 'data_ini': data_ini, 'data_fim': data_fim}
    try:
        response = requests.get(
            'https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params, headers=headers)
        response.raise_for_status()
        return response.json()['dados']
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados do IBOVESPA: {e}")
        return None


def calcular_rendimento(df):
    """Função para calcular o rendimento percentual de uma ação ou índice."""
    if isinstance(df, list):
        # Assumindo que df é uma lista de dicionários com 'data' e 'fechamento'
        df = pd.DataFrame(df)

    df['data'] = pd.to_datetime(df['data'])
    df = df.sort_values(by='data')
    inicial = df['fechamento'].iloc[0]
    final = df['fechamento'].iloc[-1]
    rendimento = ((final - inicial) / inicial) * 100
    return rendimento


def analisar_acoes(df_acoes, data_ini, data_fim):
    """Função para analisar o rendimento das ações."""
    resultados = []
    # Garantir que cada ticker seja analisado apenas uma vez
    for ticker in df_acoes['ticker'].unique():
        dados_preco = obter_preco_acoes(ticker, data_ini, data_fim)
        if dados_preco:
            df_preco = pd.DataFrame(dados_preco)
            rendimento = calcular_rendimento(df_preco)
            resultados.append((ticker, rendimento))
        else:
            resultados.append((ticker, None))
    return resultados


def comparar_rendimentos(rendimentos, rendimento_ibov):
    """Função para comparar os rendimentos com o Ibovespa."""
    acima = [ticker for ticker,
             rend in rendimentos if rend is not None and rend > rendimento_ibov]
    abaixo = [ticker for ticker,
              rend in rendimentos if rend is not None and rend <= rendimento_ibov]
    return acima, abaixo


def main():
    # Definir datas de análise
    data_base = '2023-04-03'
    data_ini = '2023-04-03'
    data_fim = '2024-04-01'

    # Executando a análise
    dados_planilhao = obter_dados_planilhao(data_base)
    if not dados_planilhao:
        print("Não foi possível obter os dados do planilhão.")
        return
    df_planilhao = pd.DataFrame(dados_planilhao)

    # API IBOVESPA
    dados_ibovespa = obter_preco_ibovespa(data_ini, data_fim)
    if not dados_ibovespa:
        print("Não foi possível obter os dados do IBOVESPA.")
        return
    df_ibovespa = pd.DataFrame(dados_ibovespa)

    # Calcular rendimento do IBOVESPA
    rendimento_ibovespa = calcular_rendimento(df_ibovespa)

    # Análise ROE
    df_roe = df_planilhao[['ticker', 'roe', 'volume']].copy()
    df_roe['nome_base'] = df_roe['ticker'].apply(
        lambda x: re.sub(r'\d+$', '', x))
    df_roe_filtrado = df_roe.loc[df_roe.groupby(
        'nome_base')['volume'].idxmax()].copy()
    df_roe_filtrado = df_roe_filtrado.dropna(
        subset=['roe'])  # Remover valores nulos em 'roe'
    df_top_10_roe = df_roe_filtrado[['ticker', 'roe']].sort_values(
        by='roe', ascending=False).head(10)

    rendimentos_roe = analisar_acoes(df_top_10_roe, data_ini, data_fim)
    acima_ibov_roe, abaixo_ibov_roe = comparar_rendimentos(
        rendimentos_roe, rendimento_ibovespa)

    # Análise Magic Formula
    df_magic = df_planilhao[['setor', 'ticker',
                             'roic', 'earning_yield', 'volume']].copy()
    df_magic['nome_base'] = df_magic['ticker'].apply(
        lambda x: re.sub(r'\d+$', '', x))
    df_magic_filtrado = df_magic.loc[df_magic.groupby(
        'nome_base')['volume'].idxmax()].copy()
    setores_remover = ['banco', 'seguro', 'financeiro']
    df_magic_filtrado = df_magic_filtrado.loc[~df_magic_filtrado['setor'].str.lower(
    ).isin(setores_remover)].copy()
    df_magic_filtrado = df_magic_filtrado.dropna(
        subset=['roic', 'earning_yield'])
    df_magic_filtrado['ranking_roic'] = df_magic_filtrado['roic'].rank(
        ascending=False)
    df_magic_filtrado['ranking_earning_yield'] = df_magic_filtrado['earning_yield'].rank(
        ascending=False)
    df_magic_filtrado['ranking_combined'] = df_magic_filtrado['ranking_roic'] + \
        df_magic_filtrado['ranking_earning_yield']
    df_magic_top10 = df_magic_filtrado.sort_values(
        by='ranking_combined').head(10)
    rendimentos_mf = analisar_acoes(df_magic_top10, data_ini, data_fim)
    acima_ibov_mf, abaixo_ibov_mf = comparar_rendimentos(
        rendimentos_mf, rendimento_ibovespa)

    # Exibindo resultados
    print(f"Rendimento Ibovespa = {rendimento_ibovespa:.2f}%")
    print("---------------------------------------------------")
    print("ROE:")
    for ticker, rendimento in rendimentos_roe:
        if rendimento is not None:
            print(f"Rendimento total da ação {ticker}: {rendimento:.2f}%")
        else:
            print(f"Não foi possível obter dados para a ação {ticker}")
    rendimentos_validos_roe = [r for _, r in rendimentos_roe if r is not None]
    carteira_roe = sum(rendimentos_validos_roe) / \
        len(rendimentos_validos_roe) if rendimentos_validos_roe else 0
    print(f"\nAções acima do Ibovespa:")
    for k in acima_ibov_roe:
        print(f'- {k}')
    print(f"\nAções abaixo do Ibovespa:")
    for l in abaixo_ibov_roe:
        print(f'- {l}')
    print(f"\nRendimento carteira ROE = {carteira_roe:.2f}%")
    print("---------------------------------------------------")
    print("Magic Formula:")
    for ticker, rendimento in rendimentos_mf:
        if rendimento is not None:
            print(f"Rendimento total da ação {ticker}: {rendimento:.2f}%")
        else:
            print(f"Não foi possível obter dados para a ação {ticker}")
    rendimentos_validos_mf = [r for _, r in rendimentos_mf if r is not None]
    carteira_mf = sum(rendimentos_validos_mf) / \
        len(rendimentos_validos_mf) if rendimentos_validos_mf else 0
    print(f"\nAções acima do Ibovespa:")
    for i in acima_ibov_mf:
        print(f'- {i}')
    print(f"\nAções abaixo do Ibovespa:")
    for j in abaixo_ibov_mf:
        print(f'- {j}')
    print(f"\nRendimento carteira Magic Formula = {carteira_mf:.2f}%")
    print("---------------------------------------------------")
    # Comparação com Ibovespa
    if carteira_roe > rendimento_ibovespa:
        print("A carteira ROE superou o Ibovespa! Bom investimento!")
    else:
        print("A carteira ROE ficou abaixo do Ibovespa. É hora de reavaliar.")

    if carteira_mf > rendimento_ibovespa:
        print("A carteira da Magic Formula superou o Ibovespa! Estratégia eficaz!")
    else:
        print("A carteira da Magic Formula ficou abaixo do Ibovespa. É hora de reavaliar.")


if __name__ == "__main__":
    main()