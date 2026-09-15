# ₿ Agentecrypto

Proyecto universitario de "vibe coding": un modelo de Machine Learning entrenado localmente que analiza noticias de Bitcoin y sugiere si conviene **comprar**, **vender** o **mantener**, más una mini web conversacional para probarlo.

![Demo del proyecto](demo.gif)

> ⚠️ **Aviso**: este es un proyecto educativo. No es asesoramiento financiero real. Las predicciones no deben usarse para tomar decisiones de inversión.

## ¿Qué hace?

1. Descarga el precio histórico de Bitcoin en euros (últimos 365 días) desde la API de CoinGecko.
2. Descarga y filtra noticias históricas relacionadas con Bitcoin (fuentes: The Guardian, Finnhub, AlphaVantage).
3. Cruza ambos datasets: para cada noticia, mira qué hizo el precio 3 días después y le asigna una etiqueta (`comprar` / `vender` / `mantener`).
4. Convierte el texto de las noticias en números con la técnica TF-IDF.
5. Entrena un modelo de clasificación (Regresión Logística) con scikit-learn.
6. Expone el modelo en una mini aplicación web local hecha con Flask, con una interfaz tipo chat.

## Tecnologías usadas

- Python (pandas, scikit-learn, Flask, joblib, requests)
- HTML / CSS / JavaScript (para la mini web)
- Git / GitHub

## Estructura del proyecto


Agentecrypto/
├── data/ # Datos descargados y generados
├── python/
│ ├── obtener_precio_btc.py # Etapa 1: precio histórico de Bitcoin
│ ├── obtener_noticias_btc.py # Etapa 2: noticias históricas de Bitcoin
│ ├── crear_dataset_entrenamiento.py # Etapa 3: cruce de datos y etiquetado
│ ├── entrenar_modelo.py # Etapa 4: entrenamiento del modelo
│ ├── usar_modelo.py # Probar el modelo por terminal
│ ├── app.py # Mini web (Flask)
│ └── templates/
│ └── index.html
└── README.md


## Cómo correrlo en tu computadora

1. Cloná el repositorio:
git clone https://github.com/manu2306/Proyecto-Agentecrypto.git

2. Creá y activá un entorno virtual:
python -m venv venv
.\venv\Scripts\Activate.ps1

3. Instalá las dependencias:
pip install flask scikit-learn pandas requests joblib

4. Corré los scripts en orden (cada uno genera datos que usa el siguiente):
python python/obtener_precio_btc.py
python python/obtener_noticias_btc.py
python python/crear_dataset_entrenamiento.py
python python/entrenar_modelo.py

5. Levantá la web:
python python/app.py

Abrí `http://127.0.0.1:5000` en tu navegador.

## Resultado del modelo

El modelo entrenado alcanza un accuracy de entrenamiento (validación) de aproximadamente 53%. Predecir movimientos de precio de Bitcoin a partir de noticias es un problema genuinamente difícil incluso para expertos — el objetivo de este proyecto es demostrar el proceso completo de Machine Learning, no lograr un modelo de trading real.

## Autor

Manuel Corzo
