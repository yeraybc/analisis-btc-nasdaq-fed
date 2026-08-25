# BTC · NASDAQ · FED

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CI](https://github.com/yeraybc/analisis-btc-nasdaq-fed/actions/workflows/ci.yml/badge.svg)](https://github.com/yeraybc/analisis-btc-nasdaq-fed/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Last commit](https://img.shields.io/github/last-commit/yeraybc/analisis-btc-nasdaq-fed)

Análisis econométrico de series temporales sobre la relación entre Bitcoin, el NASDAQ y los tipos de la Reserva Federal, entre 2015 y 2025.

## Índice

- [Motivación detrás del proyecto](#motivación-detrás-del-proyecto)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Fuente de datos](#fuente-de-datos)
- [Metodología](#metodología)
- [Resultados](#resultados)
- [Stack técnico](#stack-técnico)
- [Limitaciones reconocidas](#limitaciones-reconocidas)
- [Cómo ejecutar el proyecto en local](#cómo-ejecutar-el-proyecto-en-local)
- [Autor](#autor)
- [Licencia](#licencia)

## Motivación detrás del proyecto

La narrativa sobre el Bitcoin lleva años oscilando entre dos etiquetas incompatibles: refugio de valor descorrelacionado del mercado, u activo de riesgo que amplifica los movimientos de la renta variable. La pregunta tiene consecuencias prácticas: si es lo primero, añadirlo a una cartera reduce el riesgo; si es lo segundo, lo concentra justo cuando peor viene.

El problema es que la vía rápida para responderla (correlacionar las series de precios y hacer una regresión) da una respuesta equivocada. Bitcoin y NASDAQ correlacionan a 0.94 en niveles, y un OLS explica el 88 % de la varianza. Ese resultado es engañoso, ya que las dos series comparten una tendencia, y eso basta para producir un ajuste entre variables que podrían no tener ninguna relación.

> **Hallazgo principal:** los indicios de regresión espuria son inequívocos (Durbin-Watson de 0.36 sobre un R² de 0.879), pero al aplicar el contraste correcto la relación **resiste**. Las series cointegran: existe un equilibrio real de largo plazo, y las desviaciones se corrigen a un ritmo del 18,4 % mensual. Bitcoin NO es un activo descorrelacionado; está anclado al NASDAQ por una relación estructural, NO por una coincidencia de tendencias.

## Estructura del proyecto

```
analisis-btc-nasdaq-fed/
├── notebooks/                              # La investigación, en orden de ejecución
│   ├── 01_data_extraction_processing.ipynb # Ingesta de APIs y construcción del dataset
│   ├── 02_exploratory_data_analysis.ipynb  # EDA, descriptivos y correlaciones
│   ├── 03_statistical_tests_and_ols.ipynb  # Raíces unitarias, OLS y sus diagnósticos
│   ├── 04_arima_arimax_modeling.ipynb      # ARIMA y ARIMAX con exógenas
│   └── 05_cointegration_and_causality.ipynb # Engle-Granger, ECM e IV-2SLS
├── src/                                    # Funciones que usan los notebooks
│   ├── data_extraction_processing.py       # Descarga de Yahoo Finance y FRED
│   ├── data_visualization.py               # Gráficos y diagnósticos visuales
│   ├── descriptive_analysis.py             # Estadísticos descriptivos
│   ├── statistical_tests.py                # ADF, KPSS, Breusch-Pagan, Durbin-Watson
│   ├── models_arima.py                     # Auto-ARIMA y Ljung-Box
│   └── models_econometrics.py              # Engle-Granger y preparación del ECM
├── data/
│   ├── raw/                                # Descarga bruta de las APIs (no versionada)
│   └── processed/
│       └── btc_nasdaq_fed_monthly.csv      # Dataset final, versionado
├── .github/
│   ├── workflows/ci.yml                    # Verificación en cada push y PR
│   └── scripts/check.py                    # Sintaxis y dependencias, sin instalar el stack
├── .env.example                            # Plantilla de credenciales
├── requirements.txt
├── LICENSE
└── README.md
```

La separación `raw/` / `processed/` es la línea entre lo que se descarga y lo que se deriva. `data/raw/` recibe la descarga bruta de las APIs y no se versiona, porque es regenerable. `data/processed/` guarda el dataset mensual final y **sí se versiona**: son 122 filas y 8 KB, y tenerlo en el repositorio permite que los notebooks 02 a 05 se ejecuten sobre un clon recién hecho sin necesidad de una clave de API. Solo el notebook 01, que es el que descarga, la necesita.

## Fuente de datos

| Serie | Origen | Frecuencia original |
|---|---|---|
| Precio de Bitcoin (`btc`) | Yahoo Finance, `BTC-USD` | Diaria, 24/7 |
| Índice NASDAQ (`nasdaq`) | Yahoo Finance, `^IXIC` | Diaria, días hábiles NYSE |
| Volatilidad de BTC (`btc_vol`) | Calculada sobre los retornos diarios | Diaria |
| Tipo de los fondos federales (`fed_rate`) | FRED, serie `FEDFUNDS` | Mensual |

El dataset final cubre de enero de 2015 a febrero de 2025: 122 observaciones mensuales, sin valores ausentes.

La frecuencia mensual no es una preferencia estética, es una restricción de los datos. `FEDFUNDS` se publica mensualmente, así que es la serie que marca el límite superior de resolución del análisis. Además resuelve un problema de calendarios: Bitcoin cotiza los 365 días del año y el NASDAQ solo en días hábiles, de modo que cualquier análisis diario obliga a decidir qué hacer con los fines de semana. Al agregar a cierre de mes esa asimetría desaparece.

## Metodología

1. **Ingesta y sincronización.** Descarga de ambas APIs con reintentos, cálculo de la volatilidad y remuestreo a frecuencia mensual, resolviendo el desajuste entre el calendario cripto y el bursátil.
2. **Análisis exploratorio.** Descriptivos con asimetría y curtosis, crecimiento comparado en base 100 sobre escala logarítmica y matriz de correlaciones.
3. **Contraste de estacionariedad.** Validación dual con ADF y KPSS. Se cruzan ambos porque sus hipótesis nulas son opuestas, y coincidir en el diagnóstico es más fiable que fiarse de uno solo.
4. **OLS en niveles y diagnóstico.** Se estima la regresión ingenua no para creérsela, sino para someterla a Durbin-Watson, Breusch-Pagan y Shapiro-Wilk y documentar por qué no se sostiene.
5. **Modelado dinámico.** ARIMA sobre la serie univariante y ARIMAX incorporando NASDAQ y tipo FED como exógenas, con selección de órdenes por AIC y validación de residuos mediante Ljung-Box.
6. **Cointegración y corrección de error.** Engle-Granger en dos pasos: ADF sobre los residuos del equilibrio de largo plazo, y ECM para medir la velocidad de ajuste. Se añade una estimación IV-2SLS instrumentando el NASDAQ para atender la endogeneidad.

## Resultados

Todas las cifras proceden de los outputs de los notebooks de este repositorio.

| Qué se mide | Resultado | Lectura |
|---|---|---|
| Correlación BTC-NASDAQ en niveles | **0.9375** | Sincronía aparente casi perfecta |
| La misma, sobre retornos mensuales | **0.34** | La sincronía real es mucho menor |
| R² del OLS en niveles | **0.879** | Ajuste altísimo, y sospechoso |
| Durbin-Watson de ese OLS | **0.3603** | Autocorrelación residual severa (ρ ≈ 0.82) |
| ADF sobre los residuos del equilibrio | **−3.9102** (crítico 5 %: −1.9435) | Los residuos son estacionarios: **cointegran** |
| Velocidad de ajuste del ECM | **−0.1840** (p = 0.001) | Se corrige el 18,4 % de la desviación cada mes |
| Efecto del tipo FED en niveles | −291,80 $ (p = 0.558) | No significativo |
| Efecto del tipo FED en diferencias (ECM) | **−5.270,78 $** (p = 0.031) | Sí significativo |

### El R² alto no es el hallazgo

Un R² de 0.879 acompañado de un Durbin-Watson de 0.36 es algo clásico de una regresión espuria. Durbin-Watson se mueve entre 0 y 4, y el valor neutro es 2; un 0.36 implica una autocorrelación residual de en torno a 0.82. Dicho de otro modo: los errores del modelo no son ruido, arrastran memoria de un mes a otro. Los tests lo confirman por otras dos vías, con Breusch-Pagan rechazando la homocedasticidad (p < 0.001) y Shapiro-Wilk la normalidad (p = 0.0035).

La consecuencia práctica es que los errores estándar de esa regresión no valen, y por tanto tampoco valen sus contrastes de significatividad. Cualquier conclusión de inversión extraída de ahí estaría construida sobre una inferencia errónea.

El contraste de las correlaciones lo enseña de forma más directa: 0.94 en niveles frente a 0.34 en retornos mensuales. La primera mide sobre todo que ambas series suben con el tiempo. La segunda mide lo que de verdad importa a una cartera, que es si se mueven juntas mes a mes.

### Qué aporta la cointegración

Que dos series no estacionarias correlacionen no significa nada, pero si una combinación lineal de ellas **sí** es estacionaria, entonces comparten una tendencia estocástica común y la relación es real.

El ADF sobre los residuos del equilibrio de largo plazo da −3.9102, por debajo del valor crítico al 5 % (−1.9435) y también al 1 % (−2.5846). Los residuos son estacionarios y las series cointegran, así que la relación entre BTC y NASDAQ sobrevive al contraste que tumbaba al OLS.

El modelo de corrección de error cuantifica la dinámica: el coeficiente del término de corrección es −0.1840 y es significativo (p = 0.001). Cada mes se corrige el 18,4 % de la desviación respecto al equilibrio, lo que sitúa el tiempo medio de ajuste en torno a los **5,4 meses**. El signo negativo es lo que confirma que el mecanismo es estabilizador: cuando el Bitcoin se despega de su relación de largo plazo con el NASDAQ, tiende a volver.

### El tipo de interés solo aparece al diferenciar

El detalle más interesante es que el tipo FED **no es significativo en la regresión en niveles** (p = 0.558) y **sí lo es dentro del ECM, en diferencias** (−5.270,78 $ por punto porcentual, p = 0.031).

No es una contradicción, es exactamente lo que predice la teoría. En niveles, el efecto del tipo queda absorbido por la tendencia común que domina a las tres series. Al diferenciar, esa tendencia se elimina y emerge lo que quedaba tapado: lo que mueve al Bitcoin no es el nivel del tipo de interés, sino su **variación**. Es decir, los cambios en las condiciones de liquidez, no la liquidez en sí.

## Stack técnico

- **Lenguaje:** Python 3.13
- **Econometría:** `statsmodels`, `pmdarima`, `linearmodels`, `scipy`
- **Datos:** `pandas`, `numpy`, `yfinance`, `fredapi`
- **Visualización:** `matplotlib`, `seaborn`

## Limitaciones reconocidas

- **Un solo ciclo monetario.** La ventana 2015-2025 cubre tipos en el suelo, la subida agresiva de 2022 y el inicio de la bajada, pero es un único ciclo. La relación estimada podría no ser estable en otro régimen.
- **122 observaciones.** La frecuencia mensual viene impuesta por `FEDFUNDS`, y deja una muestra corta. Los contrastes de raíz unitaria son conocidos por su baja potencia en muestras de este tamaño, de modo que el diagnóstico de estacionariedad de alguna serie queda inconcluso al cruzar ADF y KPSS.
- **Engle-Granger admite un único vector de cointegración.** Con tres variables podría haber más de una relación de equilibrio. Contrastarlo exigiría el procedimiento de Johansen, que queda fuera del alcance de este trabajo.
- **`FEDFUNDS` es un proxy imperfecto de liquidez global.** El tipo de referencia no captura los programas de balance ni la política monetaria de otros bancos centrales, que también mueven la liquidez que llega a los activos de riesgo.
- **Esto no es una estrategia de inversión.** El análisis describe una relación histórica, no predice precios ni se ha validado fuera de muestra con criterio de inversión.

## Cómo ejecutar el proyecto en local

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/yeraybc/analisis-btc-nasdaq-fed.git
   cd analisis-btc-nasdaq-fed
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta el análisis.** Los notebooks 02 a 05 funcionan directamente sobre un clon recién hecho, porque el dataset está versionado en `data/processed/`:
   ```bash
   jupyter lab notebooks/
   ```

4. **Regenera el dataset** (opcional). Solo hace falta si quieres extender la ventana temporal o actualizar los datos. El notebook 01 es el único que llama a las APIs, y para FRED necesita una clave:
   ```bash
   cp .env.example .env    # y añade tu FRED_API_KEY
   ```
   La clave se solicita gratis en [FRED](https://fred.stlouisfed.org/docs/api/api_key.html), registrándose en la web de la Reserva Federal de San Luis. Yahoo Finance no requiere credenciales.

## Autor

**Yeray Benito Calviño**
Data Science student, Universidad Complutense de Madrid
[LinkedIn](https://www.linkedin.com/in/yeraybenit0) · [GitHub](https://github.com/yeraybc)

## Licencia

Distribuido bajo licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
