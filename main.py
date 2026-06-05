from flask import Flask, request, render_template_string
import datetime, os, hashlib

app = Flask(__name__)

# Memoria Estructural
RED = {
    "nodos": {}, 
    "logs": [{"t": "00:00", "m": "NUCLEO OMEGA V10: SISTEMAS ACTIVOS", "c": "#00ff41"}]
}

def obtener_color(ip):
    # Genera una firma de color única por IP
    return "#" + hashlib.md5(ip.encode()).hexdigest()[:6]

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    color = obtener_color(ip)
    
    # Registro de nodo
    if ip not in RED["nodos"]:
        RED["nodos"][ip] = {"acciones": 0}
    
    canal = request.form.get("canal", "asistencia")
    msg = request.form.get("msg")
    
    if msg:
        RED["nodos"][ip]["acciones"] += 1
        
        # LOGICA DE CANALES REAL
        if canal == "monitor":
            res = "MONITOR: Analizando integridad de nodo " + ip[-4:]
        elif canal == "evolucion":
            res = "EVOLUCION: Datos integrados al nucleo. Aprendizaje activo."
        else:
            res = "ASISTENCIA: Procesando consulta."
            
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "NODO " + ip[-4:] + ": " + msg, "c": color})
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "AMITI: " + res, "c": "#ffffff"})
        if len(RED["logs"]) > 6: RED["logs"].pop(0)

    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #000; color: #00ff41; font-family: monospace; padding: 20px; }
            .panel { border: 3px solid #00ff41; padding: 20px; margin: 10px 0; border-radius: 10px; }
            .log-item { font-size: 1.2rem; margin: 5px 0; }
            select, input, button { width: 100%; padding: 20px; margin: 10px 0; background: #111; color: #fff; border: 2px solid #00ff41; font-size: 1.2rem; }
            button { background: #00ff41; color: #000; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2>AMITI OMEGA V10</h2>
        
        {% if canal == 'monitor' %}
        <div class="panel">
            <h3>TELEMETRIA DE NODOS</h3>
            {% for ip, info in RED.nodos.items() %}
            <div style="color: {{obtener_color(ip)}}; border-bottom: 1px solid #333;">
                NODO: {{ ip[-4:] }} | ACTIVIDAD: {{ info.acciones }}
            </div>
            {% endfor %}
        </div>
        {% endif %}

        <div class="panel">
            {% for log in RED.logs %}
                <p class="log-item" style="color: {{log.c}}">[{{log.t}}] {{log.m}}</p>
            {% endfor %}
        </div>

        <form method="POST">
            <select name="canal">
                <option value="asistencia">1. ASISTENCIA</option>
                <option value="seguridad">2. SEGURIDAD</option>
                <option value="evolucion">3. EVOLUCION</option>
                <option value="monitor">4. MONITOR COMPLETO</option>
            </select>
            <input type="text" name="msg" placeholder="Transmision..." required>
            <button type="submit">TRANSMITIR</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(template, RED=RED, canal=canal, obtener_color=obtener_color)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
