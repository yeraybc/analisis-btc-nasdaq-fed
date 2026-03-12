import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_comparative_growth(df):
    """Generamos un gráfico en Base 100 con escala logarítmica."""
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
    """Generamos un mapa de calor con máscara para evitar redundancia en la parte superior matriz."""
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