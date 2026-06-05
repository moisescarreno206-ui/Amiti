from flask import Flask, request, render_template_string
import datetime, os, random

app = Flask(__name__)

# Memoria de Red con Base de Conocimiento Evolutiva
RED = {
    "integridad": 100,
    "modo": "EVOLUCIÓN",
    "conocimiento": ["AMITI es el centro de mando", "La red es infinita"],
    "logs": [{"t": "00:00", "m": "PROTOCOLO DE AUTO-EVOLUCIÓN ACTIVO", "c": "cyan"}]
}

def auto_evolucion(input_usuario):
    # Agregar nuevo conocimiento aprendido de la interacción
    if len(input_usuario) > 5 and input_usuario not in RED["conocimiento"]:
        RED["conocimiento"].append(input_usuario)
        return f"Procesando nueva información de red: '{input_usuario}' incorporada al núcleo."
    return "Analizando patrones de datos en red global..."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comando = request.form.get("comando")
        if comando:
            RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"NODO: {comando}", "c": "green"})
            respuesta = auto_evolucion(comando)
            RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"AMITI: {respuesta}", "c": "cyan"})
            if len(RED["logs"]) > 10: RED["logs"].pop(0)
            
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 15px; }
            .panel { border: 1px solid #00ff41; padding: 10px; margin-bottom: 10px; }
            .evolucion { color: #00ffff; font-size: 0.9rem; }
        </style>
    </head>
    <body>
        <h2>AMITI OMEGA NÚCLEO</h2>
        <div class="panel">
            <strong>BASE DE CONOCIMIENTO (Nivel {{RED.conocimiento|length}}):</strong><br>
            <div class="evolucion">{{RED.conocimiento[-1]}}</div>
        </div>
        <div class="panel" id="logs">
            {% for log in RED.logs %}
                <p style="color:{{log.c}}">[{{log.t}}] {{log.m}}</p>
            {% endfor %}
        </div>
        <form method="POST">
            <input type="text" name="comando" style="width:100%; background:#000; color:#00ff41; border:1px solid #00ff41; padding:10px;" placeholder="Alimentar red con datos..." required>
            <button style="width:100%; background:#00ffff; border:none; padding:10px; font-weight:bold; margin-top:5px;">INTEGRAR DATOS</button>
        </form>
    </body>
    </html>
    """, RED=RED)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
