import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# Direccion del archivo con las noticias (dataset publico en GitHub)
url = "https://media.githubusercontent.com/media/mouadja02/bitcoin-news-data/main/bitcoin-news.tsv"

print("Descargando noticias, puede tardar unos segundos...")
respuesta = requests.get(url)

# Guardamos el archivo tal cual llega (formato TSV = como un CSV pero separado por tabs)
os.makedirs("data", exist_ok=True)
ruta_temporal = "data/bitcoin-news.tsv"
with open(ruta_temporal, "wb") as f:
    f.write(respuesta.content)

# Leemos el archivo con pandas. sep="\t" le dice que las columnas estan separadas por tabulaciones
# on_bad_lines="skip" descarta las pocas filas que vienen mal formadas (texto raro en algunos resumenes)
df = pd.read_csv(ruta_temporal, sep="\t", on_bad_lines="skip")

# Convertimos la columna de fecha a un formato de fecha real (no texto)
df["DATETIME"] = pd.to_datetime(df["DATETIME"], errors="coerce")

# Nos quedamos solo con el ultimo año, para que coincida con nuestros datos de precio
hoy = datetime.utcnow()
hace_un_anio = hoy - timedelta(days=365)
df = df[(df["DATETIME"] >= hace_un_anio) & (df["DATETIME"] <= hoy)]

# Nos quedamos solo con noticias que mencionan "bitcoin" o "btc" en el titulo o el resumen
mascara = (
    df["HEADLINE"].str.contains("bitcoin|btc", case=False, na=False)
    | df["SUMMARY"].str.contains("bitcoin|btc", case=False, na=False)
)
df = df[mascara]

# Elegimos y renombramos las columnas que nos interesan
df = df[["DATETIME", "HEADLINE", "SUMMARY", "SOURCE"]]
df.columns = ["fecha", "titular", "resumen", "fuente"]

# Guardamos el resultado limpio
df.to_csv("data/noticias_bitcoin.csv", index=False)

# Borramos el archivo temporal grande, ya no lo necesitamos
os.remove(ruta_temporal)

print(f"Se guardaron {len(df)} noticias relacionadas con Bitcoin.")
print(df.head())
print(df.tail())