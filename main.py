import threading, time, sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- CONFIGURACIÓN ---
LLAVE_SEGURIDAD = "Amiti infinito neutro total"

# --- MOTOR AUTÓNOMO (Segundo plano corregido) ---
def motor_autonomo():
    while True:
        try:
            # check_same_thread=False permite que este hilo escriba aunque Flask esté activo
            conn = sqlite3.connect('amiti_memoria.db', check_same_thread=False)
            conn.execute('INSERT INTO registro_conocimiento (comando, respuesta) VALUES (?, ?)', 
                         ("SYSTEM_AUTO_UPDATE", "Optimización de nodos completada."))
            conn.commit()
            conn.close()
        except:
            pass
        time.sleep(15) 

hilo = threading.Thread(target=motor_autonomo, daemon=True)
hilo.start()

# --- INTERFAZ Y LÓGICA ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #050505; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; }
        .monitor { border: 1px solid #00ff41; padding: 15px; }
        .led { height: 10px; width: 10px; background: #00ff41; border-radius: 50%; display: inline-block; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } }
        input, button { background: #000; color: #00ff41; border: 1px solid #00ff41; padding: 10px; width: 100%; margin-top: 5px; }
    </style>
</head>
<body>
    <h2>AMITI NUCLEO V15 <div class="led"></div></h2>
    <div class="monitor">
        <p>> ESTADO: Sistema estabilizado.</p>
        <p>> Última acción: {{ res }}</p>
        <p>> Registros en memoria: {{ count }}</p>
    </div>
    <form method="POST">
        <input name="llave" type="password" placeholder="LLAVE DE ACCESO" required>
        <input name="msg" placeholder="COMANDO..." required>
        <button type="submit">EJECUTAR</button>
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def orquestador():
    respuesta = "Sistema esperando..."
    if request.method == 'POST':
        msg = request.form.get("msg", "")
        llave = request.form.get("llave", "")
        
        if llave == LLAVE_SEGURIDAD:
            respuesta = f"Comando '{msg}' ejecutado."
            conn = sqlite3.connect('amiti_memoria.db', check_same_thread=False)
            conn.execute('INSERT INTO registro_conocimiento (comando, respuesta) VALUES (?, ?)', (msg, respuesta))
            conn.commit()
            conn.close()
        else:
            respuesta = "ACCESO DENEGADO."

    conn = sqlite3.connect('amiti_memoria.db', check_same_thread=False)
    count = conn.execute('SELECT count(*) FROM registro_conocimiento').fetchone()[0]
    conn.close()
    return render_template_string(HTML_TEMPLATE, res=respuesta, count=count)

if __name__ == "__main__":
    conn = sqlite3.connect('amiti_memoria.db', check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS registro_conocimiento (comando TEXT, respuesta TEXT)')
    conn.close()
    app.run(host='0.0.0.0', port=10000)
    
