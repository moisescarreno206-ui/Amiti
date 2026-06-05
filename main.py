from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos en memoria
ACTIVIDAD = []

@app.route('/', methods=['GET'])
def index():
    # Respuesta simple para verificar conexión
    return "NÚCLEO AMITI ONLINE - SISTEMA DE MANDO ACTIVO"

@app.route('/nodo_reporte', methods=['POST'])
def recibir_reporte():
    try:
        data = request.json
        ACTIVIDAD.append(data)
        return jsonify({"status": "recibido"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Esto es necesario para arranque local y algunas configuraciones de Render
    app.run(host='0.0.0.0', port=10000)
    
