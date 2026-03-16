import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

def engle_granger_step1(y, x):
    """
    Primer paso de Engle-Granger: Estimación de la relación de equilibrio de largo plazo.

    Realiza una regresión por Mínimos Cuadrados Ordinarios (MCO) sobre las variables 
    en niveles para capturar la tendencia común. Los residuos de esta regresión 
    representan el 'error de equilibrio'.

    Args:
        y (pd.Series): Variable dependiente (ej. log_btc).
        x (pd.DataFrame/pd.Series): Variables independientes (ej. log_nasdaq, fed_rate).

    Returns:
        tuple: (statsmodels.regression.linear_model.RegressionResultsWrapper, pd.Series)
            - El objeto del modelo ajustado.
            - La serie de residuos ($u_t$) generada.
    """
    X = sm.add_constant(x)
    model = sm.OLS(y, X).fit()
    return model, model.resid

def adf_on_residuals(residuals):
    """
    Segundo paso de Engle-Granger: Test de raíz unitaria sobre los residuos.

    Verifica si los residuos de la regresión de largo plazo son estacionarios $I(0)$.
    Si lo son, se confirma la existencia de cointegración entre las variables.

    Args:
        residuals (pd.Series): Residuos obtenidos en el paso 1.

    Returns:
        tuple: Resultados del test ADF (estadístico, p-valor, valores críticos, etc.).
            Se utiliza 'n' (sin constante ni tendencia) porque los residuos ya 
            provienen de una regresión con intercepto.
    """
    return adfuller(residuals, regression='n', autolag='AIC')

def prepare_ecm_data(df, target, exogs, residuals):
    """
    Prepara el dataset para la estimación del Modelo de Corrección de Error (ECM).

    Calcula las primeras diferencias (dinámica de corto plazo) y alinea el 
    término de error retardado ($u_{t-1}$), que representa la velocidad de ajuste 
    hacia el equilibrio de largo plazo.

    Args:
        df (pd.DataFrame): DataFrame original con las variables en niveles.
        target (str): Nombre de la variable dependiente.
        exogs (list): Lista de nombres de las variables exógenas.
        residuals (pd.Series): Residuos de la regresión de niveles.

    Returns:
        pd.DataFrame: DataFrame transformado con las variables diferenciadas 
            ('d_') y el residuo rezagado ('u_lag').
    """
    # Dinámica de corto plazo: Primeras diferencias (dY, dX)
    df_diff = df[[target] + exogs].diff().dropna()
    df_diff.columns = [f'd_{col}' for col in df_diff.columns]
    
    # Mecanismo de corrección: Error retardado (u_{t-1})
    u_lag = residuals.shift(1).dropna()
    u_lag.name = 'u_lag'
    
    # Sincronización temporal y limpieza de nulos generados por el lag
    ecm_df = pd.concat([df_diff, u_lag], axis=1).dropna()
    return ecm_df