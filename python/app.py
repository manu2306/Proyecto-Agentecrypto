from flask import Flask, render_template, request, redirect, url_for
import joblib

app = Flask(__name__)

# Cargamos el modelo una sola vez, cuando arranca el servidor
modelo = joblib.load("data/modelo_btc.pkl")
vectorizador = joblib.load("data/vectorizador_btc.pkl")

# Emojis y frases para que la respuesta se sienta mas conversacional
MENSAJES = {
    "comprar": "📈 Creo que es un buen momento para COMPRAR.",
    "vender": "📉 Creo que deberias VENDER.",
    "mantener": " Creo que lo mejor es MANTENER tu posicion.",
}

# Orden fijo para mostrar siempre las 3 barras en el mismo orden
ORDEN_CATEGORIAS = ["comprar", "mantener", "vender"]

# Titulares de ejemplo para los botones rapidos
EJEMPLOS = [
    "Bitcoin surges to new highs after positive news",
    "Bitcoin price crashes as investors panic sell",
    "Bitcoin remains stable amid market uncertainty",
]

# Guardamos el historial de la conversacion en memoria (se reinicia si apagas el servidor)
conversacion = []


def predecir(titular):
    """Recibe un titular y devuelve el mensaje de respuesta y las probabilidades por categoria."""
    texto_vectorizado = vectorizador.transform([titular])
    prediccion = modelo.predict(texto_vectorizado)[0]
    probabilidades = modelo.predict_proba(texto_vectorizado)[0]

    # Armamos una lista ordenada: [{"categoria": "comprar", "porcentaje": 35}, ...]
    mapa_probabilidades = dict(zip(modelo.classes_, probabilidades))
    lista_probabilidades = [
        {"categoria": cat, "porcentaje": round(mapa_probabilidades[cat] * 100)}
        for cat in ORDEN_CATEGORIAS
    ]

    return MENSAJES[prediccion], lista_probabilidades


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        titular = request.form.get("titular", "").strip()
        if titular:
            respuesta, probabilidades = predecir(titular)

            conversacion.append({"autor": "vos", "texto": titular, "probabilidades": None})
            conversacion.append({"autor": "bot", "texto": respuesta, "probabilidades": probabilidades})

    return render_template("index.html", conversacion=conversacion, ejemplos=EJEMPLOS)


@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    conversacion.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)