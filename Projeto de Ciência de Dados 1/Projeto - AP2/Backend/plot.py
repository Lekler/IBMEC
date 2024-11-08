# plot.py

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from dotenv import load_dotenv
import re
from datetime import datetime
from scipy import optimize

# Carregar variáveis do arquivo .env
load_dotenv()
token = os.getenv('TOKEN')

# Funções para obter dados (as mesmas utilizadas no main.py)


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


def calcular_rendimento(df):
    """Função para calcular o rendimento percentual de uma ação."""
    if isinstance(df, list):
        df = pd.DataFrame(df)
    df['data'] = pd.to_datetime(df['data'])
    df = df.sort_values(by='data')
    df.set_index('data', inplace=True)
    df['retorno'] = df['fechamento'].pct_change()
    return df


def main():
    # Verifique se o token foi fornecido
    if not token:
        print("Por favor, defina o seu token JWT no arquivo .env.")
        return

    # Definir datas de início e fim
    data_base = '2023-04-03'
    data_inicio = '2022-04-03'
    data_fim = '2023-04-03'

    # Executando a análise
    dados_planilhao = obter_dados_planilhao(data_base)
    if not dados_planilhao:
        print("Não foi possível obter os dados do planilhão.")
        return

    df_planilhao = pd.DataFrame(dados_planilhao)

    # Análise ROE
    df_roe = df_planilhao[['ticker', 'roe', 'volume']].copy()
    df_roe['nome_base'] = df_roe['ticker'].apply(
        lambda x: re.sub(r'\d+$', '', x))
    df_roe_filtrado = df_roe.loc[df_roe.groupby(
        'nome_base')['volume'].idxmax()].copy()
    df_top_10_roe = df_roe_filtrado[['ticker', 'roe']].sort_values(
        by='roe', ascending=False).head(10)

    # Análise Magic Formula
    df_magic = df_planilhao[['setor', 'ticker',
                             'roic', 'earning_yield', 'volume']].copy()
    df_magic['nome_base'] = df_magic['ticker'].apply(
        lambda x: re.sub(r'\d+$', '', x))
    df_magic_filtrado = df_magic.loc[df_magic.groupby(
        'nome_base')['volume'].idxmax()].copy()
    setores_remover = ['bancos', 'seguros', 'financeiros']
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

    # Lista de tickers das carteiras
    tickers_roe = df_top_10_roe['ticker'].tolist()
    tickers_magic = df_magic_top10['ticker'].tolist()

    # Obter dados de preços das ações selecionadas
    # Criar um DataFrame para armazenar os preços
    df_precos = pd.DataFrame()
    for ticker in tickers_roe + tickers_magic:
        dados_preco = obter_preco_acoes(ticker, data_inicio, data_fim)
        if dados_preco:
            df_ticker = pd.DataFrame(dados_preco)
            df_ticker['data'] = pd.to_datetime(df_ticker['data'])
            df_ticker.set_index('data', inplace=True)
            df_precos[ticker] = df_ticker['fechamento']
        else:
            print(f"Dados de preço não disponíveis para {ticker}")

    # Remover colunas com todos os valores nulos
    df_precos.dropna(axis=1, how='all', inplace=True)

    # Preencher valores ausentes com o último valor disponível
    df_precos.fillna(method='ffill', inplace=True)

    # Plotar o histórico de preços das ações
    plt.figure(figsize=(14, 7))
    for ticker in df_precos.columns:
        plt.plot(df_precos.index, df_precos[ticker], label=ticker)
    plt.title('Histórico de Preços das Ações Selecionadas')
    plt.xlabel('Data')
    plt.ylabel('Preço de Fechamento (R$)')
    plt.legend()
    plt.show()

    # Calcular retornos diários das ações
    retornos = df_precos.pct_change().dropna()

    # Plotar o histórico de retornos das ações
    plt.figure(figsize=(14, 7))
    for ticker in retornos.columns:
        plt.plot(retornos.index, retornos[ticker], label=ticker)
    plt.title('Retornos Diários das Ações Selecionadas')
    plt.xlabel('Data')
    plt.ylabel('Retorno Diário')
    plt.legend()
    plt.show()

    # Estatísticas descritivas dos retornos
    print("Estatísticas Descritivas dos Retornos Diários:")
    print(retornos.describe())

    # Matriz de correlação dos retornos
    plt.figure(figsize=(10, 8))
    sns.heatmap(retornos.corr(), annot=True, cmap='coolwarm')
    plt.title('Matriz de Correlação dos Retornos')
    plt.show()

    # Simulação de Portfólios
    # Utilizando apenas as ações com dados disponíveis
    tickers_disponiveis = retornos.columns.tolist()
    num_acoes = len(tickers_disponiveis)
    num_portfolios = 10000
    resultados = np.zeros((3, num_portfolios))
    pesos_registrados = []

    for i in range(num_portfolios):
        # Geração de pesos aleatórios
        pesos = np.random.random(num_acoes)
        pesos /= np.sum(pesos)
        # Registro dos pesos
        pesos_registrados.append(pesos)
        # Retorno esperado do portfólio
        retorno_esperado = np.sum(retornos.mean() * pesos) * 252  # Anualizado
        # Volatilidade do portfólio
        volatilidade = np.sqrt(
            np.dot(pesos.T, np.dot(retornos.cov() * 252, pesos)))
        # Índice de Sharpe (taxa livre de risco assumida como zero)
        sharpe_ratio = retorno_esperado / volatilidade
        # Registro dos resultados
        resultados[0, i] = retorno_esperado
        resultados[1, i] = volatilidade
        resultados[2, i] = sharpe_ratio

    # Convertendo resultados para DataFrame
    df_resultados = pd.DataFrame({
        'Retorno Anualizado': resultados[0],
        'Volatilidade Anualizada': resultados[1],
        'Índice de Sharpe': resultados[2]
    })

    # Adicionando os pesos ao DataFrame
    for i, ticker in enumerate(tickers_disponiveis):
        df_resultados[ticker + ' Peso'] = [w[i] for w in pesos_registrados]

    # Encontrando o portfólio com maior Índice de Sharpe
    max_sharpe_idx = df_resultados['Índice de Sharpe'].idxmax()
    port_max_sharpe = df_resultados.loc[max_sharpe_idx]

    # Encontrando o portfólio de menor volatilidade
    min_vol_idx = df_resultados['Volatilidade Anualizada'].idxmin()
    port_min_vol = df_resultados.loc[min_vol_idx]

    # Plotando os portfólios simulados
    plt.figure(figsize=(14, 7))
    plt.scatter(df_resultados['Volatilidade Anualizada'], df_resultados['Retorno Anualizado'],
                c=df_resultados['Índice de Sharpe'], cmap='viridis')
    plt.colorbar(label='Índice de Sharpe')
    plt.scatter(port_max_sharpe['Volatilidade Anualizada'],
                port_max_sharpe['Retorno Anualizado'], c='red', s=50, label='Máximo Sharpe')
    plt.scatter(port_min_vol['Volatilidade Anualizada'],
                port_min_vol['Retorno Anualizado'], c='blue', s=50, label='Mínima Volatilidade')
    plt.title('Portfólios Simulados')
    plt.xlabel('Volatilidade Anualizada')
    plt.ylabel('Retorno Anualizado')
    plt.legend()
    plt.show()

    # Fronteira Eficiente
    def get_ret_vol_sr(pesos):
        pesos = np.array(pesos)
        retorno = np.sum(retornos.mean() * pesos) * 252
        volatilidade = np.sqrt(
            np.dot(pesos.T, np.dot(retornos.cov() * 252, pesos)))
        sharpe_ratio = retorno / volatilidade
        return np.array([retorno, volatilidade, sharpe_ratio])

    # Função para minimizar (volatilidade)
    def minimize_vol(pesos):
        return get_ret_vol_sr(pesos)[1]

    # Restrições e limites
    limites = tuple((0, 1) for _ in range(num_acoes))
    restricoes = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}

    # Fronteira eficiente para diferentes níveis de retorno
    retornos_alvo = np.linspace(
        port_min_vol['Retorno Anualizado'], port_max_sharpe['Retorno Anualizado'], 50)
    volatilidades = []

    for retorno in retornos_alvo:
        restricoes_ret = [
            {'type': 'eq', 'fun': lambda x: get_ret_vol_sr(x)[0] - retorno},
            restricoes
        ]
        resultado = optimize.minimize(minimize_vol, num_acoes * [
                                      1. / num_acoes, ], method='SLSQP', bounds=limites, constraints=restricoes_ret)
        volatilidades.append(resultado['fun'])

    # Plotando a fronteira eficiente
    plt.figure(figsize=(14, 7))
    plt.scatter(df_resultados['Volatilidade Anualizada'], df_resultados['Retorno Anualizado'],
                c=df_resultados['Índice de Sharpe'], cmap='viridis')
    plt.colorbar(label='Índice de Sharpe')
    plt.plot(volatilidades, retornos_alvo, 'b--',
             linewidth=3, label='Fronteira Eficiente')
    plt.scatter(port_max_sharpe['Volatilidade Anualizada'],
                port_max_sharpe['Retorno Anualizado'], c='red', s=50, label='Máximo Sharpe')
    plt.title('Fronteira Eficiente e Portfólios Simulados')
    plt.xlabel('Volatilidade Anualizada')
    plt.ylabel('Retorno Anualizado')
    plt.legend()
    plt.show()

    # Evolução do patrimônio investido na carteira de Máximo Sharpe
    pesos_max_sharpe = port_max_sharpe[[
        ticker + ' Peso' for ticker in tickers_disponiveis]].values
    investimento_inicial = 10000  # Valor inicial investido
    alocacao = (pesos_max_sharpe * investimento_inicial)
    df_investimento = df_precos[tickers_disponiveis] * \
        alocacao / df_precos.iloc[0]
    df_investimento['Valor Total'] = df_investimento.sum(axis=1)

    # Plotando a evolução do patrimônio
    plt.figure(figsize=(14, 7))
    plt.plot(df_investimento.index,
             df_investimento['Valor Total'], label='Carteira Máximo Sharpe')
    plt.title('Evolução do Patrimônio Investido na Carteira Máximo Sharpe')
    plt.xlabel('Data')
    plt.ylabel('Valor do Patrimônio (R$)')
    plt.legend()
    plt.show()

    # Evolução do patrimônio por ação na carteira
    plt.figure(figsize=(14, 7))
    for ticker in tickers_disponiveis:
        plt.plot(df_investimento.index, df_investimento[ticker], label=ticker)
    plt.title('Evolução do Patrimônio por Ação na Carteira Máximo Sharpe')
    plt.xlabel('Data')
    plt.ylabel('Valor Investido (R$)')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
