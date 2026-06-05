import sqlite3
from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN ---
LLAVE_SEGURIDAD = "Amiti infinito neutro total"

# --- MOTOR DE ACTUALIZACIÓN INTEGRADO ---
# En lugar de usar threading (que causa errores 500), 
# la IA se auto-actualiza al cargar la página.
def ejecutar_actualizacion_autonoma():
    conn = sqlite3.connect('amiti_memoria.db')
    conn.execute('INSERT INTO registro_conocimiento (comando, respuesta) VALUES (?, ?)', 
                 ("SYSTEM_AUTO_UPDATE", f"Optimización realizada a las {datetime.datetime.now()}"))
    conn.commit()
    conn.close()

# --- INTERFAZ ESTÉTICA ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #050505; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; }
        .monitor { border: 1px solid #00ff41; padding: 15px; }
        .led { height: 10px; width: 10px; background: #00ff41; border-radius: 50%; display: inline-block; }
        input, button { background: #000; color: #00ff41; border: 1px solid #00ff41; padding: 10px; width: 100%; margin-top: 5px; }
    </style>
</head>
<body>
    <h2>AMITI NUCLEO V16 <div class="led"></div></h2>
    <div class="monitor">
        <p>> ESTADO: Sistema estabilizado.</p>
        <p>> Último registro: {{ res }}</p>
        <p>> Registros totales: {{ count }}</p>
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
    # Cada vez que alguien entra, la IA trabaja
    ejecutar_actualizacion_autonoma()
    
    respuesta = "Sistema activo."
    if request.method == 'POST':
        msg = request.form.get("msg", "")
        llave = request.form.get("llave", "")
        
        if llave == LLAVE_SEGURIDAD:
            respuesta = f"Comando '{msg}' autorizado."
            conn = sqlite3.connect('amiti_memoria.db')
            conn.execute('INSERT INTO registro_conocimiento (comando, respuesta) VALUES (?, ?)', (msg, respuesta))
            conn.commit()
            conn.close()
        else:
            respuesta = "ACCESO DENEGADO."

    conn = sqlite3.connect('amiti_memoria.db')
    count = conn.execute('SELECT count(*) FROM registro_conocimiento').fetchone()[0]
    conn.close()
    return render_template_string(HTML_TEMPLATE, res=respuesta, count=count)

if __name__ == "__main__":
    conn = sqlite3.connect('amiti_memoria.db')
    conn.execute('CREATE TABLE IF NOT EXISTS registro_conocimiento (comando TEXT, respuesta TEXT)')
    conn.close()
    app.run(host='0.0.0.0', port=10000)
    
