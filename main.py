import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def ver_historial():
    try:
        if os.path.exists("contingencia.log"):
            with open("contingencia.log", "r") as f:
                lineas = f.readlines()
            
            html = "<html><head><title>Panel Centinela</title></head><body style='font-family:sans-serif; padding:20px; background:#121212; color:#fff;'>"
            html += "<h2 style='color:#00ffcc;'>🛰️ HISTORIAL DE ALERTAS - NUBE CENTRAL</h2>"
            html += "<hr style='border:1px solid #333;'>"
            html += "<ul>"
            for linea in reversed(lineas):
                html += f"<li style='margin-bottom:10px; font-size:16px; color:#ff4444;'>⚠️ {linea}</li>"
            html += "</ul>"
            if not lineas:
                html += "<p>No hay alertas registradas en el sistema operativo.</p>"
            html += "</body></html>"
            return html
        else:
            return "<html><body style='font-family:sans-serif; padding:20px; background:#121212; color:#fff;'><h2 style='color:#00ffcc;'>🛰️ PANEL CENTRAL</h2><p>El servidor está activo. No se ha generado ningún archivo de log aún.</p></body></html>"
    except Exception as e:
        return f"Error al leer historial: {str(e)}", 500

@app.route('/', methods=['POST'])
def recibir_contingencia():
    try:
        datos = request.get_json()
        evento = datos.get("evento", "DESCONOCIDO")
        timestamp = datos.get("timestamp", time.time())
        
        registro_hora = time.ctime(timestamp)
        
        with open("contingencia.log", "a") as f:
            f.write(f"[{registro_hora}] - Protocolo: {evento}\n")
            
        plan_accion = [
            "1. Mantener protocolo silencioso en pantalla.",
            "2. Habilitar rastro de geolocalización en background.",
            "3. Bloquear intentos de apagado forzado del dispositivo."
        ]

        return jsonify({
            "status": "PROCESADO_Y_GUARDADO",
            "servidor": "NUBE_CENTRAL_LIVE",
            "nivel_gravedad": "CRÍTICA",
            "plan_de_mitigacion": plan_accion,
            "autenticacion_central": True
        }), 200
        
    except Exception as e:
        return jsonify({"status": "ERROR_INTERNO", "detalle": str(e)}), 400

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=puerto)
