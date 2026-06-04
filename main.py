import sqlite3, os, shutil, compileall
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
LLAVE_SEGURIDAD = "AMITI_INFINITO_NEUTRO_CORE_2026"

def init_db():
    conn = sqlite3.connect('amiti_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS alertas 
                      (id INTEGER PRIMARY KEY, fecha TIMESTAMP, protocolo TEXT, lat TEXT, lon TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['POST'])
def manejar_alerta():
    if request.headers.get("X-AMITI-KEY") != LLAVE_SEGURIDAD:
        return jsonify({"status": "ACCESO DENEGADO"}), 403

    datos = request.json
    conn = sqlite3.connect('amiti_data.db')
    cursor = conn.cursor()
    
    # Insertar con timestamp real
    cursor.execute("INSERT INTO alertas (fecha, protocolo, lat, lon) VALUES (?, ?, ?, ?)",
                   (datetime.now(), datos['protocolo'], datos['latitud'], datos['longitud']))
    
    # ANALISTA: Buscar si hay 3 alertas en el último minuto
    hace_un_minuto = datetime.now() - timedelta(minutes=1)
    cursor.execute("SELECT COUNT(*) FROM alertas WHERE fecha > ?", (hace_un_minuto,))
    conteo_reciente = cursor.fetchone()[0]
    
    estado = "AMITI INFINITO NEUTRO - Estable"
    if conteo_reciente >= 3:
        estado = "AMITI INFINITO NEUTRO - ALERTA ROJA: PATRÓN ACELERADO"
        
    cursor.execute("SELECT COUNT(*) FROM alertas")
    total = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    return jsonify({"status": "Registro Exitoso", "total": total, "estado": estado})

# ... (mantén tu función auto_upgrade igual que antes)
