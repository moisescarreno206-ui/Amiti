import sqlite3, os
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
# Identidad de seguridad
LLAVE_MAESTRA = "AMITI_INFINITO_NEUTRO_OMEGA_2026"
NODOS_AUTORIZADOS = ["NODO_MOVIL_01", "PC_CENTRAL", "NODO_RF_01"]

def init_db():
    conn = sqlite3.connect('amiti_core.db')
    cursor = conn.cursor()
    # Registra eventos legítimos e intrusiones (Honeypot)
    cursor.execute('''CREATE TABLE IF NOT EXISTS log_defensa 
                      (id INTEGER PRIMARY KEY, tipo TEXT, timestamp TIMESTAMP, origen TEXT, detalle TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/comms', methods=['POST'])
def comunicacion_hibrida():
    datos = request.json
    origen = datos.get("centinela_id")
    modo = datos.get("modo", "IP") # Puede ser "IP" o "RADIO"
    
    # Validación de Acceso
    if request.headers.get("X-AMITI-KEY") != LLAVE_MAESTRA or origen not in NODOS_AUTORIZADOS:
        registrar_evento("INTENTO_INTRUSION", request.remote_addr, "Acceso no autorizado via " + modo)
        return jsonify({"status": "ACCESO DENEGADO"}), 403

    # Detección de Agresión (Lógica de Patrón Acelerado)
    if datos.get("alerta_agresion"):
        registrar_evento("ALERTA_ROJA", origen, "Patrón de agresión detectado")
    
    return jsonify({"status": "SISTEMA OMEGA OPERATIVO", "modo": modo})

def registrar_evento(tipo, origen, detalle):
    conn = sqlite3.connect('amiti_core.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO log_defensa (tipo, timestamp, origen, detalle) VALUES (?, ?, ?, ?)",
                   (tipo, datetime.now(), origen, detalle))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
