from sklearn.feature_extraction.text import TfidfVectorizer

# Un par de "noticias" de ejemplo, para entender como funciona esto
noticias_ejemplo = [
    "Bitcoin sube fuerte tras noticias positivas",
    "El precio de Bitcoin cae por miedo del mercado",
    "Bitcoin se mantiene estable esta semana",
]

vectorizador = TfidfVectorizer()

# fit_transform aprende el vocabulario y convierte el texto en numeros, todo junto
matriz = vectorizador.fit_transform(noticias_ejemplo)

# Vemos que palabras aprendio (su "vocabulario")
print("Palabras que reconocio:")
print(vectorizador.get_feature_names_out())

print()
print("Cada noticia convertida en numeros (una fila por noticia):")
print(matriz.toarray())