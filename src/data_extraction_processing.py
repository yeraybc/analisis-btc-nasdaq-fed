import pandas as pd
import numpy as np
import yfinance as yf
from fredapi import Fred
import time 

def download_market_data(tickers_dict, start, end, max_retries=5):
    """Descargamos datos de Yahoo Finance con un maximo de 5 intentos, por si esta congestionada la API.
    """
    for attempt in range(max_retries):
        try:
            data = yf.download(list(tickers_dict.keys()), start=start, end=end)['Close']
            return data.rename(columns=tickers_dict)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            else:
                raise e

def get_fred_data(series_id, api_key, start, end):
    """
    Descargamos datos de la FRED usando la API oficial y la clave del usuario.
    """
    fred = Fred(api_key=api_key)
    # Descargamos la serie (FEDFUNDS en tu caso)
    data = fred.get_series(series_id, observation_start=start, observation_end=end)
    
    # Convertimos a DataFrame y limpiamos
    df = pd.DataFrame(data, columns=['fed_rate'])
    df.index.name = 'Date'
    return df

def calculate_volatility(df, window=30):
    """Calculamos la volatilidad logarítmica anualizada de BTC."""
    # Trabajamos sobre una copia para no modificar el original por accidente
    df_temp = df.copy()
    returns = np.log(df_temp['btc'] / df_temp['btc'].shift(1))
    vol = returns.rolling(window=window).std() * np.sqrt(365)
    return vol

def clean_and_resample(df_market, df_fed):
    """Sincronizamos calendarios variables y remuestreamos a frecuencia mensual."""
    # Sincronizamos a frecuencia diaria (Forward Fill)
    df_daily = df_market.ffill() # Hacemos que NASDAQ mantenga el precio (Viernes) durante el fin de semana -> NASDAQ (NO cotiza fin de semanas, BTC cotiza 24/7).

    # Unimos con FED y limpieza
    df_combined = df_daily.join(df_fed, how='left').ffill()

    # Resampling al cierre de mes (ME)
    df_monthly = df_combined.resample('ME').last().dropna()
    return df_monthly