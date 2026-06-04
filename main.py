import sqlite3, os, shutil, compileall
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
LLAVE_SEGURIDAD = "AMITI_INFINITO_NEUTRO_CORE_2026"

def init_db():
    conn = sqlite3.connect('amiti_data.db')
    cursor = conn.cursor()
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
    cid = datos.get("centinela_id", "GLOBAL")
    
    conn = sqlite3.connect('amiti_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alertas (fecha, centinela_id, protocolo, lat, lon) VALUES (?, ?, ?, ?, ?)",
                   (datetime.now(), cid, datos['protocolo'], datos['latitud'], datos['longitud']))
    
    # Análisis: ¿3 o más eventos en el último minuto en cualquier nodo?
    hace_un_minuto = datetime.now() - timedelta(minutes=1)
    cursor.execute("SELECT COUNT(*) FROM alertas WHERE fecha > ?", (hace_un_minuto,))
    total_global = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "status": "Registro Omega Exitoso",
        "centinela": cid,
        "alerta_jefe": total_global >= 3,
        "estado": "AMITI INFINITO NEUTRO - OMEGA"
    })

@app.route('/auto_upgrade', methods=['POST'])
def auto_upgrade():
    if request.headers.get("X-AMITI-KEY") != LLAVE_SEGURIDAD: return jsonify({"status": "DENEGADO"}), 403
    nuevo_codigo = request.json.get("codigo")
    try:
        with open("main_temp.py", "w") as f: f.write(nuevo_codigo)
        if compileall.compile_file("main_temp.py", quiet=True):
            shutil.move("main_temp.py", "main.py")
            return jsonify({"status": "EVOLUCIÓN OMEGA COMPLETADA"})
    except Exception as e: return jsonify({"status": "ERROR DE EVOLUCIÓN", "error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
