import pandas as pd

def get_descriptive_stats(df):
    """
    Genera un resumen estadístico exhaustivo centrado en la forma de la distribución.

    Además de las métricas de tendencia central y dispersión, calcula la asimetría 
    y la curtosis para identificar la presencia de 'Fat Tails' (colas pesadas) 
    y falta de normalidad en los activos.

    Args:
        df (pd.DataFrame): DataFrame con las variables numéricas del estudio 
            (btc, nasdaq, btc_vol, fed_rate).

    Returns:
        pd.DataFrame: Tabla de estadísticos descriptivos transpuesta y redondeada 
            a dos decimales para mejorar la legibilidad en el portfolio.
    """
    # Excluimos columnas no numéricas si las hubiera para el cálculo. Selección de métricas estándar de dispersión y tendencia
    stats = df.describe().T[['mean', 'std', 'min', '50%', 'max']]

    # Incorporación de métricas de forma (cruciales para el análisis de riesgo)
    stats['skew'] = df.skew() 
    stats['kurtosis'] = df.kurtosis()
    return stats.round(2)