import joblib

# Cargamos el modelo y el vectorizador que ya entrenamos y guardamos antes
modelo = joblib.load("data/modelo_btc.pkl")
vectorizador = joblib.load("data/vectorizador_btc.pkl")

print("=== Prediciendo con el modelo de Bitcoin ===")
titular = input("Escribi un titular de noticia (en ingles): ")

# Convertimos el texto que escribiste en numeros, usando el MISMO vectorizador del entrenamiento
texto_vectorizado = vectorizador.transform([titular])

# Le pedimos al modelo que prediga la categoria
prediccion = modelo.predict(texto_vectorizado)[0]

# Tambien le pedimos las probabilidades de cada categoria (que tan "seguro" esta)
probabilidades = modelo.predict_proba(texto_vectorizado)[0]

print()
print(f"Prediccion del modelo: {prediccion.upper()}")
print()
print("Nivel de confianza por categoria:")
for categoria, probabilidad in zip(modelo.classes_, probabilidades):
    print(f"  {categoria}: {probabilidad:.1%}")