from flask import Flask, request, render_template_string
import datetime, os

app = Flask(__name__)

# Memoria de Red inicializada
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

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <body>
        <h2>AMITI OMEGA NUCLEO</h2>
        <div id="logs">
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
            <input type="text" name="msg" required>
            <button type="submit">ENVIAR</button>
        </form>
    </body>
    </html>
    """, RED=RED, canal=modo)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
