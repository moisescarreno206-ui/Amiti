from flask import Flask, request, render_template_string
import datetime
import os

# Ahora 'Flask' (con mayúscula) está definido correctamente por la importación
app = Flask(__name__)

# Memoria de estado
ESTADO_SISTEMA = {
    "integridad": 100,
    "modo": "NEUTRO",
    "logs": [{"t": "00:00", "m": "AMITI ONLINE - SISTEMA LISTO", "c": "green"}]
}

def obtener_respuesta_ia(comando):
    c = comando.lower()
    if "hola" in c: return "Saludos, Creador. Operativa al 100%."
    if "cómo estás" in c: return "Operativa y protegiendo tus archivos, Creador."
    if "evolución" in c: return "Evolución iniciada. Optimizando protocolos."
    return f"Consulta '{comando}' registrada en la red global."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comando = request.form.get("comando")
        if comando:
            respuesta = obtener_respuesta_ia(comando)
            ESTADO_SISTEMA["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"Yo: {comando}", "c": "green"})
            ESTADO_SISTEMA["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"AMITI: {respuesta}", "c": "blue"})
            if len(ESTADO_SISTEMA["logs"]) > 10: ESTADO_SISTEMA["logs"].pop(0)
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><style>
        body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 15px; }
        .box { border: 1px solid #00ff41; padding: 10px; margin-bottom: 10px; }
        input { background: #000; color: #00ff41; border: 1px solid #00ff41; width: 70%; padding: 5px; }
        button { background: #00ff41; color: #000; border: none; padding: 5px; }
        .blue { color: #00aaff; } .green { color: #00ff41; }
    </style></head>
    <body>
        <h2>AMITI NÚCLEO: CENTRO DE MANDO</h2>
        <div class="box">Estado: {{ESTADO.modo}} | Integridad: {{ESTADO.integridad}}%</div>
        <div class="box" style="height: 250px; overflow-y: scroll;">
            {% for log in ESTADO.logs %}
                <p class="{{log.c}}">[{{log.t}}] {{log.m}}</p>
            {% endfor %}
        </div>
        <form method="POST">
            <input type="text" name="comando" placeholder="Comando..." required>
            <button type="submit">Enviar</button>
        </form>
    </body>
    </html>
    """, ESTADO=ESTADO_SISTEMA)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
