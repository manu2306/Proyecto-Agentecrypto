import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Cargamos el dataset que armamos en la etapa anterior
dataset = pd.read_csv("data/dataset_entrenamiento.csv")

# Juntamos titular + resumen en un solo texto por noticia (mas informacion para el modelo)
dataset["texto"] = dataset["titular"].fillna("") + " " + dataset["resumen"].fillna("")

X = dataset["texto"]       # las entradas: el texto de la noticia
y = dataset["etiqueta"]    # lo que queremos predecir: comprar / vender / mantener

# Separamos: una parte para ENTRENAR el modelo, otra para EVALUARLO despues
# (con datos que el modelo nunca vio, para ver si aprendio de verdad o solo memorizo)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Convertimos el texto en numeros (lo que vimos en la etapa anterior)
vectorizador = TfidfVectorizer(max_features=3000, stop_words="english", ngram_range=(1, 2))
X_train_vec = vectorizador.fit_transform(X_train)
X_test_vec = vectorizador.transform(X_test)

# Creamos y entrenamos el modelo
# class_weight="balanced" le da mas importancia a las categorias menos frecuentes
# (recordemos que "mantener" aparecia mas seguido que las otras)
modelo = LogisticRegression(max_iter=1000, class_weight="balanced")
modelo.fit(X_train_vec, y_train)

# Probamos el modelo con las noticias que NUNCA vio (el set de test)
predicciones = modelo.predict(X_test_vec)

print(f"Precision general (accuracy): {accuracy_score(y_test, predicciones):.2%}")
print()
print("Reporte detallado por categoria:")
print(classification_report(y_test, predicciones))

# Guardamos el modelo y el vectorizador entrenados, para poder usarlos despues
# sin tener que volver a entrenar cada vez
joblib.dump(modelo, "data/modelo_btc.pkl")
joblib.dump(vectorizador, "data/vectorizador_btc.pkl")
print("Modelo y vectorizador guardados en la carpeta data/")