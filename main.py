import sqlite3
from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN ---
LLAVE_SEGURIDAD = "Amiti infinito neutro total"

# --- LÓGICA DE MEMORIA ---
def registrar(comando, respuesta):
    try:
        conn = sqlite3.connect('amiti_memoria.db')
        conn.execute('CREATE TABLE IF NOT EXISTS registro_conocimiento (comando TEXT, respuesta TEXT)')
        conn.execute('INSERT INTO registro_conocimiento (comando, respuesta) VALUES (?, ?)', (comando, respuesta))
        conn.commit()
        conn.close()
    except:
        pass

# --- ORQUESTADOR (MANEJADOR DE MÉTODOS) ---
@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    # Manejo de HEAD (Verificación de Render)
    if request.method == 'HEAD':
        return "", 200

    respuesta = "Sistema activo."
    count = 0
    
    # Manejo de POST (Interacción)
    if request.method == 'POST':
        msg = request.form.get("msg", "")
        llave = request.form.get("llave", "")
        if llave == LLAVE_SEGURIDAD:
            respuesta = f"Comando '{msg}' autorizado."
            registrar(msg, respuesta)
        else:
            respuesta = "ACCESO DENEGADO."

    # Lectura de estado
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
                body { background: #000; color: #0f0; font-family: monospace; padding: 20px; }
                .monitor { border: 1px solid #0f0; padding: 10px; }
                input, button { background: #000; color: #0f0; border: 1px solid #0f0; padding: 10px; width: 100%; margin-top: 5px; }
            </style>
        </head>
        <body>
            <h2>AMITI NUCLEO V17</h2>
            <div class="monitor">
                <p>> Estatus: Online.</p>
                <p>> Respuesta: {{ res }}</p>
                <p>> Registros: {{ count }}</p>
            </div>
            <form method="POST">
                <input name="llave" type="password" placeholder="LLAVE DE SEGURIDAD" required>
                <input name="msg" placeholder="COMANDO..." required>
                <button type="submit">EJECUTAR</button>
            </form>
        </body>
        </html>
    ''', res=respuesta, count=count)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
