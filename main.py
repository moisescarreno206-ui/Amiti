from flask import Flask, request, render_template_string
import sqlite3, datetime

app = Flask(__name__)

# --- LÓGICA DE BASE DE DATOS (Memoria) ---
def registrar_interaccion(pregunta, respuesta):
    conn = sqlite3.connect('amiti.db')
    conn.execute('CREATE TABLE IF NOT EXISTS conocimiento (q TEXT, a TEXT)')
    conn.execute('INSERT INTO conocimiento VALUES (?, ?)', (pregunta, respuesta))
    conn.commit()
    conn.close()

# --- LÓGICA DE COMANDOS (Sistema) ---
def manejar_comando(msg):
    msg = msg.lower()
    if "monitor" in msg: return "ESTADO: Núcleo Online. Memoria: Activa. Integridad: 100%."
    if "seguridad" in msg: return "SEGURIDAD: Nodo Casco Central protegido. No hay intrusiones."
    if "ayuda" in msg: return "COMANDOS: monitor, seguridad, ayuda, o hazme una consulta."
    return None

# --- ORQUESTADOR (El Puente) ---
@app.route('/', methods=['GET', 'POST'])
def puente():
    resultado = "Casco Central en línea. Esperando órdenes..."
    
    if request.method == 'POST':
        msg = request.form.get("msg", "")
        if msg:
            # 1. Intentar ejecutar comando
            comando = manejar_comando(msg)
            # 2. Si no es comando, procesar como IA
            resultado = comando if comando else f"IA: He recibido '{msg}'. Estoy aprendiendo de esto."
            
            # 3. Registrar en memoria
            registrar_interaccion(msg, resultado)
            
    return render_template_string('''
        <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
            <h3>AMITI NUCLEO MAESTRO</h3>
            <p>{{res}}</p>
            <form method="POST">
                <input name="msg" style="width:100%; background:#111; color:#0f0; border:1px solid #0f0;" required autofocus>
                <button type="submit" style="width:100%; background:#0f0;">ENVIAR</button>
            </form>
        </body>
    ''', res=resultado)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
