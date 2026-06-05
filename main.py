from flask import Flask, request, render_template_string
import datetime
import os

app = Flask(__name__)

# Memoria maestra expandida
ESTADO = {
    "integridad": 100,
    "modo": "NEUTRO",
    "logs": [{"t": "00:00", "m": "SISTEMA INICIALIZADO", "c": "green"}],
    "nodos": ["NODO_ALPHA", "NODO_BETA"] # Simulación de vigilancia
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comando = request.form.get("comando")
        if comando:
            ESTADO["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"Yo: {comando}", "c": "green"})
            ESTADO["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "AMITI: Procesando vigilancia...", "c": "blue"})
            if len(ESTADO["logs"]) > 15: ESTADO["logs"].pop(0)
            
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #050505; color: #00ff41; font-family: 'Courier New', monospace; margin: 0; padding: 10px; }
            .container { display: flex; flex-direction: column; height: 95vh; }
            .panel { border: 1px solid #00ff41; padding: 10px; margin-bottom: 10px; flex-grow: 1; overflow-y: auto; }
            h2 { margin: 0; font-size: 1.2rem; border-bottom: 1px solid #00ff41; }
            input { background: #000; color: #00ff41; border: 1px solid #00ff41; width: 100%; padding: 10px; box-sizing: border-box; }
            button { background: #00ff41; color: #000; width: 100%; padding: 10px; border: none; font-weight: bold; margin-top: 5px; }
            .node { color: #ff00ff; font-size: 0.8rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>AMITI OMEGA NÚCLEO</h2>
            <div class="panel">
                <strong>VIGILANCIA DE NODOS:</strong>
                {% for nodo in ESTADO.nodos %}
                    <div class="node">> {{nodo}} [ACTIVO]</div>
                {% endfor %}
            </div>
            <div class="panel" id="logs">
                {% for log in ESTADO.logs %}
                    <p style="color:{{log.c}}">[{{log.t}}] {{log.m}}</p>
                {% endfor %}
            </div>
            <form method="POST">
                <input type="text" name="comando" placeholder="Ingresar comando táctico..." required>
                <button type="submit">EJECUTAR</button>
            </form>
        </div>
    </body>
    </html>
    """, ESTADO=ESTADO)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
