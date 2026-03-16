import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats

def check_stationarity(df, variables):
    """
    Realiza una validación dual de estacionariedad mediante los tests ADF y KPSS.

    Cruza las hipótesis de ambos tests para ofrecer un diagnóstico robusto:
    - ADF: H0 = La serie tiene raíz unitaria (no estacionaria).
    - KPSS: H0 = La serie es estacionaria.
    
    Esta función es crítica para evitar 'regresiones espurias' y decidir si 
    las series deben ser diferenciadas antes del modelado.

    Args:
        df (pd.DataFrame): DataFrame con las series temporales.
        variables (list): Lista de columnas a testear (ej. ['btc', 'nasdaq']).

    Returns:
        pd.DataFrame: Tabla resumen con estadísticos, valores críticos al 5% y 
            un diagnóstico final interpretado.
    """
    results = []
    for var in variables:
        # ADF (H0: No estacionaria / Tiene raíz unitaria). Se incluye constante y tendencia ('ct') por la naturaleza de los activos
        adf_res = adfuller(df[var].dropna(), regression='ct', autolag='AIC')
        
        # KPSS (H0: Estacionaria). Se incluye tendencia ('ct') para evaluar estacionariedad en torno a ella
        kpss_res = kpss(df[var].dropna(), regression='ct', nlags="auto")
        
        # Lógica de diagnóstico
        t_stat = adf_res[0]
        crit_5 = adf_res[4]['5%']
        pval_kpss = kpss_res[1]
        
        if t_stat < crit_5 and pval_kpss > 0.05:
            diag = 'Estacionaria (I0)'
        elif t_stat > crit_5 and pval_kpss < 0.05:
            diag = 'No Estacionaria (I1)'
        else:
            diag = 'Inconcluso'
            
        results.append({
            'Variable': var,
            'ADF_Stat': round(t_stat, 3),
            'ADF_Crit5': round(crit_5, 3),
            'KPSS_Pval': round(pval_kpss, 3),
            'Diagnostico': diag
        })
    return pd.DataFrame(results)

def residual_diagnostics(model):
    """
    Evalúa los supuestos de Gauss-Markov sobre los residuos de un modelo.

    Ejecuta una batería de tests estadísticos para validar el modelo:
    1. Shapiro-Wilk: Test de normalidad de los residuos.
    2. Breusch-Pagan: Test de homocedasticidad (varianza constante).
    3. Durbin-Watson: Test de autocorrelación (independencia).

    Args:
        model (statsmodels.regression.linear_model.RegressionResultsWrapper): 
            Modelo ajustado sobre el cual extraer los residuos.

    Returns:
        dict: Diccionario con los p-valores y estadísticos de diagnóstico.
    """
    residuals = model.resid
    
    # Shapiro-Wilk: Buscamos p > 0.05 para asumir normalidad
    sw_stat, sw_p = stats.shapiro(residuals)
    
    # Breusch-Pagan: Buscamos p > 0.05 para asumir varianza constante
    # Requiere las variables exógenas del modelo
    bp_test = het_breuschpagan(residuals, model.model.exog)
    
    # Durbin-Watson: Buscamos un valor cercano a 2.0 para descartar autocorrelación
    dw_stat = durbin_watson(residuals)
    
    diagnostics = {
        'Shapiro_Pval': sw_p,
        'BP_Pval': bp_test[1],
        'DW_Stat': dw_stat
    }
    return diagnostics