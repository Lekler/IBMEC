import os
import requests
import pandas as pd
import re
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()
token = os.getenv('TOKEN')


def obter_dados_planilhao(data_base):
    """Função para obter os dados do planilhão."""
    headers = {'Authorization': f'JWT {token}'}
    params = {'data_base': data_base}
    response = requests.get(
        'https://laboratoriodefinancas.com/api/v1/planilhao', params=params, headers=headers)
    if response.status_code == 200:
        return response.json()["dados"]
    else:
        print("Erro ao obter dados do planilhão:", response.text)
        return None


def obter_preco_acoes(ticker, data_ini, data_fim):
    """Função para obter os dados de preço de ações."""
    headers = {'Authorization': f'JWT {token}'}
    params = {'ticker': ticker, 'data_ini': data_ini, 'data_fim': data_fim}
    response = requests.get(
        'https://laboratoriodefinancas.com/api/v1/preco-corrigido', params=params, headers=headers)
    if response.status_code == 200:
        return response.json()["dados"]
    else:
        print(f"Erro ao obter dados de preço para {ticker}:", response.text)
        return None


def obter_preco_ibovespa(data_ini, data_fim):
    """Função para obter os dados do IBOVESPA."""
    headers = {'Authorization': f'JWT {token}'}
    params = {'ticker': 'ibov', 'data_ini': data_ini, 'data_fim': data_fim}
    response = requests.get(
        'https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params, headers=headers)
    if response.status_code == 200:
        return response.json()['dados']
    else:
        print("Erro ao obter dados do Ibovespa:", response.text)
        return None


def calcular_rendimento(df):
    """Função para calcular o rendimento percentual de uma ação."""
    if isinstance(df, list):
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
    # Verifique se o token foi fornecido
    if not token:
        print("Por favor, defina o seu token JWT no arquivo .env.")
        return

    # Definir datas de início e fim
    data_inicio = '2023-04-03'
    data_fim = '2024-09-25'

    # Executando a análise
    dados_planilhao = obter_dados_planilhao(data_inicio)
    if not dados_planilhao:
        print("Não foi possível obter os dados do planilhão.")
        return

    df_planilhao = pd.DataFrame(dados_planilhao)

    # API IBOVESPA
    dados_ibovespa = obter_preco_ibovespa('2023-04-01', '2024-04-01')
    if not dados_ibovespa:
        print("Não foi possível obter os dados do Ibovespa.")
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
    df_top_10_roe = df_roe_filtrado[['ticker', 'roe']].sort_values(
        by='roe', ascending=False).head(10)

    rendimentos_roe = analisar_acoes(df_top_10_roe, data_inicio, data_fim)
    acima_ibov_roe, abaixo_ibov_roe = comparar_rendimentos(
        rendimentos_roe, rendimento_ibovespa)

    # Análise Magic Formula
    df_magic = df_planilhao[['setor', 'ticker',
                             'roic', 'earning_yield', 'volume']].copy()
    df_magic['nome_base'] = df_magic['ticker'].apply(
        lambda x: re.sub(r'\d+$', '', x))
    df_magic_filtrado = df_magic.loc[df_magic.groupby(
        'nome_base')['volume'].idxmax()].copy()

    # Remover setores que não se aplicam à fórmula
    setores_remover = ['bancos', 'seguros', 'financeiros']
    df_magic_filtrado = df_magic_filtrado.loc[~df_magic_filtrado['setor'].str.lower(
    ).isin(setores_remover)].copy()

    # Remover empresas com dados faltantes em 'roic' ou 'earning_yield'
    df_magic_filtrado = df_magic_filtrado.dropna(
        subset=['roic', 'earning_yield'])

    # Calcular rankings individuais
    df_magic_filtrado['ranking_roic'] = df_magic_filtrado['roic'].rank(
        ascending=False)
    df_magic_filtrado['ranking_earning_yield'] = df_magic_filtrado['earning_yield'].rank(
        ascending=False)

    # Calcular ranking combinado
    df_magic_filtrado['ranking_combined'] = df_magic_filtrado['ranking_roic'] + \
        df_magic_filtrado['ranking_earning_yield']

    # Selecionar top 10 ações com base no ranking combinado
    df_magic_top10 = df_magic_filtrado.sort_values(
        by='ranking_combined').head(10)

    # Analisar rendimentos das ações selecionadas
    rendimentos_mf = analisar_acoes(df_magic_top10, data_inicio, data_fim)
    acima_ibov_mf, abaixo_ibov_mf = comparar_rendimentos(
        rendimentos_mf, rendimento_ibovespa)

    # Exibindo resultados
    print(f"Rendimento Ibovespa = {rendimento_ibovespa:.2f}%")
    print("---------------------------------------------------")
    print("Top 10 ações por ROE:")
    for ticker, rendimento in rendimentos_roe:
        if rendimento is not None:
            print(f"Rendimento total da ação {ticker}: {rendimento:.2f}%")
        else:
            print(f"Não foi possível obter o rendimento para a ação {ticker}.")
    carteira_roe = sum([r for _, r in rendimentos_roe if r is not None]) / \
        len([r for _, r in rendimentos_roe if r is not None])
    print(f"\nAções acima do Ibovespa:")
    for k in acima_ibov_roe:
        print(f'- {k}')
    print(f"\nAções abaixo do Ibovespa:")
    for l in abaixo_ibov_roe:
        print(f'- {l}')
    print(f"\nRendimento médio da carteira ROE = {carteira_roe:.2f}%")
    print("---------------------------------------------------")
    print("Top 10 ações pela Magic Formula:")
    for ticker, rendimento in rendimentos_mf:
        if rendimento is not None:
            print(f"Rendimento total da ação {ticker}: {rendimento:.2f}%")
        else:
            print(f"Não foi possível obter o rendimento para a ação {ticker}.")
    carteira_mf = sum([r for _, r in rendimentos_mf if r is not None]) / \
        len([r for _, r in rendimentos_mf if r is not None])
    print(f"\nAções acima do Ibovespa:")
    for i in acima_ibov_mf:
        print(f'- {i}')
    print(f"\nAções abaixo do Ibovespa:")
    for j in abaixo_ibov_mf:
        print(f'- {j}')
    print(f"\nRendimento médio da carteira Magic Formula = {carteira_mf:.2f}%")
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
