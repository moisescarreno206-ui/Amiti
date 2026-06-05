from flask import Flask, request, render_template_string
import datetime, os, re

app = Flask(__name__)

ESTADO = {
    "integridad": 100,
    "modo": "NEUTRO",
    "logs": [{"t": "00:00", "m": "NÚCLEO ANALÍTICO ACTIVADO", "c": "green"}]
}

def analizar_comando(comando):
    c = comando.lower()
    
    # 1. Seguridad
    if any(a in c for a in ["hack", "virus"]):
        return "ALERTA: Amenaza detectada. Bloqueo de seguridad activado."
    
    # 2. IA Analítica (Resolver operaciones básicas y preguntas)
    if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', c):
        try:
            resultado = eval(re.search(r'\d+\s*[\+\-\*\/]\s*\d+', c).group())
            return f"Cálculo completado: El resultado es {resultado}."
        except:
            return "Error en la unidad de cálculo."
            
    if "hola" in c or "saludos" in c:
        return "Hola, Creador. Mis sensores están listos. ¿En qué te ayudo hoy?"
    
    if "qué eres" in c or "quién eres" in c:
        return "Soy AMITI Infinito, tu sistema de mando, protección y evolución constante."

    return f"He recibido tu instrucción: '{comando}'. Analizando prioridad..."

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
            #logs { height: 250px; overflow-y: auto; }
            input { background: #000; color: #00ff41; border: 1px solid #00ff41; width: 100%; padding: 10px; }
            button { background: #00ff41; color: #000; width: 100%; padding: 10px; border: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2>AMITI OMEGA NÚCLEO</h2>
        <div class="panel">Integridad: {{ESTADO.integridad}}% | Modo: {{ESTADO.modo}}</div>
        <div class="panel" id="logs">
            {% for log in ESTADO.logs %}
                <p style="color:{{log.c}}">[{{log.t}}] {{log.m}}</p>
            {% endfor %}
        </div>
        <form method="POST">
            <input type="text" name="comando" placeholder="Comando..." required>
            <button type="submit">EJECUTAR</button>
        </form>
    </body>
    </html>
    """, ESTADO=ESTADO)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
