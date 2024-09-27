import pandas as pd
import re
from src.api import fetch_planilhao_data, fetch_ibovespa_prices
from src.analise import evaluate_stocks, compare_performance
from src.utils import calculate_return


def main():
    # Carregar dados do planilhão
    planilhao_data = fetch_planilhao_data('2024-09-25')
    df_planilhao = pd.DataFrame(planilhao_data)

    # Carregar dados do IBOVESPA
    ibov_data = fetch_ibovespa_prices('2023-04-01', '2024-09-25')
    df_ibov = pd.DataFrame(ibov_data)

    # Calcular retorno do IBOVESPA
    ibov_return = calculate_return(df_ibov)

    # Análise baseada no ROE
    df_roe = df_planilhao[['ticker', 'roe', 'volume']].copy()
    df_roe['base_ticker'] = df_roe['ticker'].apply(
        lambda x: re.sub(r'\d+$', '', x))
    df_roe_filtered = df_roe.loc[df_roe.groupby(
        'base_ticker')['volume'].idxmax()].copy()
    top10_roe = df_roe_filtered[['ticker', 'roe']].sort_values(
        by='roe', ascending=False).head(10)

    # Avaliar desempenho das ações selecionadas
    roe_returns = evaluate_stocks(top10_roe, '2023-04-03', '2024-04-01')
    above_ibov_roe, below_ibov_roe = compare_performance(
        roe_returns, ibov_return)

    # Análise baseada na Magic Formula
    df_magic = df_planilhao[['setor', 'ticker',
                             'roic', 'earning_yield', 'volume']].copy()
    df_magic['base_ticker'] = df_magic['ticker'].apply(
        lambda x: re.sub(r'\d+$', '', x))
    df_magic_filtered = df_magic.loc[df_magic.groupby(
        'base_ticker')['volume'].idxmax()].copy()
    excluded_sectors = ['banco', 'seguro', 'financeiro']
    df_magic_filtered = df_magic_filtered[~df_magic_filtered['setor'].isin(
        excluded_sectors)].copy()
    df_magic_filtered = df_magic_filtered.dropna(
        subset=['roic', 'earning_yield'])
    df_magic_filtered['roic_rank'] = df_magic_filtered['roic'].rank(
        ascending=False)
    df_magic_filtered['ey_rank'] = df_magic_filtered['earning_yield'].rank(
        ascending=False)
    df_magic_filtered['combined_rank'] = df_magic_filtered['roic_rank'] + \
        df_magic_filtered['ey_rank']
    top10_magic = df_magic_filtered.sort_values(by='combined_rank').head(10)

    # Avaliar desempenho das ações selecionadas
    magic_returns = evaluate_stocks(top10_magic, '2023-04-03', '2024-04-01')
    above_ibov_magic, below_ibov_magic = compare_performance(
        magic_returns, ibov_return)

    # Exibir resultados
    print(f"Retorno do IBOVESPA: {ibov_return:.2f}%")
    print("---------------------------------------------------")
    print("Análise ROE:")
    for ticker, ret in roe_returns:
        if ret is not None:
            print(f"Retorno da ação {ticker}: {ret:.2f}%")
    roe_portfolio_return = sum(
        [r for _, r in roe_returns if r is not None]) / len(roe_returns)
    print(f"\nAções acima do IBOVESPA:")
    for ticker in above_ibov_roe:
        print(f"- {ticker}")
    print(f"\nAções abaixo do IBOVESPA:")
    for ticker in below_ibov_roe:
        print(f"- {ticker}")
    print(f"\nRetorno da carteira ROE: {roe_portfolio_return:.2f}%")
    print("---------------------------------------------------")
    print("Análise Magic Formula:")
    for ticker, ret in magic_returns:
        if ret is not None:
            print(f"Retorno da ação {ticker}: {ret:.2f}%")
    magic_portfolio_return = sum(
        [r for _, r in magic_returns if r is not None]) / len(magic_returns)
    print(f"\nAções acima do IBOVESPA:")
    for ticker in above_ibov_magic:
        print(f"- {ticker}")
    print(f"\nAções abaixo do IBOVESPA:")
    for ticker in below_ibov_magic:
        print(f"- {ticker}")
    print(f"\nRetorno da carteira Magic Formula: {
          magic_portfolio_return:.2f}%")
    print("---------------------------------------------------")
    # Comparação com o IBOVESPA
    if roe_portfolio_return > ibov_return:
        print("A carteira ROE superou o IBOVESPA! Excelente desempenho!")
    else:
        print("A carteira ROE não superou o IBOVESPA. Reavalie a estratégia.")

    if magic_portfolio_return > ibov_return:
        print("A carteira Magic Formula superou o IBOVESPA! Estratégia eficaz!")
    else:
        print("A carteira Magic Formula não superou o IBOVESPA. Reavalie a estratégia.")


if __name__ == "__main__":
    main()
