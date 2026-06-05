from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos en memoria para el monitoreo
REGISTRO_ACTIVIDAD = []

@app.route('/', methods=['GET'])
def index():
    return "NÚCLEO AMITI ONLINE - SISTEMA DE MANDO ACTIVO"

@app.route('/nodo_reporte', methods=['POST'])
def recibir_reporte():
    try:
        data = request.json
        REGISTRO_ACTIVIDAD.append(data)
        return jsonify({"status": "recibido"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render asigna el puerto mediante una variable de entorno, 
    # pero si no la encuentra, usaremos el 10000 por defecto.
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
