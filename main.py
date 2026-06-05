from flask import Flask, request, render_template_string
import datetime, os, re

app = Flask(__name__)

# Memoria maestra con contador de clientes
ESTADO = {
    "integridad": 100,
    "modo": "NEUTRO",
    "clientes_en_linea": 0,
    "logs": [{"t": "00:00", "m": "NÚCLEO ONLINE - MONITOR ACTIVO", "c": "green"}]
}

def analizar_comando(comando):
    c = comando.lower()
    if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', c):
        resultado = eval(re.search(r'\d+\s*[\+\-\*\/]\s*\d+', c).group())
        return f"Cálculo completado: {resultado}."
    if "hola" in c: return "Saludos, Creador. Mis sensores están listos."
    return f"Instrucción '{comando}' procesada."

@app.route('/', methods=['GET', 'POST'])
def index():
    # Aumentar contador cada vez que alguien entra
    ESTADO["clientes_en_linea"] += 1
    
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
            .stat { color: #ff00ff; font-weight: bold; }
            #logs { height: 200px; overflow-y: auto; }
            input { background: #000; color: #00ff41; border: 1px solid #00ff41; width: 100%; padding: 10px; }
            button { background: #00ff41; color: #000; width: 100%; padding: 10px; border: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2>AMITI OMEGA NÚCLEO</h2>
        <div class="panel">
            Integridad: {{ESTADO.integridad}}% | Modo: {{ESTADO.modo}}<br>
            Clientes en línea: <span class="stat">{{ESTADO.clientes_en_linea}}</span>
        </div>
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
