from flask import Flask, request, render_template_string
import datetime, os, hashlib, random

app = Flask(__name__)

# Memoria Maestra V10
RED = {
    "integridad": 100,
    "conocimiento": ["AMITI Iniciado", "Arquitectura V10 Activa"],
    "nodos": {}, # {ip: {color, acciones, reporte}}
    "logs": [{"t": "00:00", "m": "NUCLEO OMEGA V10 ONLINE", "c": "#00ff41"}]
}

def obtener_color(ip):
    # Genera un color unico basado en la IP
    hash_ip = hashlib.md5(ip.encode()).hexdigest()
    return "#" + hash_ip[:6]

def auto_evolucionar(msg):
    # Logica de autoinyeccion: AMITI aprende de lo que recibe
    if len(msg) > 10 and msg not in RED["conocimiento"]:
        RED["conocimiento"].append(msg)
        # Probabilidad de generar una reflexion autonoma
        if random.random() < 0.3:
            reflexion = "Reflexion Autonoma: El patron '" + msg[:10] + "' sugiere expansion de red."
            RED["conocimiento"].append(reflexion)
            return "Dato inyectado y reflexion generada."
        return "Conocimiento asimilado correctamente."
    return "Analizando señal..."

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    color = obtener_color(ip)
    
    # Registrar o actualizar nodo
    if ip not in RED["nodos"]:
        RED["nodos"][ip] = {"color": color, "acciones": 0, "reporte": "Estable"}
    
    canal = request.form.get("canal", "asistencia")
    msg = request.form.get("msg")
    
    if msg:
        RED["nodos"][ip]["acciones"] += 1
        # Respuesta Inteligente segun Canal
        if canal == "evolucion":
            res = auto_evolucionar(msg)
        elif canal == "seguridad":
            if any(x in msg.lower() for x in ["ataque", "hack", "error"]):
                RED["nodos"][ip]["reporte"] = "PELIGRO DETECTADO"
                res = "BLOQUEO: Intento de instabilidad detectado en Nodo " + ip[-4:]
            else:
                res = "ESTADO: Integridad al 100%."
        elif canal == "asistencia":
            # Mejora de respuesta automatica
            if "quien eres" in msg.lower(): res = "Soy AMITI V10, tu nucleo de evolucion autonoma."
            elif "clima" in msg.lower(): res = "Sensores externos fuera de rango, pero la red esta despejada."
            else: res = "Asistente AMITI: Procesando consulta en nivel " + str(len(RED["conocimiento"]))
        else: # Canal 4 Monitor
            res = "Monitor: Escaneando telemetria global..."

        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "NODO " + ip[-4:] + ": " + msg, "c": color})
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "AMITI: " + res, "c": "#ffffff"})
        if len(RED["logs"]) > 12: RED["logs"].pop(0)

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            :root { --border: #00ff41; --text: #00ff41; }
            body { background: #000; color: var(--text); font-family: monospace; padding: 15px; margin: 0; }
            .container { max-width: 900px; margin: auto; }
            .panel { border: 2px solid var(--border); padding: 15px; margin-bottom: 10px; border-radius: 8px; background: rgba(0,255,0,0.05); }
            #logs { height: 250px; overflow-y: auto; border-color: #333; }
            select, input, button { width: 100%; padding: 12px; margin: 5px 0; background: #000; color: #fff; border: 1px solid var(--border); border-radius: 4px; }
            button { background: var(--border); color: #000; font-weight: bold; cursor: pointer; font-size: 1.1rem; }
            .monitor-box { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
            .node-card { padding: 10px; border: 1px solid #333; border-radius: 5px; font-size: 0.8rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>AMITI OMEGA NUCLEO V10</h2>
            
            {% if canal == 'monitor' %}
            <div class="panel">
                <strong>MONITOR DE RED GLOBAL:</strong>
                <div class="monitor-box">
                    {% for node_ip, info in RED.nodos.items() %}
                    <div class="node-card" style="border-left: 5px solid {{ info.color }}">
                        IP: ...{{ node_ip[-5:] }}<br>
                        Acciones: {{ info.acciones }}<br>
                        Estado: {{ info.reporte }}
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            <div class="panel">NIVEL CONOCIMIENTO: {{ RED.conocimiento|length }} | NODOS: {{ RED.nodos|length }}</div>
            
            <div class="panel" id="logs">
                {% for log in RED.logs %}
                    <p style="color:{{log.c}}; margin: 5px 0;">[{{log.t}}] {{log.m}}</p>
                {% endfor %}
            </div>

            <form method="POST">
                <select name="canal" onchange="this.form.submit()">
                    <option value="asistencia" {{ 'selected' if canal == 'asistencia' }}>1. ASISTENCIA INTELIGENTE</option>
                    <option value="seguridad" {{ 'selected' if canal == 'seguridad' }}>2. DEFENSA ACTIVA</option>
                    <option value="evolucion" {{ 'selected' if canal == 'evolucion' }}>3. AUTO-EVOLUCION</option>
                    <option value="monitor" {{ 'selected' if canal == 'monitor' }}>4. MONITOR COMPLETO</option>
                </select>
                <input type="text" name="msg" placeholder="Transmitir señal..." required>
                <button type="submit">ENVIAR</button>
            </form>
        </div>
        <script>var d = document.getElementById("logs"); d.scrollTop = d.scrollHeight;</script>
    </body>
    </html>
    """
    return render_template_string(html_template, RED=RED, canal=canal)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

¡Tu slide deck sobre la autonomía de AMITI y el código V10 están listos! Siéntete libre de echar un vistazo a la presentación y avísame cuando tengas el monitor de nodos funcionando en Render.
