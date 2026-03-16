import pandas as pd
import pmdarima as pm
from statsmodels.stats.diagnostic import acorr_ljungbox

def fit_custom_arima(series, exog=None):
    """
    Ajusta automáticamente el mejor modelo ARIMA o ARIMAX (si hay exógenas).

    Utiliza una búsqueda exhaustiva (Stepwise=False) para comparar diferentes 
    combinaciones de órdenes (p, d, q) y seleccionar el modelo con el menor AIC.

    Args:
        series (pd.Series/np.array): Serie temporal dependiente (ej. retornos de BTC).
        exog (pd.DataFrame, optional): Variables independientes (ej. NASDAQ, FED rate). 
            Si se proporciona, el modelo se convierte en un ARIMAX.

    Returns:
        pmdarima.arima.ARIMA: El objeto del modelo ajustado con los mejores parámetros encontrados.  
    """
    model = pm.auto_arima(
        series,
        X=exog,
        stepwise=False,       
        approximation=False,   
        seasonal=False,
        error_action='ignore',
        suppress_warnings=True,
        trace=False
    )
    return model

def run_ljung_box(model_residuals, lags=24, df_adj=0):
    """
    Ejecuta el test de Ljung-Box sobre los residuos del modelo.

    Esta prueba es crítica para verificar si queda información sistemática en los 
    residuos (autocorrelación). La hipótesis nula (H0) es que los residuos son 
    independientes (ruido blanco).

    Args:
        model_residuals (pd.Series/np.array): Los residuos del modelo ajustado.
        lags (int): Número de retardos a testear (por defecto 24 para datos mensuales/diarios).
        df_adj (int): Ajuste de grados de libertad. Debe ser igual a p + q del modelo ARIMA.

    Returns:
        pd.DataFrame: Resultado del test que incluye el estadístico y el p-valor.
    """
    res = acorr_ljungbox(
        model_residuals, 
        lags=[lags], 
        model_df=df_adj, # Ajuste de grados de libertad (p+q)
        return_df=True
    )
    return res