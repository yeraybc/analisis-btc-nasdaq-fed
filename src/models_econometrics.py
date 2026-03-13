import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

def engle_granger_step1(y, x):
    """
    1: Regresión de largo plazo (MCO en niveles).
    2: Generación de residuos para test de cointegración.
    """
    X = sm.add_constant(x)
    model = sm.OLS(y, X).fit()
    return model, model.resid

def adf_on_residuals(residuals):
    """
    3: Test ADF sobre residuos.
    """
    return adfuller(residuals, regression='n', autolag='AIC')

def prepare_ecm_data(df, target, exogs, residuals):
    """
    Prepara el dataframe para el Modelo de Corrección de Error (ECM).
    Alinea las diferencias (corto plazo) con el error retardado (largo plazo).
    """
    # Diferencias (dY, dX)
    df_diff = df[[target] + exogs].diff().dropna()
    df_diff.columns = [f'd_{col}' for col in df_diff.columns]
    
    # Error retardado (u_{t-1})
    u_lag = residuals.shift(1).dropna()
    u_lag.name = 'u_lag'
    
    # Unir y limpiar
    ecm_df = pd.concat([df_diff, u_lag], axis=1).dropna()
    return ecm_df