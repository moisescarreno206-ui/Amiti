from flask import Flask, request, render_template_string
import datetime, os

app = Flask(__name__)

# Memoria maestra del Núcleo
RED = {
    "integridad": 100,
    "modo": "ACTIVO",
    "conocimiento": ["AMITI es el centro de mando"],
    "logs": [{"t": "00:00", "m": "TRIPLE CANAL INICIADO", "c": "cyan"}]
}

def procesar_canal(tipo, dato):
    dato = dato.lower()
    # Canal 1: Asistencia (IA)
    if tipo == "asistencia":
        if "hola" in dato: return "Hola Creador, aquí AMITI. Estoy operativa."
        return f"Procesando consulta táctica: '{dato}'."
    
    # Canal 2: Seguridad/Reportes
    if tipo == "seguridad":
        if "peligro" in dato or "reporte" in dato:
            return "ESCANEO: Integridad al 100%. Sin amenazas detectadas en la red."
        return "Canal de seguridad abierto. Reportando..."
    
    # Canal 3: Inyección de Conocimiento (Evolución)
    if tipo == "evolucion":
        if dato not in RED["conocimiento"]:
            RED["conocimiento"].append(dato)
            return f"Dato '{dato}' asimilado. Nivel de red subió a {len(RED['conocimiento'])}."
        return "Dato ya existe en la red."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        canal = request.form.get("canal")
        msg = request.form.get("msg")
        if msg:
            RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"NODO: {msg}", "c": "green"})
            respuesta = procesar_canal(canal, msg)
            RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"AMITI: {respuesta}", "c": "cyan"})
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><style>
        body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 10px; }
        .panel { border: 1px solid #00ff41; padding: 10px; margin-bottom: 10px; }
        input, select, button { width: 100%; background: #000; color: #00ff41; border: 1px solid #00ff41; padding: 8px; margin: 5px 0; }
        button { background: #00ff41; color: #000; font-weight: bold; }
    </style></head>
    <body>
        <h2>AMITI OMEGA NÚCLEO</h2>
        <div class="panel">Nivel de Conocimiento: {{RED.conocimiento|length}}</div>
        <div class="panel" id="logs" style="height:150px; overflow-y:auto;">
            {% for log in RED.logs %}<p style="color:{{log.c}}">[{{log.t}}] {{log.m}}</p>{% endfor %}
        </div>
        <form method="POST">
            <select name="canal">
                <option value="asistencia">1. ASISTENCIA IA</option>
                <option value="seguridad">2. SEGURIDAD/REPORTES</option>
                <option value="evolucion">3. INYECCIÓN DE DATOS</option>
            </select>
            <input type="text" name="msg" placeholder="Ingresar señal..." required>
            <button type="submit">TRANSMITIR SEÑAL</button>
        </form>
    </body>
    </html>
    """, RED=RED)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
