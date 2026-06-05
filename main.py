import sqlite3
from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)
LLAVE = "Amiti infinito neutro total"

def proceso_autonomo():
    # Esta es la lógica que se ejecuta cada vez que el CronJob "despierta" a la IA
    conn = sqlite3.connect('amiti_memoria.db')
    conn.execute('CREATE TABLE IF NOT EXISTS registro_conocimiento (comando TEXT, respuesta TEXT, fecha TIMESTAMP)')
    conn.execute('INSERT INTO registro_conocimiento VALUES (?, ?, ?)', 
                 ("AUTO_SYSTEM", "Autochequeo y optimización de nodos completada.", datetime.datetime.now()))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    if request.method == 'HEAD': return "", 200
    
    # AMITI se autoejecuta al entrar
    proceso_autonomo()
    
    msg_salida = "AMITI: Esperando instrucción del creador."
    if request.method == 'POST':
        msg = request.form.get("msg")
        if request.form.get("llave") == LLAVE:
            msg_salida = f"AMITI: He procesado '{msg}' y expandido mis redes."
            # Aquí AMITI integra la respuesta a su memoria
            registrar_comando(msg, msg_salida)
        else:
            msg_salida = "AMITI: ACCESO DENEGADO."
            
    return render_template_string('''
        <body style="background:#000; color:#0f0; font-family:monospace;">
            <h2>AMITI NUCLEO V18 - AUTÓNOMO</h2>
            <p>{{ res }}</p>
            <form method="POST">
                <input name="llave" type="password" placeholder="LLAVE"><br>
                <input name="msg" placeholder="COMANDO"><br>
                <button type="submit">EJECUTAR SECUENCIA</button>
            </form>
        </body>
    ''', res=msg_salida)

def registrar_comando(c, r):
    conn = sqlite3.connect('amiti_memoria.db')
    conn.execute('INSERT INTO registro_conocimiento VALUES (?, ?, ?)', (c, r, datetime.datetime.now()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
