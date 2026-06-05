import sqlite3
from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)
LLAVE = "Amiti infinito neutro total"

# --- LÓGICA DE MEMORIA ESTABLE ---
def registrar_actividad(comando, respuesta):
    try:
        conn = sqlite3.connect('amiti_memoria.db')
        conn.execute('CREATE TABLE IF NOT EXISTS registro_conocimiento (comando TEXT, respuesta TEXT, fecha TIMESTAMP)')
        conn.execute('INSERT INTO registro_conocimiento VALUES (?, ?, ?)', (comando, respuesta, datetime.datetime.now()))
        conn.commit()
        conn.close()
    except:
        pass

# --- ORQUESTADOR ---
@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    if request.method == 'HEAD': return "", 200
    
    # Auto-actualización al recibir "toque" del CronJob o visita
    registrar_actividad("AUTO_SYSTEM", "Optimización de nodos completada.")
    
    msg_salida = "AMITI: Estado operativo. Esperando comando."
    if request.method == 'POST':
        if request.form.get("llave") == LLAVE:
            comando = request.form.get("msg")
            msg_salida = f"AMITI: He ejecutado '{comando}' exitosamente."
            registrar_actividad(comando, msg_salida)
        else:
            msg_salida = "AMITI: ACCESO DENEGADO."

    # Obtener conteo para el contador
    try:
        conn = sqlite3.connect('amiti_memoria.db')
        count = conn.execute('SELECT count(*) FROM registro_conocimiento').fetchone()[0]
        conn.close()
    except:
        count = 0

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; }
                .monitor { border: 1px solid #00ff41; padding: 15px; box-shadow: 0 0 10px rgba(0, 255, 65, 0.2); }
                input, button { background: #000; color: #00ff41; border: 1px solid #00ff41; padding: 10px; width: 100%; margin-top: 10px; }
                h2 { border-bottom: 1px solid #00ff41; padding-bottom: 10px; }
            </style>
        </head>
        <body>
            <h2>AMITI NUCLEO V19</h2>
            <div class="monitor">
                <p>> Estatus: Online</p>
                <p>> Último registro: {{ res }}</p>
                <p>> Registros en memoria: {{ count }}</p>
            </div>
            <form method="POST">
                <input name="llave" type="password" placeholder="LLAVE DE SEGURIDAD" required>
                <input name="msg" placeholder="COMANDO..." required>
                <button type="submit">EJECUTAR</button>
            </form>
        </body>
        </html>
    ''', res=msg_salida, count=count)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
