import pandas as pd
from datetime import date
import logging
logger = logging.getLogger(__name__)
from backend.apis import (get_planilhao,
                          get_preco_corrigido,
                          get_preco_diversos)

def filtrar_duplicado(df:pd.DataFrame, meio:str = None) -> pd.DataFrame:
    """
    Filtra o df das ações duplicados baseado no meio escolhido (defau

    params:
    df (pd.DataFrame): dataframe com os ticker duplicados 
    meio (str): campo escolhido para escolher qual ticker escolher (default: volume)

    return:
    (pd.DataFrame): dataframe com os ticker filtrados.
    """
    meio = meio or 'volume'
    df_dup = df[df.empresa.duplicated(keep=False)]
    lst_dup = df_dup.empresa.unique()
    lst_final = []
    for tic in lst_dup:
        tic_dup = df_dup[df_dup.empresa==tic].sort_values(by=[meio], ascending=False)['ticker'].values[0]
        lst_final = lst_final + [tic_dup]
    lst_dup = df_dup[~df_dup.ticker.isin(lst_final)]['ticker'].values
    logger.info(f"Ticker Duplicados Filtrados: {lst_dup}")
    print(f"Ticker Duplicados Filtrados: {lst_dup}")
    return df[~df.ticker.isin(lst_dup)]

def pegar_df_planilhao(data_base:date) -> pd.DataFrame:
    """
    Consulta todas as ações com os principais indicadores fundamentalistas

    params:
    data_base (date): Data Base para o cálculo dos indicadores.

    return:
    df (pd.DataFrame): DataFrame com todas as Ações.
    """
    dados = get_planilhao(data_base)
    if dados:
        dados = dados['dados']
        planilhao = pd.DataFrame(dados)
        planilhao['empresa'] = [ticker[:4] for ticker in planilhao.ticker.values]
        df = filtrar_duplicado(planilhao)
        logger.info(f"Dados do Planilhao consultados com sucesso: {data_base}")
        print(f"Dados do Planilhao consultados com sucesso: {data_base}")
        return df
    else:
        logger.info(f"Sem Dados no Planilhão: {data_base}")
        print(f"Sem Dados no Planilhão: {data_base}")
    

def pegar_df_preco_corrigido(data_ini:date, data_fim:date, carteira:list) -> pd.DataFrame:
    """
    Consulta os preços Corrigidos de uma lista de ações

    params:
    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta
    carteira (list): lista de ativos a serem consultados

    return:
    df_preco (pd.DataFrame): dataframe com os preços do período dos ativos da lista
    """
    df_preco = pd.DataFrame()
    for ticker in carteira:
        dados = get_preco_corrigido(data_ini, data_fim, ticker)
        if dados:
            dados = dados.json()['dados']
            df_temp = pd.DataFrame.from_dict(dados)
            df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True)
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')   
        else:
            logger.error(f"Sem Preco Corrigido: {ticker}")
            print(f"Sem Preco Corrigido: {ticker}")
    return df_preco

def pegar_df_preco_diversos(data_ini:date, data_fim:date, carteira:list) -> pd.DataFrame:
    """
    Consulta os preços históricos de uma carteira de ativos

    params:

    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta
    carteira (list): lista de ativos a serem consultados

    return:
    df_preco (pd.DataFrame): dataframe com os preços do período dos ativos da lista
    """
    df_preco = pd.DataFrame()
    for ticker in carteira:
        dados = get_preco_diversos(data_ini, data_fim, ticker)
        if dados:
            dados = dados.json()['dados']
            df_temp = pd.DataFrame.from_dict(dados)
            df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True)
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')   
        else:
            logger.error(f"Sem Preco Corrigido: {ticker}")
            print(f"Sem Preco Corrigido: {ticker}")
    return df_preco