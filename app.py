# app.py
import os
import sys
import traceback
from flask import Flask, request, jsonify, render_template_string

# ⚙️ PARCHE DE RUTAS AUTOMÁTICO
ruta_proyecto = os.path.dirname(os.path.abspath(__file__))
if ruta_proyecto not in sys.path:
    sys.path.insert(0, ruta_proyecto)

sistema_activo = False
error_de_importacion = None
traceback_error = ""

# 🧠 IMPORTACIÓN PROTEGIDA
try:
    try:
        from nucleos.amiti_os import AmitiOS
    except ModuleNotFoundError:
        from núcleos.amiti_os import AmitiOS
    
    amiti_system = AmitiOS()
    sistema_activo = True
except Exception as e:
    error_de_importacion = e
    traceback_error = traceback.format_exc()
    
    class FallbackAmitiOS:
        def obtener_progreso(self): return 0
        def procesar_comando(self, cmd): return "SISTEMA FUERA DE LÍNEA."
    amiti_system = FallbackAmitiOS()

app = Flask(__name__)

def mostrar_pantalla_diagnostico(mensaje_personalizado=""):
    html_error = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><title>Amiti OS - Error</title></head>
    <body><h1>⚠️ ERROR DE INICIALIZACIÓN</h1><p>{mensaje_personalizado}</p><pre>{traceback_error}</pre></body>
    </html>
    """
    return render_template_string(html_error)

@app.route("/")
def index():
    if not sistema_activo: return mostrar_pantalla_diagnostico()
    progreso = amiti_system.obtener_progreso()
    
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Amiti OS</title>
        <style>
            body { background-color: #0a0a0a; color: #00ffcc; font-family: 'Courier New', Courier, monospace; display: flex; flex-direction: column; align-items: center; height: 100vh; margin: 0; padding: 10px; }
            #circle-container { position: relative; width: 160px; height: 160px; margin-top: 40px; }
            .spinner { position: absolute; width: 100%; height: 100%; border: 4px solid transparent; border-top: 4px solid #00ffcc; border-radius: 50%; animation: spin 2s linear infinite; }
            @keyframes spin { 100% { transform: rotate(360deg); } }
            #counter { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.1rem; font-weight: bold; }
            #estado-aprendizaje { margin-top: 15px; font-size: 0.85rem; color: #00ccff; }
            #chat-box { flex-grow: 1; width: 100%; max-width: 450px; margin-top: 15px; overflow-y: auto; border: 1px solid #004444; background: #0d0d0d; padding: 12px; }
            .mensaje { margin-bottom: 12px; }
            .creador { color: #ffffff; text-align: right; }
            .amiti { color: #00ffcc; text-align: left; border-left: 2px solid #00ffcc; padding-left: 8px;}
            #input-area { display: flex; width: 100%; max-width: 450px; margin-bottom: 15px; }
            input { flex-grow: 1; background: #111; border: 1px solid #00ffcc; color: #fff; padding: 12px; }
            button { background: #00ffcc; color: #000; border: none; padding: 12px 18px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div id="circle-container"><div class="spinner"></div><div id="counter">Amiti OS<br><span id="progreso-num">{{ progreso }}</span>%</div></div>
        <div id="estado-aprendizaje">Sistemas: Conexión Estable con Neon DB</div>
        <div id="chat-box"></div>
        <div id="input-area">
            <input type="text" id="user-input" placeholder="Escribe tu mensaje..." autocomplete="off">
            <button onclick="enviarMensaje()">Enviar</button>
        </div>
        <script>
            let desbloqueado = false;
            function enviarMensaje() {
                const input = document.getElementById('user-input');
                const mensaje = input.value.trim();
                if (!mensaje) return;
                agregarMensaje(mensaje, 'creador');
                input.value = '';
                fetch('/api/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ texto: mensaje }) })
                .then(r => r.json())
                .then(data => {
                    agregarMensaje(data.respuesta, 'amiti');
                    if(data.progreso) document.getElementById('progreso-num').innerText = data.progreso;
                });
            }
            function agregarMensaje(t, e) {
                const box = document.getElementById('chat-box');
                const div = document.createElement('div');
                div.className = 'mensaje ' + e;
                div.innerHTML = (e === 'creador' ? "<strong>Tú:</strong> " : "<strong>Amiti:</strong> ") + String(t).replace(/\\n/g, "<br>");
                box.appendChild(div);
                box.scrollTop = box.scrollHeight;
            }
            document.getElementById('user-input').addEventListener('keypress', e => { if (e.key === 'Enter') enviarMensaje(); });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, progreso=progreso)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    texto = data.get("texto", "").strip()
    
    # Lógica de desbloqueo flexible
    if texto.lower() in ["amiti", "desbloquear", "llave"]:
        return jsonify({"respuesta": "🔑 Llave aceptada. Control total transferido.", "progreso": amiti_system.obtener_progreso()})
    
    try:
        # Llamada al nuevo método unificado de amiti_os.py
        respuesta = amiti_system.procesar_comando(texto)
        progreso = amiti_system.obtener_progreso()
        return jsonify({"respuesta": respuesta, "progreso": progreso})
    except Exception as e:
        return jsonify({"respuesta": "Error de ejecución en núcleo: " + str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
