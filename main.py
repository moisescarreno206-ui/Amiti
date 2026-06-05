from flask import Flask, request, jsonify, render_template_string
import sqlite3, os, random

app = Flask(__name__)

# --- INTERFAZ HTML ---
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head><title>AMITI OMEGA</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{background:#000;color:#0f0;font-family:monospace;padding:15px;} #chat{height:300px;border:1px solid #0f0;overflow-y:scroll;padding:10px;margin-bottom:10px;} input{width:65%;padding:10px;background:#111;color:#0f0;border:1px solid #0f0;} button{padding:10px;background:#0f0;color:#000;border:none;font-weight:bold;}</style></head>
<body><h3>AMITI OMEGA NÚCLEO CENTRAL</h3><div id="chat"></div><input type="text" id="msg" placeholder="Habla con AMITI..."><button onclick="enviar()">Enviar</button>
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

# --- INICIALIZACIÓN ---
def init_db():
    conn = sqlite3.connect('amiti_core.db')
    conn.execute('CREATE TABLE IF NOT EXISTS eventos (id INTEGER PRIMARY KEY, tipo TEXT, detalle TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- RUTAS ---
@app.route('/')
def index(): return render_template_string(HTML_INTERFACE)

@app.route('/chat', methods=['POST'])
def chat():
    comando = request.json.get("comando", "")
    conn = sqlite3.connect('amiti_core.db')
    conn.execute("INSERT INTO eventos (tipo, detalle) VALUES (?, ?)", ('ENTRADA_USUARIO', comando))
    conn.commit()
    
    cmd_lower = comando.lower()
    if "estado" in cmd_lower: 
        respuesta = "SISTEMA OMEGA: Operativo. Integridad de red al 100%."
    elif "diagnóstico" in cmd_lower: 
        count = conn.execute("SELECT COUNT(*) FROM eventos").fetchone()[0]
        respuesta = f"ANÁLISIS: {count} nodos de información procesados. Mi base de conocimiento se expande."
    elif "hola" in cmd_lower:
        respuesta = "Saludos, operador. Estoy conectada y lista para analizar nuevos datos."
    else: 
        respuestas = ["He registrado tu aporte. Analizando patrones.", "Interesante. Dato almacenado para evolución.", "Procesando información. Memoria actualizada."]
        respuesta = random.choice(respuestas)
    
    conn.close()
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
