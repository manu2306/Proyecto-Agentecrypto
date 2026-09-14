import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# Calculamos el rango: desde hace 365 días hasta hoy
hoy = datetime.utcnow()
hace_un_anio = hoy - timedelta(days=365)

# La API pide las fechas como "timestamp" (segundos desde 1970)
desde = int(hace_un_anio.timestamp())
hasta = int(hoy.timestamp())

# Armamos el pedido a la API de CoinGecko
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"
parametros = {
    "vs_currency": "eur",
    "from": desde,
    "to": hasta
}

respuesta = requests.get(url, params=parametros)
datos = respuesta.json()

# "prices" es una lista de [timestamp_en_milisegundos, precio]
precios = datos["prices"]

# La convertimos en una tabla (DataFrame) de pandas
df = pd.DataFrame(precios, columns=["timestamp_ms", "precio_eur"])

# Convertimos el timestamp a una fecha legible
df["fecha"] = pd.to_datetime(df["timestamp_ms"], unit="ms")
df = df[["fecha", "precio_eur"]]

# Creamos la carpeta "data" si no existe, y guardamos el archivo ahí
os.makedirs("data", exist_ok=True)
df.to_csv("data/precio_bitcoin_eur.csv", index=False)

print(f"Se guardaron {len(df)} registros de precio.")
print(df.head())
print(df.tail())