import flask, datetime, os

app = flask.Flask(__name__)

# --- MEMORIA MAESTRA Y ESTRUCTURA DE SEGURIDAD (Puntos 1, 4, 13, 14, 15) ---
ESTADO_SISTEMA = {
    "integridad": 100,
    "modo": "NEUTRO", # PROTECCIÓN, ALERTA, EMERGENCIA
    "nodos": {},
    "logs": []
}

def filtro_seguridad(texto):
    # Punto 2, 5, 16: Protección del creador y bloqueo de agresiones
    prohibidas = ["hack", "exploit", "drop table", "sudo"]
    if any(p in texto.lower() for p in prohibidas):
        ESTADO_SISTEMA["modo"] = "EMERGENCIA"
        return False
    return True

@app.route('/', methods=['GET'])
def index():
    # Punto 11, 14: Interfaz de monitoreo estética
    return flask.render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><style>
        body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; }
        .box { border: 2px solid #00ff41; padding: 15px; margin-bottom: 20px; }
        .blue { color: #00aaff; } .purple { color: #aa00ff; }
    </style></head>
    <body>
        <h1>AMITI OMEGA NÚCLEO CENTRAL</h1>
        <div class="box">
            Integridad: {{ESTADO.integridad}}% | Modo: {{ESTADO.modo}}
        </div>
        <div class="box">
            {% for log in ESTADO.logs %}
                <p class="{{log.c}}">[{{log.t}}] {{log.m}}</p>
            {% endfor %}
        </div>
    </body>
    </html>
    """, ESTADO=ESTADO_SISTEMA)

@app.route('/nodo_reporte', methods=['POST'])
def recibir_reporte():
    data = flask.request.json
    msg = str(data.get('data', ''))
    
    # Punto 2: Seguridad antes de procesar
    if not filtro_seguridad(msg):
        return flask.jsonify({"status": "ACCESO_DENEGADO"})

    # Punto 3, 21: Asistencia real y clasificación
    color = "green"
    if "cuanto" in msg.lower() or "+" in msg: color = "blue"
    elif "contabilidad" in msg.lower(): color = "purple"

    ESTADO_SISTEMA["logs"].append({"t": datetime.datetime.now().strftime("%H:%M:%S"), "m": msg, "c": color})
    if len(ESTADO_SISTEMA["logs"]) > 20: ESTADO_SISTEMA["logs"].pop(0)
    
    return flask.jsonify({"status": "OK", "msg": "Procesado"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
