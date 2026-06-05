from flask import Flask, request, render_template_string
import datetime, os, uuid

app = Flask(__name__)

# Memoria de red expandida
RED = {
    "integridad": 100,
    "modo": "MONITOREO",
    "clientes": {}, # Diccionario para rastrear comportamiento: {id: {hora, ip}}
    "logs": [{"t": "00:00", "m": "TELEMETRÍA DE RED INICIADA", "c": "green"}]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    # Identificar cliente
    client_id = request.headers.get('X-Forwarded-For', request.remote_addr)
    RED["clientes"][client_id] = datetime.datetime.now().strftime("%H:%M:%S")
    
    if request.method == 'POST':
        comando = request.form.get("comando")
        if comando:
            RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"NODO {client_id[-4:]}: {comando}", "c": "green"})
            if len(RED["logs"]) > 8: RED["logs"].pop(0)
            
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 10px; }
            .panel { border: 1px solid #00ff41; padding: 10px; margin-bottom: 10px; }
            .nodo-activo { color: #00aaff; font-size: 0.8rem; }
        </style>
    </head>
    <body>
        <h2>AMITI OMEGA NÚCLEO</h2>
        <div class="panel">
            <strong>TELEMETRÍA DE COMPORTAMIENTO:</strong><br>
            {% for id, hora in RED.clientes.items() %}
                <div class="nodo-activo">> NODO {{id[-4:]}} - ÚLTIMA ACCIÓN: {{hora}}</div>
            {% endfor %}
        </div>
        <div class="panel" id="logs">
            {% for log in RED.logs %}
                <p style="color:{{log.c}}">[{{log.t}}] {{log.m}}</p>
            {% endfor %}
        </div>
        <form method="POST">
            <input type="text" name="comando" style="width:100%; background:#000; color:#00ff41; border:1px solid #00ff41; padding:10px;" name="comando" placeholder="Emitir señal a red...">
            <button style="width:100%; background:#00ff41; border:none; padding:10px; font-weight:bold; margin-top:5px;">TRANSMITIR</button>
        </form>
    </body>
    </html>
    """, RED=RED)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
