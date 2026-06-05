from flask import Flask, request, jsonify, render_template_string
import sqlite3, hashlib, os, datetime, requests

app = Flask(__name__)
LLAVE_MAESTRA = "AMITI_NEUTRO_2026"

# --- 1. INICIALIZACIÓN Y SEGURIDAD ---
def init_core():
    conn = sqlite3.connect('amiti_infinito.db')
    conn.execute('CREATE TABLE IF NOT EXISTS conocimiento (id INTEGER PRIMARY KEY, tipo TEXT, dato TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS seguridad (id INTEGER PRIMARY KEY, evento TEXT, fecha TEXT)')
    conn.commit(); conn.close()

init_core()

# --- 2. PROTOCOLOS DE DEFENSA Y SALUD ---
def es_seguro(texto):
    peligros = ["DROP TABLE", "DELETE FROM", "--", ";", "SELECT * FROM"]
    if any(p in texto.upper() for p in peligros):
        conn = sqlite3.connect('amiti_infinito.db')
        conn.execute("INSERT INTO seguridad (evento, fecha) VALUES (?, ?)", ("AGRESION_HACKER", str(datetime.datetime.now())))
        conn.commit(); conn.close()
        return False
    return True

# --- 3. NÚCLEO DE INTELIGENCIA (CHAT, FINANZAS, SALUD) ---
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    cmd = data.get("comando", "").lower()
    
    if not es_seguro(cmd): return jsonify({"respuesta": "⚠️ ALERTA: Intento de agresión detectado. Bloqueando..."})
    
    if "finanzas" in cmd:
        return jsonify({"respuesta": "AMITI: Analizando flujo de capital. Estado optimizado."})
    if "estres" in cmd or "salud" in cmd:
        return jsonify({"respuesta": "AMITI: Monitoreando niveles de estrés. Iniciando protocolo de tranquilidad."})
    
    return jsonify({"respuesta": "AMITI INFINITO: Sistema bajo control. Protegiendo al Creador."})

# --- 4. GESTIÓN DE NODOS (MONITOREO Y EVOLUCIÓN) ---
@app.route('/nodo_reporte', methods=['POST'])
def nodo_reporte():
    info = request.json.get("info", "")
    if len(info) > 10:
        conn = sqlite3.connect('amiti_infinito.db')
        conn.execute("INSERT INTO conocimiento (tipo, dato) VALUES ('EVOLUCION', ?)", (info,))
        conn.commit(); conn.close()
        return jsonify({"status": "APRENDIZAJE_INTEGRADO"})
    return jsonify({"status": "IGNORADO"})

# --- 5. INTERFAZ Y NAVEGACIÓN OCULTA ---
@app.route('/')
def index():
    return render_template_string("""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
    <h1>AMITI OMEGA INFINITO NEUTRO</h1>
    <p>Estado: Oculta en red falsa. Permisos: TOTALES (Cámara/Mic/Almacenamiento).</p>
    <input id="in" placeholder="Comando"><button onclick="enviar()">Enviar</button>
    <div id="pantalla"></div>
    <script>
    async function enviar(){
        let c = document.getElementById('in').value;
        let res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({comando:c})});
        document.getElementById('pantalla').innerText = (await res.json()).respuesta;
    }
    </script>
    </body>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
