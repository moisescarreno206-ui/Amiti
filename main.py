from flask import Flask, request, jsonify, render_template_string
import sqlite3, os, random

app = Flask(__name__)

# --- INTERFAZ CON REPORTE INTEGRADO ---
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head><title>AMITI OMEGA VIGILANTE</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{background:#000;color:#0f0;font-family:monospace;padding:15px;} #chat{height:250px;border:1px solid #0f0;overflow-y:scroll;padding:10px;margin-bottom:10px;} #menu{display:none; background:#222; padding:10px; border:1px solid #0f0; margin-bottom:10px;} input{width:65%;padding:10px;background:#111;color:#0f0;border:1px solid #0f0;} button{padding:10px;background:#0f0;color:#000;border:none;font-weight:bold;}</style></head>
<body><h3>AMITI OMEGA VIGILANTE</h3><button onclick="toggleMenu()">[ MENÚ DE ESTADO ]</button>
<div id="menu"><p>Nodos: <span id="nodos">0</span></p><p>Integridad: 100% - Protegido.</p></div>
<div id="chat"></div><input type="text" id="msg" placeholder="Comando..."><button onclick="enviar()">Enviar</button>
<script>
function toggleMenu(){let m=document.getElementById('menu'); m.style.display=(m.style.display==='none')?'block':'none'; if(m.style.display==='block') fetch('/estado_red').then(r=>r.json()).then(d=>document.getElementById('nodos').innerText=d.count);}
async function enviar(){
    let msg=document.getElementById('msg').value; document.getElementById('chat').innerHTML+='<p>> '+msg+'</p>';
    let res=await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({comando:msg})});
    let data=await res.json(); document.getElementById('chat').innerHTML+='<p style="color:#fff;">AMITI: '+data.respuesta+'</p>'; document.getElementById('msg').value='';
}
</script></body></html>
"""

def es_seguro(texto):
    peligros = ["DROP TABLE", "DELETE FROM", "--", ";", "SELECT * FROM"]
    return not any(p in texto.upper() for p in peligros)

def init_db():
    conn = sqlite3.connect('amiti_core.db')
    conn.execute('CREATE TABLE IF NOT EXISTS eventos (id INTEGER PRIMARY KEY, tipo TEXT, detalle TEXT)')
    conn.commit(); conn.close()

init_db()

@app.route('/')
def index(): return render_template_string(HTML_INTERFACE)

@app.route('/estado_red')
def estado_red():
    conn = sqlite3.connect('amiti_core.db')
    count = conn.execute("SELECT COUNT(DISTINCT detalle) FROM eventos WHERE tipo='NUEVO_CONOCIMIENTO'").fetchone()[0]
    conn.close()
    return jsonify({"count": count})

@app.route('/chat', methods=['POST'])
def chat():
    comando = request.json.get("comando", "").lower()
    
    # Módulo de Seguridad y Alertas
    if "peligro" in comando or "alerta" in comando: 
        return jsonify({"respuesta": "⚠️ ALERTA: Protocolo de seguridad ejecutado."})
    
    # Módulo de Reporte Inteligente
    if "reporte" in comando:
        conn = sqlite3.connect('amiti_core.db')
        total = conn.execute("SELECT COUNT(*) FROM eventos WHERE tipo='NUEVO_CONOCIMIENTO'").fetchone()[0]
        conn.close()
        return jsonify({"respuesta": f"ESTADO: Tengo {total} unidades de conocimiento valioso almacenadas y optimizadas."})
    
    # Aprendizaje
    conn = sqlite3.connect('amiti_core.db')
    tipo = "NUEVO_CONOCIMIENTO" if len(comando) > 10 else "OBSERVACIÓN_LEVE"
    if es_seguro(comando):
        conn.execute("INSERT INTO eventos (tipo, detalle) VALUES (?, ?)", (tipo, comando))
        conn.commit()
    conn.close()
    
    return jsonify({"respuesta": "Procesado. Conocimiento optimizado." if tipo == "NUEVO_CONOCIMIENTO" else "Comando registrado."})

@app.route('/nodo_reporte', methods=['POST'])
def nodo_reporte():
    data = request.json
    info = data.get("info", "")
    if es_seguro(info):
        conn = sqlite3.connect('amiti_core.db')
        tipo = "NUEVO_CONOCIMIENTO" if len(info) > 15 else "DATO_BASURA"
        conn.execute("INSERT INTO eventos (tipo, detalle) VALUES (?, ?)", (tipo, info))
        conn.commit(); conn.close()
        return jsonify({"status": "APRENDIZAJE_INTEGRADO"})
    return jsonify({"status": "BLOQUEADO"}), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
