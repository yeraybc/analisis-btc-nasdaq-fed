import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import statsmodels.api as sm 
from statsmodels.stats.outliers_influence import variance_inflation_factor

def plot_comparative_growth(df):
    """Genera un gráfico en Base 100 con escala logarítmica."""
    base_100 = df[['btc', 'nasdaq']].divide(df[['btc', 'nasdaq']].iloc[0]) * 100
    
    plt.figure(figsize=(12, 6))
    plt.plot(base_100.index, base_100['btc'], label='Bitcoin (Base 100)', lw=2)
    plt.plot(base_100.index, base_100['nasdaq'], label='NASDAQ (Base 100)', ls='--')
    plt.yscale('log')
    plt.title('Crecimiento Comparado: BTC vs NASDAQ (Escala Log)', fontsize=14)
    plt.ylabel('Índice (Base 100)')
    plt.legend()
    plt.show()

def plot_correlation_heatmap(df):
    """Genera un mapa de calor con máscara para evitar redundancia en la parte superior matriz."""
    plt.figure(figsize=(8, 6))
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', linewidths = 0.5)
    plt.title('Matriz de Correlación de Pearson')
    plt.show()

def plot_scatter_btc_analysis(df, x_col, title, color):
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x=x_col, y='btc', 
                scatter_kws={'alpha':0.4, 'color':color}, 
                line_kws={'color':'red'})
    plt.title(title, fontsize=14)
    plt.show()

def plot_vif(df, target):
    """Calcula y grafica el Factor de Inflación de Varianza (VIF)."""
    X = df.drop(columns=[target])
    X = sm.add_constant(X) # VIF requiere una constante
    
    vif_data = pd.DataFrame()
    vif_data["Variable"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
    
    # Quitamos la constante para el gráfico
    vif_data = vif_data[vif_data['Variable'] != 'const']
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x='VIF',
                y='Variable', 
                data=vif_data.sort_values('VIF'), 
                hue='Variable',
                palette='viridis')
    plt.axvline(x=5, color='red', linestyle='--', label='Umbral Sugerido (5)')
    plt.title('Factor de Inflación de Varianza (VIF)')
    plt.legend()
    plt.show()

def plot_residuals_qq(model):
    """Genera el Q-Q Plot de los residuos (Traducción de ggplot + stat_qq)."""
    plt.figure(figsize=(8, 6))
    sm.qqplot(model.resid, line='s', fit=True)
    plt.title('Q-Q Plot de los Residuos')
    plt.show()