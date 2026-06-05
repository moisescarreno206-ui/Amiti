from flask import Flask, request, render_template_string
import datetime, os, hashlib, random

app = Flask(__name__)

# MEMORIA MAESTRA
RED = {
    "integridad": 100,
    "conocimiento": ["AMITI Iniciado", "Arquitectura V10 Activa"],
    "nodos": {}, # Almacena datos de clientes {ip: {color, acciones}}
    "logs": [{"t": "00:00", "m": "NUCLEO OMEGA V10 ONLINE", "c": "#00ff41"}]
}

def obtener_color(ip):
    hash_ip = hashlib.md5(ip.encode()).hexdigest()
    return "#" + hash_ip[:6]

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.remote_addr
    color = obtener_color(ip)
    
    # Registro de nodo cliente
    if ip not in RED["nodos"]:
        RED["nodos"][ip] = {"color": color, "acciones": 0}
    
    canal = request.form.get("canal", "asistencia")
    msg = request.form.get("msg")
    
    if msg:
        RED["nodos"][ip]["acciones"] += 1
        # Lógica de Autoinyección
        if canal == "evolucion":
            RED["conocimiento"].append(msg)
            res = "Dato asimilado. Nivel de red: " + str(len(RED["conocimiento"]))
        elif canal == "seguridad":
            res = "SISTEMA SEGURO. Integridad: " + str(RED["integridad"]) + "%"
        else:
            res = "Procesando señal: " + msg
        
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "NODO " + ip[-4:] + ": " + msg, "c": color})
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "AMITI: " + res, "c": "#ffffff"})
        if len(RED["logs"]) > 8: RED["logs"].pop(0)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #000; color: #00ff41; font-family: monospace; padding: 20px; }
            .panel { border: 4px solid #00ff41; padding: 30px; margin-bottom: 20px; border-radius: 15px; }
            h2 { font-size: 2.5rem; text-align: center; }
            #logs { height: 400px; overflow-y: auto; font-size: 1.5rem; }
            .node-card { padding: 15px; margin: 10px 0; border-left: 10px solid; font-size: 1.3rem; }
            select, input, button { width: 100%; padding: 25px; margin: 15px 0; font-size: 1.6rem; background: #000; color: #fff; border: 3px solid #00ff41; }
            button { background: #00ff41; color: #000; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2>AMITI OMEGA V10</h2>
        
        {% if canal == 'monitor' %}
        <div class="panel">
            <h3>MONITOR COMPLETO DE NODOS</h3>
            {% for ip, info in RED.nodos.items() %}
            <div class="node-card" style="border-color: {{ info.color }}">
                CLIENTE: ...{{ ip[-4:] }} | ACCIONES: {{ info.acciones }}
            </div>
            {% endfor %}
        </div>
        {% endif %}

        <div class="panel" id="logs">
            {% for log in RED.logs %}
                <p style="color:{{log.c}}">[{{log.t}}] {{log.m}}</p>
            {% endfor %}
        </div>

        <form method="POST">
            <select name="canal">
                <option value="asistencia">1. ASISTENCIA</option>
                <option value="seguridad">2. SEGURIDAD</option>
                <option value="evolucion">3. AUTO-EVOLUCION</option>
                <option value="monitor">4. MONITOR COMPLETO</option>
            </select>
            <input type="text" name="msg" placeholder="Transmitir..." required>
            <button type="submit">EJECUTAR</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html, RED=RED, canal=canal)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
