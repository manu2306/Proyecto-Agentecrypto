import pandas as pd

# Cuantos dias hacia adelante miramos para ver que hizo el precio despues de la noticia
DIAS_ADELANTE = 3

# Si el precio subio mas que esto (en %), decimos "comprar"
UMBRAL_SUBIDA = 2.0
# Si el precio bajo mas que esto (en %), decimos "vender"
UMBRAL_BAJADA = -2.0

# Cargamos los dos archivos que ya tenemos
precios = pd.read_csv("data/precio_bitcoin_eur.csv", parse_dates=["fecha"])
noticias = pd.read_csv("data/noticias_bitcoin.csv", parse_dates=["fecha"])

# Los precios son uno por dia. Las noticias tienen hora exacta.
# Nos quedamos solo con el "dia" de cada noticia, para poder cruzarlas con el precio de ese dia
noticias["dia"] = noticias["fecha"].dt.normalize()
precios["dia"] = precios["fecha"].dt.normalize()

# Armamos una tabla chica: dia -> precio, facil de buscar
precio_por_dia = precios.set_index("dia")["precio_eur"]

resultados = []
for _, noticia in noticias.iterrows():
    dia_noticia = noticia["dia"]
    dia_futuro = dia_noticia + pd.Timedelta(days=DIAS_ADELANTE)

    # Si no tenemos precio para ese dia exacto (o el futuro), nos saltamos esta noticia
    if dia_noticia not in precio_por_dia.index or dia_futuro not in precio_por_dia.index:
        continue

    precio_actual = precio_por_dia[dia_noticia]
    precio_futuro = precio_por_dia[dia_futuro]

    variacion_pct = (precio_futuro - precio_actual) / precio_actual * 100

    if variacion_pct > UMBRAL_SUBIDA:
        etiqueta = "comprar"
    elif variacion_pct < UMBRAL_BAJADA:
        etiqueta = "vender"
    else:
        etiqueta = "mantener"

    resultados.append({
        "fecha": noticia["fecha"],
        "titular": noticia["titular"],
        "resumen": noticia["resumen"],
        "fuente": noticia["fuente"],
        "precio_actual": precio_actual,
        "precio_futuro": precio_futuro,
        "variacion_pct": round(variacion_pct, 2),
        "etiqueta": etiqueta,
    })

dataset = pd.DataFrame(resultados)
dataset.to_csv("data/dataset_entrenamiento.csv", index=False)

print(f"Se armaron {len(dataset)} ejemplos de entrenamiento (de {len(noticias)} noticias originales).")
print()
print("Cantidad de cada etiqueta:")
print(dataset["etiqueta"].value_counts())
print()
print(dataset.head(3))