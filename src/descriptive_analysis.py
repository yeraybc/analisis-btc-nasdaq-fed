import pandas as pd

def get_descriptive_stats(df):
    """Generamos estadísticos descriptivos del dataset incluyendo asimetría y curtosis."""
    # Excluimos columnas no numéricas si las hubiera para el cálculo
    stats = df.describe().T[['mean', 'std', 'min', '50%', 'max']]
    stats['skew'] = df.skew() 
    stats['kurtosis'] = df.kurtosis()
    return stats.round(2)