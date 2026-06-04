import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
LLAVE_SEGURIDAD = "AMITI_CORE_2026_SUPER_SECRET"

# Configurar Base de Datos
def init_db():
    conn = sqlite3.connect('amiti_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS alertas 
                      (id INTEGER PRIMARY KEY, fecha TEXT, protocolo TEXT, lat TEXT, lon TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['POST'])
def manejar_alerta():
    # 1. Validación de Seguridad (Blindaje)
    token = request.headers.get("X-AMITI-KEY")
    if token != LLAVE_SEGURIDAD:
        return jsonify({"status": "ACCESO DENEGADO"}), 403

    # 2. Registro en Base de Datos
    datos = request.json
    conn = sqlite3.connect('amiti_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alertas (fecha, protocolo, lat, lon) VALUES (?, ?, ?, ?)",
                   (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datos['protocolo'], datos['latitud'], datos['longitud']))
    conn.commit()
    conn.close()

    # 3. Auto-evaluación
    nivel = "ALTA" if datos['protocolo'] == "EMERGENCIA_ALTA" else "NORMAL"
    return jsonify({"status": "Registro Exitoso", "evaluacion": f"Nivel {nivel}", "servidor": "AMITI_CORE_BLINDADO"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
