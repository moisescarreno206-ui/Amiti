import sqlite3, os, shutil, compileall
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
LLAVE_SEGURIDAD = "AMITI_INFINITO_NEUTRO_CORE_2026"

def init_db():
    conn = sqlite3.connect('amiti_data.db')
    cursor = conn.cursor()
    # Ahora guardamos el ID del centinela que reporta
    cursor.execute('''CREATE TABLE IF NOT EXISTS alertas 
                      (id INTEGER PRIMARY KEY, fecha TIMESTAMP, centinela_id TEXT, protocolo TEXT, lat TEXT, lon TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['POST'])
def manejar_alerta():
    if request.headers.get("X-AMITI-KEY") != LLAVE_SEGURIDAD:
        return jsonify({"status": "ACCESO DENEGADO"}), 403

    datos = request.json
    centinela_id = datos.get("centinela_id", "DESCONOCIDO")
    
    conn = sqlite3.connect('amiti_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alertas (fecha, centinela_id, protocolo, lat, lon) VALUES (?, ?, ?, ?, ?)",
                   (datetime.now(), centinela_id, datos['protocolo'], datos['latitud'], datos['longitud']))
    
    # Análisis Global: ¿Hay alertas críticas de cualquier centinela en el último minuto?
    hace_un_minuto = datetime.now() - timedelta(minutes=1)
    cursor.execute("SELECT COUNT(*) FROM alertas WHERE fecha > ?", (hace_un_minuto,))
    total_global = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "status": "Registro Global Exitoso",
        "centinela": centinela_id,
        "alerta_jefe": total_global >= 3
    })

# ... (mantén tu función auto_upgrade igual)
