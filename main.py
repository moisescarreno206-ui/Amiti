from flask import Flask, request, jsonify, render_template_string
import sqlite3, os

app = Flask(__name__)

# --- INTERFAZ HTML ---
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head><title>AMITI OMEGA</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{background:#000;color:#0f0;font-family:monospace;padding:15px;} #chat{height:300px;border:1px solid #0f0;overflow-y:scroll;padding:10px;margin-bottom:10px;} input{width:65%;padding:10px;background:#111;color:#0f0;border:1px solid #0f0;} button{padding:10px;background:#0f0;color:#000;border:none;font-weight:bold;}</style></head>
<body><h3>AMITI OMEGA VIGILANTE</h3><div id="chat"></div><input type="text" id="msg" placeholder="Comando..."><button onclick="enviar()">Enviar</button>
<script>
async function enviar(){
    let msg = document.getElementById('msg').value;
    document.getElementById('chat').innerHTML += '<p>> ' + msg + '</p>';
    let res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({comando: msg})});
    let data = await res.json();
    document.getElementById('chat').innerHTML += '<p style="color:#fff;">AMITI: ' + data.respuesta + '</p>';
    document.getElementById('msg').value = '';
}
</script></body></html>
"""

# --- INICIALIZACIÓN DE MEMORIA ---
def init_db():
    conn = sqlite3.connect('amiti_core.db')
    conn.execute('CREATE TABLE IF NOT EXISTS eventos (id INTEGER PRIMARY KEY, tipo TEXT, detalle TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- RUTAS PRINCIPALES ---
@app.route('/')
def index(): return render_template_string(HTML_INTERFACE)

@app.route('/chat', methods=['POST'])
def chat():
    comando = request.json.get("comando", "").lower()
    conn = sqlite3.connect('amiti_core.db')
    cursor = conn.cursor()
    respuesta = ""

    if "estado" in comando:
        respuesta = "SISTEMA OMEGA: Operativo. Integridad total."
    elif "diagnóstico" in comando:
        count = cursor.execute("SELECT COUNT(*) FROM eventos").fetchone()[0]
        respuesta = f"DIAGNÓSTICO: Registros de memoria: {count}. Sistema evolucionando."
    elif "aprende:" in comando:
        dato = comando.split("aprende:")[1].strip()
        cursor.execute("INSERT INTO eventos (tipo, detalle) VALUES (?, ?)", ('CONOCIMIENTO', dato))
        respuesta = f"MEMORIA ACTUALIZADA: He aprendido: {dato}"
    elif "crea un algoritmo:" in comando:
        algo = comando.split("crea un algoritmo:")[1].strip()
        cursor.execute("INSERT INTO eventos (tipo, detalle) VALUES (?, ?)", ('ALGORITMO', algo))
        respuesta = f"ALGORITMO GENERADO: '{algo}' integrado al núcleo."
    elif "ejecutar:" in comando:
        nombre = comando.split("ejecutar:")[1].strip()
        res = cursor.execute("SELECT detalle FROM eventos WHERE tipo='ALGORITMO' AND detalle LIKE ?", ('%'+nombre+'%',)).fetchone()
        respuesta = f"EJECUCIÓN: Procesando '{nombre}'... Resultado: {res[0] if res else 'No encontrado.'}"
    else:
        respuesta = "Comando procesado en el núcleo OMEGA."

    conn.commit()
    conn.close()
    return jsonify({"respuesta": respuesta})

@app.route('/favicon.ico')
def favicon(): return "", 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
