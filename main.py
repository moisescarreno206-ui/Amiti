from flask import Flask, request, render_template_string
import datetime, os, hashlib

app = Flask(__name__)

# CONFIGURACION DE ACCESO
# Sustituye 'TU_IP_PUBLICA' por la IP desde la que te conectas habitualmente
IP_ADMIN = "123.45.67.89" 

RED = {
    "nodos": {},
    "logs": [{"t": "00:00", "m": "NUCLEO OMEGA V10: SISTEMAS ACTIVOS", "c": "#00ff41"}]
}

def obtener_color(ip):
    return "#" + hashlib.md5(ip.encode()).hexdigest()[:6]

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    es_admin = (ip == IP_ADMIN)
    
    canal = request.form.get("canal", "asistencia")
    msg = request.form.get("msg")
    
    if msg:
        # Registro lógico
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "NODO " + ip[-4:] + ": " + msg, "c": "#ffffff"})
        
        # LOGICA SEGUN PRIVILEGIOS
        if es_admin:
            res = "MAESTRO: Comando ejecutado en canal " + canal
        else:
            res = "CLIENTE: Solicitud recibida y en cola."
        
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "AMITI: " + res, "c": "#00ff41"})
        if len(RED["logs"]) > 6: RED["logs"].pop(0)

    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: #000; color: #00ff41; font-family: monospace; padding: 20px; }
            .panel { border: 3px solid #00ff41; padding: 20px; border-radius: 10px; }
            select, input, button { width: 100%; padding: 20px; margin: 10px 0; background: #111; color: #fff; border: 2px solid #00ff41; }
        </style>
    </head>
    <body>
        <h2>{{ "AMITI NUCLEO MAESTRO" if es_admin else "AMITI INTERFAZ PUBLICO" }}</h2>
        
        <div class="panel">
            {% for log in RED.logs %}
                <p style="color:{{log.c}}">{{log.m}}</p>
            {% endfor %}
        </div>

        <form method="POST">
            {% if es_admin %}
            <select name="canal">
                <option value="asistencia">1. ASISTENCIA</option>
                <option value="seguridad">2. SEGURIDAD</option>
                <option value="evolucion">3. EVOLUCION</option>
                <option value="monitor">4. MONITOR MAESTRO</option>
            </select>
            {% endif %}
            <input type="text" name="msg" placeholder="Transmisión..." required>
            <button type="submit">TRANSMITIR</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(template, RED=RED, es_admin=es_admin)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
