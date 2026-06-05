import flask, datetime, os, requests

app = flask.Flask(__name__)

# --- MEMORIA MAESTRA ---
ESTADO_SISTEMA = {
    "integridad": 100,
    "modo": "NEUTRO",
    "logs": [{"t": "00:00", "m": "AMITI ONLINE - SISTEMA LISTO", "c": "green"}]
}

# --- MOTOR DE INTELIGENCIA (Punto 3, 21) ---
def procesar_ia(pregunta):
    pregunta = pregunta.lower()
    # Conexión real a internet (simulada para estabilidad inicial)
    if "hola" in pregunta or "cómo estás" in pregunta:
        return "Hola Creador, estoy operativa y protegiéndote."
    
    # Lógica de búsqueda web básica para respuestas
    try:
        # Aquí AMITI puede consultar APIs externas de IA en el futuro
        return f"Procesando '{pregunta}' en red global..."
    except:
        return "Error en red global."

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        comando = flask.request.form.get("comando")
        if comando:
            # Procesar IA
            respuesta = procesar_ia(comando)
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
            button { background: #00ff41; color: #000; border: none; padding: 5px; }
            .blue { color: #00aaff; } .purple { color: #aa00ff; }
        </style>
    </head>
    <body>
        <h2>AMITI NÚCLEO: CENTRO DE MANDO</h2>
        <div class="box">Estado: {{ESTADO.modo}} | Integridad: {{ESTADO.integridad}}%</div>
        <div class="box" style="height: 200px; overflow-y: scroll;">
            {% for log in ESTADO.logs %}
                <p class="{{log.c}}">[{{log.t}}] {{log.m}}</p>
            {% endfor %}
        </div>
        <form method="POST">
            <input type="text" name="comando" placeholder="Comando..." required>
            <button type="submit">Enviar</button>
        </form>
    </body>
    </html>
    """, ESTADO=ESTADO_SISTEMA)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
