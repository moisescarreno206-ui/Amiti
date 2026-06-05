from flask import Flask, request, render_template_string
import datetime, os

app = Flask(__name__)

RED = {
    "conocimiento": ["AMITI Iniciado"],
    "logs": [{"t": "00:00", "m": "NUCLEO V9 OPERATIVO", "c": "#00ff41"}]
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
            
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "NODO: " + msg, "c": "#cccccc"})
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "AMITI: " + res, "c": "#ffffff"})
        if len(RED["logs"]) > 8: RED["logs"].pop(0)

    # Definimos el template en una sola cadena para evitar errores de sintaxis
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #000; color: #00ff41; font-family: 'Courier New', Courier, monospace; padding: 20px; font-size: 1.2rem; }
            .container { max-width: 900px; margin: auto; }
            .panel { border: 3px solid #00ff41; padding: 25px; margin-bottom: 20px; border-radius: 15px; }
            h2 { color: #00ff41; text-align: center; font-size: 2rem; }
            #logs { height: 350px; overflow-y: auto; font-size: 1.3rem; }
            select, input, button { width: 100%; padding: 20px; margin: 15px 0; background: #000; color: #00ff41; border: 3px solid #00ff41; font-size: 1.4rem; border-radius: 8px; }
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
    return render_template_string(html, RED=RED, canal=modo)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
