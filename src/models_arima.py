import pandas as pd
import pmdarima as pm
from statsmodels.stats.diagnostic import acorr_ljungbox

def fit_custom_arima(series, exog=None):
    """
    Ajusta un modelo ARIMA o ARIMAX utilizando búsqueda exhaustiva (Auto-ARIMA).   
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
    Ejecuta el test de Ljung-Box para evaluar la autocorrelación en los residuos.
    """
    res = acorr_ljungbox(
        model_residuals, 
        lags=[lags], 
        model_df=df_adj, # Ajuste de grados de libertad (p+q)
        return_df=True
    )
    return res