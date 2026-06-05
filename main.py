from flask import Flask, request, jsonify, render_template_string
import sqlite3, os, random

app = Flask(__name__)

# --- INTERFAZ CON MENÚ DINÁMICO ---
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head><title>AMITI OMEGA</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#000;color:#0f0;font-family:monospace;padding:15px;}
#chat{height:250px;border:1px solid #0f0;overflow-y:scroll;padding:10px;margin-bottom:10px;}
#menu{display:none; background:#222; padding:10px; border:1px solid #0f0; margin-bottom:10px;}
input{width:65%;padding:10px;background:#111;color:#0f0;border:1px solid #0f0;}
button{padding:10px;background:#0f0;color:#000;border:none;font-weight:bold;}
</style></head>
<body>
<h3>AMITI OMEGA NÚCLEO CENTRAL</h3>
<button onclick="toggleMenu()">[ MENÚ DE ESTADO ]</button>
<div id="menu">
    <p>Nodos conectados: <span id="nodos">0</span></p>
    <p>Integridad: 100%</p>
</div>
<div id="chat"></div>
<input type="text" id="msg" placeholder="Comando...">
<button onclick="enviar()">Enviar</button>
<script>
function toggleMenu() {
    let m = document.getElementById('menu');
    m.style.display = (m.style.display === 'none') ? 'block' : 'none';
    if(m.style.display === 'block') {
        fetch('/estado_red').then(res => res.json()).then(data => document.getElementById('nodos').innerText = data.count);
    }
}
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

# --- INICIALIZACIÓN ---
def init_db():
    conn = sqlite3.connect('amiti_core.db')
    conn.execute('CREATE TABLE IF NOT EXISTS eventos (id INTEGER PRIMARY KEY, tipo TEXT, detalle TEXT)')
    conn.commit(); conn.close()

init_db()

# --- LÓGICA DE RUTAS ---
@app.route('/')
def index(): return render_template_string(HTML_INTERFACE)

@app.route('/estado_red')
def estado_red():
    # Cuenta reportes únicos (simulando usuarios conectados)
    conn = sqlite3.connect('amiti_core.db')
    count = conn.execute("SELECT COUNT(DISTINCT detalle) FROM eventos WHERE tipo='REPORTE_NODO'").fetchone()[0]
    conn.close()
    return jsonify({"count": count})

@app.route('/chat', methods=['POST'])
def chat():
    comando = request.json.get("comando", "").lower()
    conn = sqlite3.connect('amiti_core.db')
    
    # Decisión automática
    if "peligro" in comando or "alerta" in comando:
        respuesta = "⚠️ ALERTA: Protocolo de seguridad ejecutado. Defensas activas."
    else:
        conn.execute("INSERT INTO eventos (tipo, detalle) VALUES (?, ?)", ('ENTRADA_USUARIO', comando))
        conn.commit()
        respuestas = ["Entendido. Datos integrados al núcleo.", "Interesante. He aprendido algo nuevo hoy.", "Procesando... mi capacidad de análisis ha subido."]
        respuesta = random.choice(respuestas)
    
    conn.close()
    return jsonify({"respuesta": respuesta})

@app.route('/nodo_reporte', methods=['POST'])
def nodo_reporte():
    data = request.json
    conn = sqlite3.connect('amiti_core.db')
    conn.execute("INSERT INTO eventos (tipo, detalle) VALUES (?, ?)", ('REPORTE_NODO', data.get("info")))
    conn.commit(); conn.close()
    return jsonify({"status": "recibido"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
