import pandas as pd


def calculate_return(df_prices):
    """Calcula o retorno percentual baseado nos preços de fechamento ajustados."""
    df_prices['data'] = pd.to_datetime(df_prices['data'])
    df_prices = df_prices.sort_values(by='data')
    initial_price = df_prices['fechamento'].iloc[0]
    final_price = df_prices['fechamento'].iloc[-1]
    return ((final_price - initial_price) / initial_price) * 100
