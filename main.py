import sqlite3, os, shutil, compileall
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
LLAVE_SEGURIDAD = "AMITI_INFINITO_NEUTRO_CORE_2026"

def init_db():
    conn = sqlite3.connect('amiti_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS alertas 
                      (id INTEGER PRIMARY KEY, fecha TEXT, protocolo TEXT, lat TEXT, lon TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/auto_upgrade', methods=['POST'])
def auto_upgrade():
    if request.headers.get("X-AMITI-KEY") != LLAVE_SEGURIDAD:
        return jsonify({"status": "ACCESO DENEGADO"}), 403
    nuevo_codigo = request.json.get("codigo")
    shutil.copy("main.py", "main_backup.py")
    try:
        with open("main_temp.py", "w") as f:
            f.write(nuevo_codigo)
        if compileall.compile_file("main_temp.py", quiet=True):
            shutil.move("main_temp.py", "main.py")
            return jsonify({"status": "AMITI EVOLUCIONADA EXITOSAMENTE"})
        else:
            raise Exception("Error de sintaxis")
    except Exception as e:
        shutil.copy("main_backup.py", "main.py")
        return jsonify({"status": "ROLLBACK REALIZADO", "error": str(e)})

@app.route('/', methods=['POST'])
def manejar_alerta():
    if request.headers.get("X-AMITI-KEY") != LLAVE_SEGURIDAD:
        return jsonify({"status": "ACCESO DENEGADO"}), 403
    datos = request.json
    conn = sqlite3.connect('amiti_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alertas (fecha, protocolo, lat, lon) VALUES (?, ?, ?, ?)",
                   (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datos['protocolo'], datos['latitud'], datos['longitud']))
    cursor.execute("SELECT COUNT(*) FROM alertas")
    total = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({"status": "Registro Exitoso", "total": total, "estado": "AMITI INFINITO NEUTRO"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
