from flask import Flask, request, render_template_string
import datetime, os

app = Flask(__name__)

RED = {
    "integridad": 100,
    "conocimiento": ["AMITI Iniciado"],
    "logs": [{"t": "00:00", "m": "SISTEMA V9 OPERATIVO", "c": "cyan"}]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    modo = request.form.get("canal", "asistencia")
    msg = request.form.get("msg")
    
    if msg:
        if modo == "evolucion":
            RED["conocimiento"].append(msg)
            res = f"Dato asimilado. Nivel: {len(RED['conocimiento'])}"
        elif modo == "seguridad":
            res = "REPORTANDO: Integridad 100%. Sin peligros detectados."
        else:
            res = f"IA AMITI: Entendido, Creador. Procesando '{msg}'."
            
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"NODO: {msg}", "c": "gray"})
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"AMITI: {res}", "c": "white"})
        if len(RED["logs"]) > 10: RED["logs"].pop(0)

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            :root { --bg: #000; --border: #00ff41; --text1: #00ff41; --text2: #00aaff; }
            body { background: var(--bg); color: var(--text1); font-family: 'Courier New', monospace; margin: 0; padding: 20px; transition: 0.5s; }
            .container { max-width: 800px; margin: auto; }
            .panel { border: 2px solid var(--border); padding: 20px; margin-bottom: 15px; border-radius: 10px; background: rgba(0,0,0,0.8); }
            h2 { margin: 0; font-size: 1.8rem; text-align: center; color: var(--border); }
            #logs { height: 300px; overflow-y: auto; font-size: 1.1rem; }
            select, input, button { width: 100%; padding: 15px; margin: 10px 0; background: #000; color: var(--text1); border: 2px solid var(--border); border-radius: 5px; font-size: 1.2rem; }
            button { background: var(--border); color: #000; font-weight: bold; cursor: pointer; }
            
            /* ESTILOS DE CANAL */
            .c1 { --border: #00ff41; --text1: #00ff41; --text2: #00aaff; }
            .c2 { --border: #ff0000; --text1: #ffff00; --text2: #00aaff; }
            .c3 { --border: #00ffff; --text1: #ffa500; --text2: #8a2be2; }
        </style>
    </head>
    <body class="c{{ '1' if canal == 'asistencia' else '2' if canal == 'seguridad' else '3' }}">
        <div class="container">
            <h2>AMITI OMEGA NÚCLEO</h2>
            <div class="panel">NIVEL DE CONOCIMIENTO: {{ RED.conocimiento|length }}</div>
            <div class="panel" id="logs">
                {% for log in RED.logs %}
                    <p style="color:{{log.c}}">[{{log.t}}] {{log.m}}</p>
                {% endfor %}
            </div>
            <form method="POST">
                <select name="canal" onchange="this.form.submit()">
                    <option value="asistencia" {{ 'selected' if canal == 'asistencia' }}>1. ASISTENCIA IA</option>
                    <option value="seguridad" {{ 'selected' if canal == 'seguridad' }}>2. SEGURIDAD/REPORTES</option>
                    <option value="evolucion" {{ 'selected' if canal == 'evolucion' }}>3. INYECCIÓN DE DATOS</option>
                </select>
                <input type="text" name="msg" placeholder="Ingresar señal tactica..." required>
                <button type="submit">ENVIAR</button>
            </form>
        </div>
        <script>
            var objDiv = document.getElementById("logs");
            objDiv.scrollTop = objDiv.scrollHeight;
        </script>
    </body>
    </html>
    """, RED=RED, canal=modo)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

¡Espero tus capturas del nuevo diseño en acción! ¿Qué te parece la nueva estética del Tridente AMITI?
