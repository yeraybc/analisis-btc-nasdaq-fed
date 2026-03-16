import pandas as pd
import numpy as np
import yfinance as yf
from fredapi import Fred
import time 

def download_market_data(tickers_dict, start, end, max_retries=5):
    """
    Descarga datos históricos desde Yahoo Finance con un mecanismo de reintentos.

    Args:
        tickers_dict (dict): Diccionario con el mapeo {'TICKER_YF': 'nombre_columna'}.
        start (str): Fecha de inicio en formato 'YYYY-MM-DD'.
        end (str): Fecha de fin en formato 'YYYY-MM-DD'.
        max_retries (int): Número máximo de intentos en caso de error de conexión.

    Returns:
        pd.DataFrame: Precios de cierre con las columnas renombradas según el diccionario.
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
    Extrae series económicas de la base de datos FRED (Federal Reserve Economic Data).

    Args:
        series_id (str): Identificador de la serie en FRED (ej. 'FEDFUNDS').
        api_key (str): Clave de API privada del usuario.
        start (str): Fecha de inicio del periodo.
        end (str): Fecha de fin del periodo.

    Returns:
        pd.DataFrame: DataFrame con la serie económica y el índice temporal 'Date'.
    """
    fred = Fred(api_key=api_key)
    # Descargamos la serie (FEDFUNDS en tu caso)
    data = fred.get_series(series_id, observation_start=start, observation_end=end)
    
    # Convertimos a DataFrame y limpiamos
    df = pd.DataFrame(data, columns=['fed_rate'])
    df.index.name = 'Date'
    return df

def calculate_volatility(df, window=30):
    """
    Calcula la volatilidad logarítmica anualizada de un activo (BTC).

    Args:
        df (pd.DataFrame): DataFrame que debe contener la columna 'btc'.
        window (int): Ventana de días para el cálculo de la desviación estándar móvil.

    Returns:
        pd.Series: Serie con la volatilidad rodante anualizada.
    """
    # Trabajamos sobre una copia para no modificar el original por accidente
    df_temp = df.copy()
    returns = np.log(df_temp['btc'] / df_temp['btc'].shift(1))
    vol = returns.rolling(window=window).std() * np.sqrt(365)
    return vol

def clean_and_resample(df_market, df_fed):
    """
    Sincroniza activos con calendarios distintos y realiza el remuestreo mensual.

    Aplica 'Forward Fill' para alinear activos que no cotizan 24/7 (NASDAQ) 
    con los que sí lo hacen (BTC), y agrupa los datos al cierre de cada mes.

    Args:
        df_market (pd.DataFrame): Datos de precios de mercado y volatilidad.
        df_fed (pd.DataFrame): Datos de la tasa de la FED.

    Returns:
        pd.DataFrame: Dataset final limpio, sin valores nulos y con frecuencia mensual (ME).
    """
    # Sincronizamos a frecuencia diaria (Forward Fill)
    df_daily = df_market.ffill() # Hacemos que NASDAQ mantenga el precio (Viernes) durante el fin de semana -> NASDAQ (NO cotiza fin de semanas, BTC cotiza 24/7).

    # Unimos con FED y limpieza
    df_combined = df_daily.join(df_fed, how='left').ffill()

    # Resampling al cierre de mes (ME)
    df_monthly = df_combined.resample('ME').last().dropna()
    return df_monthly