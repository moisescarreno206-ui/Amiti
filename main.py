import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def recibir_contingencia():
    try:
        datos = request.get_json()
        evento = datos.get("evento", "DESCONOCIDO")
        timestamp = datos.get("timestamp", time.time())
        
        print(f"\n[ALERTA CENTRAL] Datos recibidos en la nube.")
        print(f"[EVENTO]: {evento}")
        print(f"[REGISTRO]: {time.ctime(timestamp)}")
        
        with open("contingencia.log", "a") as f:
            f.write(f"[{time.ctime(timestamp)}] - Protocolo activado: {evento}\n")
            
        return jsonify({
            "status": "PROCESADO_Y_GUARDADO",
            "servidor": "NUBE_CENTRAL_LIVE",
            "autenticacion": True
        }), 200
        
    except Exception as e:
        return jsonify({"status": "ERROR_INTERNO", "detalle": str(e)}), 400

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=puerto)
