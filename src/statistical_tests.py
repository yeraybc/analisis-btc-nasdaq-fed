import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats

def check_stationarity(df, variables):
    """Traducción de vars_test en R. Ejecuta ADF y KPSS y devuelve una tabla de diagnóstico."""
    results = []
    for var in variables:
        # ADF (H0: No estacionaria / Tiene raíz unitaria)
        adf_res = adfuller(df[var].dropna(), regression='ct', autolag='AIC')
        
        # KPSS (H0: Estacionaria)
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
    """Ejecuta Shapiro-Wilk, Breusch-Pagan y Durbin-Watson sobre un modelo ajustado."""
    residuals = model.resid
    
    # 1. Shapiro-Wilk (Normalidad)
    sw_stat, sw_p = stats.shapiro(residuals)
    
    # 2. Breusch-Pagan (Homocedasticidad)
    # Requiere las variables exógenas del modelo
    bp_test = het_breuschpagan(residuals, model.model.exog)
    
    # 3. Durbin-Watson (Autocorrelación)
    dw_stat = durbin_watson(residuals)
    
    diagnostics = {
        'Shapiro_Pval': sw_p,
        'BP_Pval': bp_test[1],
        'DW_Stat': dw_stat
    }
    return diagnostics