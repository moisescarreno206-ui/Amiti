from flask import Flask, request, render_template_string
import sqlite3, datetime

app = Flask(__name__)

# --- CONFIGURACIÓN DE MEMORIA ---
def init_db():
    conn = sqlite3.connect('amiti.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS memoria (pregunta TEXT, respuesta TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- LÓGICA INTERNA ---
def procesar_IA(msg):
    # Aquí simulamos la IA. Después conectaremos con tu base de datos.
    return f"IA AMITI: He registrado tu consulta '{msg}'. Estoy analizando la mejor respuesta."

def ejecutar_comando(msg):
    if "monitor" in msg: return "MONITOR: Sistema central al 98% de capacidad."
    if "seguridad" in msg: return "SEGURIDAD: Nodo casco central activo. Sin amenazas."
    return None

# --- ORQUESTADOR ---
@app.route('/', methods=['GET', 'POST'])
def handle():
    respuesta = "Esperando ordenes..."
    if request.method == 'POST':
        msg = request.form.get("msg", "").lower()
        comando = ejecutar_comando(msg)
        respuesta = comando if comando else procesar_IA(msg)
        
        # Guardar en memoria
        conn = sqlite3.connect('amiti.db')
        conn.execute('INSERT INTO memoria VALUES (?, ?)', (msg, respuesta))
        conn.commit()
        conn.close()

    return render_template_string('''
        <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
            <h3>AMITI NUCLEO MAESTRO</h3>
            <p>{{res}}</p>
            <form method="POST"><input name="msg"><button>EJECUTAR</button></form>
        </body>
    ''', res=respuesta)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
