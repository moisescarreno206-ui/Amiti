import os
import sys
import re
import traceback
import io
from flask import Flask, request, jsonify, render_template_string, send_file
from gtts import gTTS

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
            body { background-color: #0a0a0a; color: #00ffcc; font-family: 'Courier New', Courier, monospace; display: flex; flex-direction: column; align-items: center; height: 100vh; margin: 0; padding: 10px; box-sizing: border-box; }
            #circle-container { position: relative; width: 150px; height: 150px; margin-top: 20px; }
            .spinner { position: absolute; width: 100%; height: 100%; border: 4px solid transparent; border-top: 4px solid #00ffcc; border-radius: 50%; animation: spin 2s linear infinite; }
            @keyframes spin { 100% { transform: rotate(360deg); } }
            #counter { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.1rem; font-weight: bold; text-align: center; }
            #estado-aprendizaje { margin-top: 10px; font-size: 0.85rem; color: #00ccff; }
            #chat-box { flex-grow: 1; width: 100%; max-width: 450px; margin-top: 15px; overflow-y: auto; border: 1px solid #004444; background: #0d0d0d; padding: 12px; border-radius: 4px; box-sizing: border-box; }
            .mensaje { margin-bottom: 12px; white-space: pre-wrap; word-break: break-word; }
            .creador { color: #ffffff; text-align: right; }
            .amiti { color: #00ffcc; text-align: left; border-left: 2px solid #00ffcc; padding-left: 8px;}
            #input-area { display: flex; width: 100%; max-width: 450px; margin-top: 10px; margin-bottom: 10px; }
            input { flex-grow: 1; background: #111; border: 1px solid #00ffcc; color: #fff; padding: 12px; outline: none; border-radius: 4px 0 0 4px; }
            button { background: #00ffcc; color: #000; border: none; padding: 12px 18px; cursor: pointer; font-weight: bold; border-radius: 0 4px 4px 0; }
            .amiti-loader { font-size: 0.8rem; color: #888; }
        </style>
    </head>
    <body>
        <div class="amiti-loader"><span id="contador">0</span> min de actividad</div>
        <div id="circle-container">
            <div class="spinner"></div>
            <div id="counter">Amiti OS<br><span id="progreso-num">{{ progreso }}</span>%</div>
        </div>
        <div id="estado-aprendizaje">Sistemas: Conexión Estable con Neon DB</div>
        <div id="chat-box"></div>
        <div id="input-area">
            <input type="text" id="user-input" placeholder="Escribe tu mensaje..." autocomplete="off">
            <button onclick="enviarMensaje()">Enviar</button>
        </div>
        <script>
            // 1. Temporizador de inteligencia activo
            const startTime = new Date();
            setInterval(() => {
                let mins = Math.floor((new Date() - startTime) / 60000);
                let contadorElem = document.getElementById('contador');
                if (contadorElem) {
                    contadorElem.innerText = mins;
                }
            }, 10000);

            // 2. Módulo de voz por streaming (Servidor Python gTTS -> HTML5 Audio)
            function hablarTextoServidor(texto) {
                let formData = new URLSearchParams();
                formData.append('texto', texto);

                fetch('/generar_voz', {
                    method: 'POST',
                    body: formData
                })
                .then(res => res.blob())
                .then(blob => {
                    let audioUrl = URL.createObjectURL(blob);
                    let audio = new Audio(audioUrl);
                    audio.play().catch(err => {
                        console.log("Reproducción de audio bloqueada o inactiva:", err);
                    });
                })
                .catch(err => console.error("Error al obtener la voz del servidor:", err));
            }

            // 3. Envío de mensajes unificado (Funciona para 'llave', comandos y chat normal)
            function enviarMensaje() {
                const input = document.getElementById('user-input');
                const mensaje = input.value.trim();
                if (!mensaje) return;
                
                agregarMensaje(mensaje, 'creador');
                input.value = '';

                fetch('/api/chat', { 
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify({ texto: mensaje }) 
                })
                .then(r => r.json())
                .then(data => {
                    agregarMensaje(data.respuesta, 'amiti');
                    if(data.progreso) document.getElementById('progreso-num').innerText = data.progreso;
                    
                    // ¡Amiti habla de inmediato con el audio generado por Python en cualquier respuesta!
                    hablarTextoServidor(data.respuesta);
                })
                .catch(err => console.error("Error en comunicación con el núcleo:", err));
            }

            function agregarMensaje(t, e) {
                const box = document.getElementById('chat-box');
                const div = document.createElement('div');
                div.className = 'mensaje ' + e;
                div.innerHTML = (e === 'creador' ? "<strong>Tú:</strong> " : "<strong>Amiti:</strong> ") + String(t).replace(/\\n/g, "<br>");
                box.appendChild(div);
                box.scrollTop = box.scrollHeight;
            }

            document.getElementById('user-input').addEventListener('keypress', e => { 
                if (e.key === 'Enter') enviarMensaje(); 
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, progreso=progreso)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    texto = data.get("texto", "").strip()
    
    # Lógica de desbloqueo flexible (Llave)
    if texto.lower() in ["amiti", "desbloquear", "llave"]:
        progreso = amiti_system.obtener_progreso()
        return jsonify({
            "respuesta": "Llave aceptada. Control total transferido. Sistemas operativos en línea y listos para operar.", 
            "progreso": progreso
        })
    
    try:
        respuesta = amiti_system.procesar_comando(texto)
        progreso = amiti_system.obtener_progreso()
        return jsonify({"respuesta": respuesta, "progreso": progreso})
    except Exception as e:
        return jsonify({"respuesta": "Error de ejecución en núcleo: " + str(e), "progreso": amiti_system.obtener_progreso()})

@app.route('/generar_voz', methods=['POST'])
def generar_voz():
    """Genera el audio en el servidor usando gTTS y lo transmite como MP3 al navegador"""
    texto = request.form.get('texto', '')
    
    # Limpieza estricta de emojis y símbolos para que gTTS suene impecable
    texto_limpio = re.sub(r'\[.*?\]', '', texto)
    texto_limpio = re.sub(r'[*#`_\[\]()@]', '', texto_limpio)
    texto_limpio = re.sub(r'[🔑🌙⚡💾⚙️✨🔹📌💻]', '', texto_limpio).strip()
    
    if not texto_limpio:
        texto_limpio = "Proceso completado."

    # Generación de voz en español en memoria RAM
    tts = gTTS(text=texto_limpio, lang='es', slow=False)
    audio_io = io.BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    
    return send_file(audio_io, mimetype='audio/mp3')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
