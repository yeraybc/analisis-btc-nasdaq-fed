# 📈 BTC-NASDAQ-FED: Cointegration & Systematic Risk Audit
> **Análisis econométrico sobre la maduración de activos digitales y su dependencia estructural de la liquidez global.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Producci%C3%B3n-success.svg)](#)
[![Econometrics](https://img.shields.io/badge/Focus-Econometr%C3%ADa%20Avanzada-green.svg)](#)

## 🎯 1. Contexto de Negocio y Problema Financiero
Para un gestor de activos, la narrativa del Bitcoin ha transitado entre ser un 'refugio seguro' (Oro Digital) y un activo de riesgo extremo. Este proyecto utiliza un pipeline econométrico de nivel institucional para determinar si el BTC ofrece una diversificación real o si es un **amplificador de riesgo sistémico** vinculado a la liquidez del NASDAQ y las tasas de la FED.

**El objetivo:** Superar las limitaciones de la estadística convencional para encontrar la verdadera relación de equilibrio de largo plazo, eliminando sesgos como la regresión espuria y la autocorrelación.

> 📙 **Nota:** Dada la naturaleza técnica de este análisis, se recomienda consultar previamente el [Glosario de terminología empleada](./glosario.md) para una interpretación precisa de los conceptos econométricos (Cointegración, ECM, Heterocedasticidad) y de mercado (Risk-on, High-beta) utilizados.

---

## 🚀 2. Key Insights: Hallazgos Cuantificables
Métricas críticas obtenidas durante la investigación. Esta tabla resume la 'memoria técnica' del proyecto:

| Categoría | Métrica Técnica | Valor Obtenido | Impacto Táctico y de Negocio |
| :--- | :--- | :--- | :--- |
| **Sincronía de Mercado** | Correlación (Pearson) | **0.94** | **Falsa Diversificación**: El BTC actúa como un 'Nasdaq apalancado'. No reduce el riesgo sistémico. |
| **Riesgo de Cola** | Curtosis (Exceso) | **3.37** | **Riesgo de Cisne Negro**: La probabilidad de eventos extremos es 3x superior a una distribución normal. |
| **Asimetría** | Skewness (Sesgo) | **-0.16** | **Vulnerabilidad**: Las caídas son un 16% más rápidas que las subidas. Exige *Stop-Loss* agresivos. |
| **Integridad Estadística** | Durbin-Watson (DW) | **0.35** | **Alerta de Sesgo**: El 85% de la varianza en OLS es error autocorrelacionado. El modelo simple es inválido. |
| **Fiabilidad del Modelo** | R² (Coef. Determinación) | **0.879** | **Espejismo Estadístico**: Un R² alto causado por no-estacionariedad. Se requiere Cointegración para validar. |
| **Política Monetaria** | Impacto Tasa FED | **-4,884 USD** | **Sensibilidad a Liquidez**: Por cada 1% de subida en la FED, el BTC sufre un impacto negativo inmediato de ~$4.8k. |
| **Dinámica de Equilibrio** | Velocidad ECM | **-18.4% / mes** | **Reversión a la Media**: Tras un shock, el mercado tarda **~5.4 meses** en recuperar su valor fundamental. |

---

## 🛠️ 3. Metodología de Producción
El proyecto implementa un estándar de software modular, separando la lógica de investigación de la ejecución técnica:

* **Pipeline de Ingesta Robusta**: Sincronización de activos con calendarios divergentes (Crypto 24/7 vs. NYSE) y gestión de reintentos de API.
* **Validación de Estacionariedad**: Diagnóstico dual mediante tests **ADF (Augmented Dickey-Fuller)** y **KPSS** para asegurar la integridad de las series.
* **Modelado Dinámico (ARIMAX)**: Identificación de la estructura de retardos y filtrado de ruido estocástico mediante **Auto-ARIMA**.
* **Teoría de Cointegración (Engle-Granger)**: Estimación en dos pasos para identificar tendencias estocásticas comunes.
* **Modelo de Corrección de Error (ECM)**: Cuantificación de la velocidad de ajuste ante desviaciones del equilibrio de mercado.

---

## 🧰 4. Stack Tecnológico
Para garantizar la precisión de los cálculos y la robustez del análisis, se han empleado las siguientes tecnologías:

* **Econometría y Estadística**: `Statsmodels` (análisis de series temporales y diagnósticos), `Pmdarima` (automatización de modelos ARIMA).
* **Análisis y Manipulación de Datos**: `Pandas` y `NumPy` para la gestión de estructuras matriciales complejas.
* **Ingesta de Datos**: `yfinance` para datos de mercado y `FredAPI` para indicadores macroeconómicos oficiales.
* **Visualización Científica**: `Seaborn` y `Matplotlib` para la creación de reportes visuales de alta densidad informativa.

---

## 🏗️ 5. Estructura del Proyecto
```bash
├── data/               # Datasets procesados (CSV).
├── notebooks/          # Flujo narrativo de la investigación (.ipynb).
├── src/                # Motor lógico modularizado (.py).
│   ├── data_extraction_preprocessing.py
│   ├── data_visualization.py           
│   ├── descriptive_analysis.py          
│   ├── models_arima.py                  
│   ├── models_econometrics.py           
│   └── statistical_test.py              
├── .env.example        # Plantilla para variables de entorno (API Keys).
├── glosario.md         # Diccionario de terminología técnica y financiera.
├── requirements.txt    # Entorno reproducible.
└── README.md           # Resumen ejecutivo.

```

---

## 📊 6. Fuentes de Datos

La integridad del análisis se sustenta en el uso de fuentes de datos primarias reconocidas en el sector financiero:

* **Precios de Mercado (BTC & NASDAQ):** Extraídos mediante la API de `Yahoo Finance`.
* **Indicadores Macroeconómicos:** Series de la Tasa de Fondos Federales obtenidas de la base de datos `FRED` (Federal Reserve Economic Data) de la Reserva Federal de San Luis.
  
### 6.1. Obtención de Credenciales (FRED API)

Este proyecto utiliza datos oficiales de la Reserva Federal. Para automatizar la descarga:

* **Regístrese de forma gratuita** en la web de [St. Louis FED](https://fred.stlouisfed.org/docs/api/api_key.html) y solicite su **API Key**.
* **Cree un archivo** llamado `.env` en la raíz del proyecto.
* **Añada la clave** obtenida de la siguiente manera: `FRED_API_KEY=tu_clave_aqui`

---

## ⚖️ 7. Licencia

Este proyecto está bajo la **Licencia MIT**. Siéntase libre de utilizar, modificar y distribuir el código, siempre que se mantenga la atribución original del autor.
