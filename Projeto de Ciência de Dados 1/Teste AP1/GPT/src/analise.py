import pandas as pd
from src.api import fetch_stock_prices
from src.utils import calculate_return


def evaluate_stocks(df_stocks, start_date, end_date):
    """Avalia o retorno das ações no período especificado."""
    results = []
    for ticker in df_stocks['ticker'].unique():
        price_data = fetch_stock_prices(ticker, start_date, end_date)
        if price_data:
            df_prices = pd.DataFrame(price_data)
            stock_return = calculate_return(df_prices)
            results.append((ticker, stock_return))
        else:
            results.append((ticker, None))
    return results


def compare_performance(stock_returns, ibov_return):
    """Compara os retornos das ações com o retorno do IBOVESPA."""
    above_ibov = [ticker for ticker,
                  ret in stock_returns if ret is not None and ret > ibov_return]
    below_ibov = [ticker for ticker,
                  ret in stock_returns if ret is not None and ret <= ibov_return]
    return above_ibov, below_ibov
