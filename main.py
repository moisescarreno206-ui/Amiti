from flask import Flask, request, render_template_string
import sqlite3, datetime, os

app = Flask(__name__)

# --- INICIALIZACIÓN DE MEMORIA ---
def get_db():
    conn = sqlite3.connect('amiti.db')
    conn.execute('CREATE TABLE IF NOT EXISTS memoria (pregunta TEXT, respuesta TEXT)')
    return conn

# --- LÓGICA DE AMITI ---
def procesar_logica(msg):
    msg = msg.lower()
    if "monitor" in msg: return "MONITOR: Sistema central al 98% de capacidad. Nodos estables."
    if "seguridad" in msg: return "SEGURIDAD: Nodo casco central activo. Sin amenazas detectadas."
    if "menu" in msg: return "MENU: Soporte Central en línea. Nodos clientes activos: 0. Esperando señales."
    return f"IA AMITI: He analizado '{msg}'. Respuesta: Estoy procesando datos de forma autónoma."

# --- RUTAS ---
@app.route('/', methods=['GET', 'POST'])
def handle():
    respuesta = "Esperando órdenes..."
    if request.method == 'POST':
        msg = request.form.get("msg", "")
        if msg:
            respuesta = procesar_logica(msg)
            conn = get_db()
            conn.execute('INSERT INTO memoria VALUES (?, ?)', (msg, respuesta))
            conn.commit()
            conn.close()

    return render_template_string('''
        <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
            <h3>AMITI NUCLEO MAESTRO</h3>
            <p>{{res}}</p>
            <form method="POST">
                <input name="msg" style="width:100%; background:#111; color:#0f0; border:1px solid #0f0;" required>
                <button type="submit" style="width:100%; background:#0f0;">EJECUTAR</button>
            </form>
        </body>
    ''', res=respuesta)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
