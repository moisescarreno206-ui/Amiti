from flask import Flask, request, render_template_string
import datetime, os, hashlib

app = Flask(__name__)

# MEMORIA MAESTRA OMEGA V10
RED = {
    "conocimiento": ["Inicio de Sistema V10"],
    "nodos": {}, 
    "logs": [{"t": "00:00", "m": "NUCLEO OMEGA V10: ONLINE", "c": "#00ff41"}]
}

def obtener_color(ip):
    return "#" + hashlib.md5(ip.encode()).hexdigest()[:6]

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    color = obtener_color(ip)
    
    if ip not in RED["nodos"]:
        RED["nodos"][ip] = {"acciones": 0}
    
    canal = request.form.get("canal", "asistencia")
    msg = request.form.get("msg")
    
    if msg:
        RED["nodos"][ip]["acciones"] += 1
        
        # LOGICA DE AUTO-MEJORA (AUTOINYECCION)
        if canal == "evolucion":
            RED["conocimiento"].append(msg)
            res = "Dato inyectado. Nivel de conocimiento: " + str(len(RED["conocimiento"]))
        elif canal == "monitor":
            res = "Escaneando estado de red..."
        else:
            res = "Asistente AMITI: Procesando consulta."
            
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
            <div style="color: {{obtener_color(ip)}};">
                NODO: {{ ip[-4:] }} | ACTIVIDAD: {{ info.acciones }}
            </div>
            {% endfor %}
        </div>
        {% endif %}

        <div class="panel">
            {% for log in RED.logs %}
                <p style="color: {{log.c}}">[{{log.t}}] {{log.m}}</p>
            {% endfor %}
        </div>

        <form method="POST">
            <select name="canal">
                <option value="asistencia">1. ASISTENCIA</option>
                <option value="evolucion">3. AUTO-EVOLUCION</option>
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
    
