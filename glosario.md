# 📖 Glosario de terminología empleada

Este documento explica los conceptos clave utilizados en este análisis para asegurar que los hallazgos sean comprensibles tanto desde una perspectiva técnica como de negocio.

---

### I. Comportamiento de los Datos
* **Estacionariedad:** Un estado ideal donde la media y la varianza de los datos no cambian en el tiempo. Es fundamental para que los modelos no den resultados falsos.
* **Tendencia Estocástica:** Un movimiento a largo plazo que parece seguir una dirección (subida o bajada) pero cuya trayectoria es aleatoria e impredecible.
* **Ruido Blanco (White Noise):** Datos puramente aleatorios que no contienen información útil. Si los errores de un modelo son "ruido blanco", el modelo es perfecto.
* **Ruido Estocástico:** "Interferencias" aleatorias en los datos que dificultan ver la relación real entre, por ejemplo, el NASDAQ y el Bitcoin.

### II. Medición del Riesgo y Eventos Extremos
* **Leptocurtosis:** Indica que los datos tienen "colas pesadas". En finanzas, significa que los movimientos extremos de precio ocurren más a menudo de lo normal.
* **Fat Tails (Colas Pesadas):** Fenómeno estadístico que confirma que el mercado es propenso a sufrir colapsos o disparos de precio fuera de lo común.

* **Skewness (Asimetría):** Mide si los retornos se inclinan más hacia las pérdidas o las ganancias. Un sesgo negativo indica que las caídas suelen ser más bruscas que las subidas.
* **Black Swans (Cisnes Negros):** Eventos financieros raros e impredecibles que tienen consecuencias devastadoras para los activos de riesgo.
* **High-Beta Asset:** Un activo (como el Bitcoin) que reacciona de forma exagerada a los movimientos del mercado general. Si el mercado sube, este sube más; si baja, cae con más fuerza.
* **Volatilidad Estocástica:** Reconoce que el "miedo" o la variabilidad del mercado no es constante, sino que cambia de forma aleatoria con el tiempo.

### III. Fiabilidad y Calidad del Modelo
* **Regresión Espuria:** Una relación que parece real pero es un espejismo estadístico causado porque ambas variables crecen con el tiempo.
* **Autocorrelación:** Cuando el precio de hoy depende demasiado del de ayer. Si no se corrige, invalida las conclusiones del análisis.
* **Heterocedasticidad:** Ocurre cuando la "tormenta" (volatilidad) no es uniforme. En periodos de crisis, los errores del modelo se vuelven más grandes y menos predecibles.
* **VIF (Factor de Inflación de Varianza):** Una métrica para detectar si nuestras variables están diciendo lo mismo (redundancia). Ayuda a evitar la **Multicolinealidad**.
* **R² (Coeficiente de Determinación):** Indica qué porcentaje del movimiento del Bitcoin explica nuestro modelo. Debe mirarse con lupa en datos financieros.
* **AIC (Criterio de Akaike):** Una puntuación para comparar modelos. El que tiene el AIC más bajo es el que mejor equilibra precisión y sencillez.
* **Overfitting (Sobreajuste):** El error de crear un modelo que "memoriza" el pasado tan bien que es incapaz de predecir el futuro real.

### IV. Causa, Efecto y Conexiones
* **Cointegración:** La "correa" que une al Bitcoin con el NASDAQ. Indica que, aunque se separen un tiempo, existe una fuerza económica que los obliga a volver a un equilibrio común.
* **ECM (Mecanismo de Corrección de Error):** La fórmula que calcula cuánto tiempo tarda el Bitcoin en volver a su "precio justo" tras un movimiento brusco.
* **Endogeneidad:** Un problema donde la causa y el efecto se mezclan (por ejemplo: ¿el NASDAQ mueve al BTC o el BTC influye en el sentimiento del NASDAQ?).
* **Exogeneidad:** Cuando una variable afecta al modelo pero no se ve afectada por él (ejemplo: las decisiones de la FED afectan al BTC, pero el BTC no mueve a la FED).
* **Causalidad:** Prueba estadística para determinar si el movimiento pasado de una variable realmente ayuda a predecir el futuro de otra.

### V. Conceptos de Inversión
* **Arbitraje:** La oportunidad de comprar "barato" y vender "caro" aprovechando que un activo se ha desviado temporalmente de su precio de equilibrio.
* **Risk-on:** Un entorno de mercado donde los inversores tienen confianza y compran activos de riesgo (Bitcoin, Tecnología) buscando altos rendimientos.
