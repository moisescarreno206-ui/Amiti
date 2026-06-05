from flask import Flask, request, render_template_string
import datetime, os, hashlib

app = Flask(__name__)

# --- MÓDULOS DE BIBLIOTECA ---
class Biblioteca:
    class Asistencia:
        @staticmethod
        def ejecutar(msg):
            return "ASISTENCIA: Procesando consulta '" + msg + "' en base de datos."

    class Contabilidad:
        @staticmethod
        def ejecutar(msg):
            # Aquí irá tu lógica de cálculo de cuentas
            return "CONTABILIDAD: Analizando balance para: " + msg

    class Monitor:
        @staticmethod
        def ejecutar(msg):
            return "MONITOR: Sistema en línea. Nodos activos: 1. Integridad: 100%."

# --- NÚCLEO (ORQUESTADOR) ---
RED = {"logs": [{"t": "00:00", "m": "NUCLEO OMEGA V10: LISTO", "c": "#00ff41"}]}

@app.route('/', methods=['GET', 'POST'])
def index():
    canal = request.form.get("canal", "asistencia")
    msg = request.form.get("msg")
    
    if msg:
        # Lógica de enrutamiento modular
        if canal == "contabilidad":
            res = Biblioteca.Contabilidad.ejecutar(msg)
        elif canal == "monitor":
            res = Biblioteca.Monitor.ejecutar(msg)
        else:
            res = Biblioteca.Asistencia.ejecutar(msg)
            
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "AMITI: " + res, "c": "#ffffff"})
        if len(RED["logs"]) > 5: RED["logs"].pop(0)

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <body style="background:#000; color:#00ff41; font-family:monospace; padding:20px;">
        <h2>AMITI NUCLEO MAESTRO</h2>
        <div style="border:1px solid #00ff41; padding:10px;">
            {% for log in RED.logs %}
                <p>{{log.m}}</p>
            {% endfor %}
        </div>
        <form method="POST">
            <select name="canal" style="width:100%; padding:10px; background:#111; color:#0f0;">
                <option value="asistencia">Asistencia IA</option>
                <option value="contabilidad">Contabilidad</option>
                <option value="monitor">Monitor Maestro</option>
            </select>
            <input type="text" name="msg" style="width:100%; padding:10px;" required>
            <button type="submit" style="width:100%; padding:10px; background:#0f0;">EJECUTAR</button>
        </form>
    </body>
    </html>
    """, RED=RED)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
