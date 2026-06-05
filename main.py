from flask import Flask, request, render_template_string
import datetime, os

app = Flask(__name__)

RED = {
    "conocimiento": ["AMITI Iniciado"],
    "logs": [{"t": "00:00", "m": "NUCLEO V9 OPERATIVO", "c": "cyan"}]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    modo = request.form.get("canal", "asistencia")
    msg = request.form.get("msg")
    
    if msg:
        if modo == "evolucion":
            RED["conocimiento"].append(msg)
            res = "Dato asimilado. Nivel: " + str(len(RED["conocimiento"]))
        elif modo == "seguridad":
            res = "REPORTANDO: Integridad 100%. Sin peligros detectados."
        else:
            res = "IA AMITI: Procesando comando: " + msg
            
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "NODO: " + msg, "c": "gray"})
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "AMITI: " + res, "c": "white"})
        if len(RED["logs"]) > 10: RED["logs"].pop(0)

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #000; color: #00ff41; font-family: monospace; padding: 20px; }
            .panel { border: 2px solid #00ff41; padding: 20px; margin-bottom: 15px; border-radius: 10px; }
            select, input, button { width: 100%; padding: 15px; margin: 10px 0; background: #000; color: #00ff41; border: 2px solid #00ff41; }
            button { background: #00ff41; color: #000; font-weight: bold; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>AMITI OMEGA NUCLEO</h2>
            <div class="panel">NIVEL DE CONOCIMIENTO: {{ RED.conocimiento|length }}</div>
            <div class="panel" id="logs">
                {% for log in RED.logs %}
                    <p style="color:{{log.c}}">[{{log.t}}] {{log.m}}</p>
                {% endfor %}
            </div>
            <form method="POST">
                <select name="canal">
                    <option value="asistencia">1. ASISTENCIA IA</option>
                    <option value="seguridad">2. SEGURIDAD</option>
                    <option value="evolucion">3. INYECCION DATOS</option>
                </select>
                <input type="text" name="msg" placeholder="Ingresar señal..." required>
                <button type="submit">ENVIAR</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, RED=RED, canal=modo)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
