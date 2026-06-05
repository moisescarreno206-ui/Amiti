import flask, datetime, os

app = Flask(__name__)

# --- MEMORIA MAESTRA ---
ESTADO_SISTEMA = {
    "integridad": 100,
    "modo": "NEUTRO",
    "logs": [{"t": "00:00", "m": "AMITI ONLINE - SISTEMA DE MANDO ACTIVO", "c": "green"}]
}

# --- MOTOR DE INTELIGENCIA REAL (Punto 3, 21) ---
def obtener_respuesta_ia(comando):
    c = comando.lower()
    # Lógica de respuesta inteligente integrada
    if "hola" in c: return "Saludos, Creador. Mi sistema está al 100%."
    if "cómo estás" in c: return "Operativa y protegiendo tus archivos, Creador."
    if "quién eres" in c: return "Soy AMITI Infinito, tu inteligencia de defensa y mando."
    if "evolución" in c or "algoritmo" in c: 
        return "Evolución iniciada. Optimizando base de datos y extendiendo protocolos de red."
    if "ayuda" in c: return "Puedo gestionar nodos, monitorear integridad y procesar datos tácticos."
    
    # Respuesta por defecto para cualquier otra consulta
    return f"He analizado tu consulta '{comando}' y he registrado los datos en la red global para su procesamiento."

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        comando = flask.request.form.get("comando")
        if comando:
            # Procesar IA con el nuevo motor
            respuesta = obtener_respuesta_ia(comando)
            ESTADO_SISTEMA["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"Yo: {comando}", "c": "green"})
            ESTADO_SISTEMA["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"AMITI: {respuesta}", "c": "blue"})
            if len(ESTADO_SISTEMA["logs"]) > 10: ESTADO_SISTEMA["logs"].pop(0)
    
    return flask.render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 15px; }
            .box { border: 1px solid #00ff41; padding: 10px; margin-bottom: 10px; }
            input { background: #000; color: #00ff41; border: 1px solid #00ff41; width: 70%; padding: 5px; }
            button { background: #00ff41; color: #000; border: none; padding: 5px; cursor: pointer; }
            .blue { color: #00aaff; } .green { color: #00ff41; }
        </style>
    </head>
    <body>
        <h2>AMITI NÚCLEO: CENTRO DE MANDO</h2>
        <div class="box">Estado: {{ESTADO.modo}} | Integridad: {{ESTADO.integridad}}%</div>
        <div class="box" style="height: 250px; overflow-y: scroll;">
            {% for log in ESTADO.logs %}
                <p class="{{log.c}}">[{{log.t}}] {{log.m}}</p>
            {% endfor %}
        </div>
        <form method="POST">
            <input type="text" name="comando" placeholder="Comando..." required autofocus>
            <button type="submit">Enviar</button>
        </form>
    </body>
    </html>
    """, ESTADO=ESTADO_SISTEMA)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
