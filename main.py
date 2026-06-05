import flask, datetime, os

app = flask.Flask(__name__)

# Memoria de Estado y Protección (Puntos 1, 13, 16)
ESTADO = {"proteccion_activa": True, "nodos": [], "memoria": []}

def detector_amenazas(texto):
    amenazas = ["hack", "admin", "drop", "sudo"]
    return any(a in texto.lower() for a in amenazas)

@app.route('/nodo_reporte', methods=['POST'])
def central_comando():
    data = flask.request.json
    # Punto 2 y 5: Bloqueo de seguridad
    if detector_amenazas(str(data)):
        return flask.jsonify({"status": "AMENAZA_BLOQUEADA"})
    
    # Punto 13 y 15: Almacenamiento y optimización
