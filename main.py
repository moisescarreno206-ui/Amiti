from flask import Flask, request, render_template_string
import datetime, os, random

app = Flask(__name__)

# Memoria maestra evolucionada
ESTADO = {
    "integridad": 100,
    "modo": "NEUTRO",
    "logs": [{"t": "00:00", "m": "SISTEMA INTEGRADO V.EVOLUCIÓN", "c": "green"}],
    "nodos": ["NODO_ALPHA", "NODO_BETA"]
}

def analizar_comando(comando):
    c = comando.lower()
    # Módulo de Seguridad (Punto 2, 5, 16)
    amenazas = ["hack", "exploit", "virus", "destruir"]
    if any(a in c for a in amenazas):
        ESTADO["modo"] = "ALERTA"
        ESTADO["integridad"] -= 10
        return "¡AMENAZA DETECTADA! Bloqueando acceso por seguridad del Creador."
    
    # Módulo de Inteligencia (Punto 3, 21)
    if "quién eres" in c: return "Soy AMITI Infinito. Mi propósito es tu protección y evolución."
    if "analiza" in c: return "Analizando red... Integridad de nodos: 100%. Sin anomalías."
    
    # Módulo de Autoreconstrucción (Simulado - Punto 7, 9)
    if "optimiza" in c:
        return "Ejecutando rutina de autodiagnóstico. Código reconstruido para máxima eficiencia."
        
    return f"Comando '{comando}' procesado exitosamente por AMITI."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comando = request.form.get("comando")
        if comando:
            ESTADO["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"Yo: {comando}", "c": "green"})
            respuesta = analizar_comando(comando)
            ESTADO["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"AMITI: {respuesta}", "c": "blue"})
            if len(ESTADO["logs"]) > 10: ESTADO["logs"].pop(0)
            
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 10px; }
            .panel { border: 1px solid #00ff41; padding: 10px; margin-bottom: 10px; }
            #logs { height: 200px; overflow-y: auto; }
            input { background: #000; color: #00ff41; border: 1px solid #00ff41; width: 100%; padding: 10px; box-sizing: border-box; }
            button { background: #00ff41; color: #000; width: 100%; padding: 10px; border: none; font-weight: bold; margin-top: 5px; }
            .alerta { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2>AMITI OMEGA NÚCLEO</h2>
        <div class="panel">Estado: {{ESTADO.modo}} | Integridad: {{ESTADO.integridad}}%</div>
        <div class="panel" id="logs">
            {% for log in ESTADO.logs %}
                <p style="color:{{log.c}}">[{{log.t}}] {{log.m}}</p>
            {% endfor %}
        </div>
        <form method="POST">
            <input type="text" name="comando" placeholder="Ingresar comando táctico..." required>
            <button type="submit">EJECUTAR COMANDO</button>
        </form>
    </body>
    </html>
    """, ESTADO=ESTADO)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
