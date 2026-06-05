from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__)

# --- MEMORIA Y ESTADO ---
NODOS_CONECTADOS = {}
REGISTRO_ACTIVIDAD = []
SISTEMA_ESTADO = {"integridad": "100%", "modo": "NORMAL"}

def clasificar_y_colorear(texto):
    t = texto.lower()
    if any(x in t for x in ["cuanto es", "+", "-", "/", "*", "raiz", "potencia"]):
        return "blue", "MATEMÁTICA"
    if any(x in t for x in ["contabilidad", "saldo", "pago", "costo", "factura"]):
        return "purple", "CONTABILIDAD"
    return "#00ff41", "NORMAL"

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 15px; }
            .box { border: 1px solid #00ff41; padding: 10px; margin-bottom: 10px; }
            .MATEMÁTICA { color: #00aaff; }
            .CONTABILIDAD { color: #aa00ff; }
        </style>
    </head>
    <body>
        <h2>NÚCLEO MAESTRO: ESTADO {{estado.modo}}</h2>
        <div class="box">Nodos: {{len(nodos)}} | Integridad: {{estado.integridad}}</div>
        <div class="box">
            {% for act in actividad %}
                <p class="{{act.cat}}">[{{act.time}}] {{act.msg}}</p>
            {% endfor %}
        </div>
    </body>
    </html>
    """, nodos=NODOS_CONECTADOS, actividad=REGISTRO_ACTIVIDAD, estado=SISTEMA_ESTADO)

@app.route('/nodo_reporte', methods=['POST'])
def recibir_reporte():
    data = request.json
    msg = str(data.get('data', ''))
    
    # Comandos de Emergencia
    if "RESET_SISTEMA" in msg:
        REGISTRO_ACTIVIDAD.clear()
        return jsonify({"status": "CLEAN"})
    
    cat = clasificar_y_colorear(msg)[1]
    color = clasificar_y_colorear(msg)[0]
    
    REGISTRO_ACTIVIDAD.append({
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "msg": msg,
        "cat": cat
    })
    if len(REGISTRO_ACTIVIDAD) > 20: REGISTRO_ACTIVIDAD.pop(0)
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run()
