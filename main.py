import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def ver_historial():
    try:
        if os.path.exists("contingencia.log"):
            with open("contingencia.log", "r", encoding="utf-8") as f:
                lineas = f.readlines()
        else:
            lineas = []

        html = """
        <html>
        <head>
            <title>Panel Centinela OS</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 20px; }
                h2 { color: #58a6ff; border-bottom: 2px solid #21262d; padding-bottom: 10px; }
                .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 15px; margin-bottom: 15px; }
                .danger { color: #f85149; font-weight: bold; }
                .geo { color: #56d364; }
                .footer { font-size: 0.8em; color: #8b949e; margin-top: 30px; text-align: center; }
            </style>
        </head>
        <body>
            <h2>🛰️ HISTORIAL DE ALERTAS - NUBE CENTRAL</h2>
        """

        if not lineas:
            html += "<p style='color:#8b949e;'>[SISTEMA LIMPIO] No hay alertas registradas en la base de datos.</p>"
        else:
            for linea in reversed(lineas):
                if "||" in linea:
                    partes = linea.strip().split("||")
                    tiempo_str = partes[0]
                    protocolo = partes[1]
                    lat = partes[2]
                    lon = partes[3]
                    
                    html += f"""
                    <div class="card">
                        <span class="danger">⚠️ [{tiempo_str}] - TRANSMISIÓN DISPARADA</span><br>
                        <span>🛡️ <b>Protocolo:</b> {protocolo}</span><br>
                        <span class="geo">📍 <b>Ubicación:</b> Lat {lat}, Lon {lon}</span>
                    </div>
                    """
                else:
                    html += f'<div class="card"><span class="danger">{linea.strip()}</span></div>'

        html += """
            <div class="footer">Centinela IA Network Security © 2026</div>
        </body>
        </html>
        """
        return html
    except Exception as e:
        return f"Error en la base de datos central: {str(e)}"


@app.route('/', methods=['POST'])
def recibir_contingencia():
    try:
        datos = request.get_json()
        evento = datos.get("evento", "DESCONOCIDO")
        protocolo = datos.get("protocolo", "DESCONOCIDO")
        lat = datos.get("latitud", "0.0")
        lon = datos.get("longitud", "0.0")
        timestamp = datos.get("timestamp", time.time())
        
        tiempo_legible = time.ctime(timestamp)
        
        # Guardamos en la base de datos usando un separador estructural
        with open("contingencia.log", "a", encoding="utf-8") as f:
            f.write(f"{tiempo_legible}||{protocolo}||{lat}||{lon}\n")
            
        print(f"[NUBE ALERTA] Recibido: {evento} - Protocolo: {protocolo} - Ubicación: {lat}, {lon}")
        
        return jsonify({
            "status": "PROCESADO_Y_GUARDADO",
            "servidor": "NUBE_CENTINELA_ALPHA"
        }), 200
    except Exception as e:
        return jsonify({"status": "ERROR_INTERNO", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
