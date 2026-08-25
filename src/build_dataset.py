"""Regenera el dataset mensual desde las APIs, sin abrir un notebook.

Uso:
    python -m src.build_dataset
    python -m src.build_dataset --start 2015-01-01 --end 2025-02-28

Necesita FRED_API_KEY en el fichero .env de la raíz del proyecto.
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.data_extraction_processing import (
    calculate_volatility,
    clean_and_resample,
    download_market_data,
    get_fred_data,
)

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"
PROCESSED = RAIZ / "data" / "processed"

TICKERS = {"BTC-USD": "btc", "^IXIC": "nasdaq"}
SERIE_FED = "FEDFUNDS"


def obtener_api_key():
    load_dotenv(RAIZ / ".env")
    clave = os.getenv("FRED_API_KEY")
    if not clave:
        sys.exit(
            "Falta FRED_API_KEY.\n"
            "  cp .env.example .env   y añade la clave dentro.\n"
            "  Se obtiene gratis en https://fred.stlouisfed.org/docs/api/api_key.html"
        )
    return clave


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default="2015-01-01", help="fecha de inicio (YYYY-MM-DD)")
    parser.add_argument("--end", default="2025-02-28", help="fecha de fin (YYYY-MM-DD)")
    args = parser.parse_args()

    clave = obtener_api_key()
    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    print(f"Descargando {', '.join(TICKERS)} de Yahoo Finance...")
    mercado = download_market_data(TICKERS, args.start, args.end)

    print(f"Descargando {SERIE_FED} de FRED...")
    fed = get_fred_data(SERIE_FED, clave, args.start, args.end)

    mercado["btc_vol"] = calculate_volatility(mercado)
    mercado.to_csv(RAW / "market_daily.csv")
    fed.to_csv(RAW / "fed_rate.csv")

    df = clean_and_resample(mercado, fed)
    salida = PROCESSED / "btc_nasdaq_fed_monthly.csv"
    # Sin acotar la precisión, el ruido de coma flotante de la volatilidad rodante
    # cambia el último dígito en cada ejecución y ensucia el diff.
    df.to_csv(salida, float_format="%.10g")

    print(f"\n{salida.relative_to(RAIZ)}")
    print(f"  {len(df)} observaciones, de {df.index.min().date()} a {df.index.max().date()}")
    print(f"  nulos: {df.isnull().sum().sum()}")


if __name__ == "__main__":
    main()
