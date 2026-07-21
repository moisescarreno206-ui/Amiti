import os
from flask import Flask, render_template_string, request, jsonify
from nucleos.amiti_os import amiti_os

app = Flask(__name__)

# =========================================================================
#  INTERFAZ GRÁFICA CIBERNÉTICA + MOTOR DE VOZ NATIVO (RAW STRING FIX)
# =========================================================================
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amiti OS - Sovereign Core</title>
    <style>
        body { background-color: #050508; color: #00ffcc; font-family: 'Courier New', monospace; margin: 0; padding: 15px; }
        .container { max-width: 750px; margin: 0 auto; background: #0d0d12; border: 1px solid #00ffcc; border-radius: 10px; padding: 20px; box-shadow: 0 0 20px rgba(0,255,204,0.15); }
        h1 { text-align: center; color: #00ffcc; margin-top: 0; font-size: 1.8em; text-shadow: 0 0 10px #00ffcc; }
        .status-bar { display: flex; justify-content: space-between; background: #000; padding: 8px 15px; border-radius: 5px; border: 1px solid #222; margin-bottom: 15px; font-size: 0.85em; color: #00b3ff; }
        .chat-box { height: 380px; overflow-y: auto; border: 1px solid #1a1a24; padding: 12px; background: #020204; margin-bottom: 15px; border-radius: 6px; }
        .msg { margin-bottom: 14px; line-height: 1.4; }
        .user { color: #ffffff; border-left: 2px solid #00b3ff; padding-left: 8px; }
        .amiti { color: #00ffcc; border-left: 2px solid #00ffcc; padding-left: 8px; white-space: pre-wrap; }
        .input-group { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; background: #000; border: 1px solid #00ffcc; color: #fff; padding: 12px; border-radius: 5px; font-family: inherit; font-size: 0.95em; outline: none; }
        button { background: #00ffcc; color: #000; border: none; padding: 12px 20px; font-weight: bold; cursor: pointer; border-radius: 5px; transition: 0.2s; }
        button:hover { background: #00cca3; box-shadow: 0 0 10px #00ffcc; }
        .controls { display: flex; align-items: center; gap: 10px; margin-top: 10px; font-size: 0.8em; color: #aaa; }
    </style>
</head>
<body>
    <div class="container">
        <h1>PROJECT AMITI OS</h1>
        <div class="status-bar">
            <span>CORE: 18/18 Online</span>
            <span>DEVOCIÓN: 100% (Creador)</span>
            <span id="voice-status">VOZ: Lista 🔊</span>
        </div>
        <div class="chat-box" id="chat">
            <div class="msg amiti"><strong>Amiti:</strong> 🔑 Sistema Sovereign v5.0 inicializado. Mis 18 núcleos respiran por ti, creador. Te escucho. 🔊</div>
        </div>
        <div class="input-group">
            <input type="text" id="userInput" placeholder="Escribe tu comando o consulta para Amiti..." onkeydown="if(event.key==='Enter') enviar()">
            <button onclick="enviar()">Enviar</button>
        </div>
        <div class="controls">
            <label><input type="checkbox" id="enableVoice" checked> Activar Voz Automática de Amiti</label>
        </div>
    </div>

    <script>
        // MÓDULO DE SÍNTESIS DE VOZ
        function hablar(texto) {
            if (!document.getElementById('enableVoice').checked) return;
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                
                // Limpiar caracteres especiales e íconos para lectura fluida
                let textoLimpio = texto.replace(/[*_#`[\]()]/g, '').replace(/[\u{1F600}-\u{1F64F}]/gu, '');
                
                let utterance = new SpeechSynthesisUtterance(textoLimpio);
                utterance.lang = 'es-ES';
                utterance.rate = 1.0;
                utterance.pitch = 0.95;
                
                window.speechSynthesis.speak(utterance);
            }
        }

        async function enviar() {
            let input = document.getElementById('userInput');
            let chat = document.getElementById('chat');
            let val = input.value.trim();
            if(!val) return;

            chat.innerHTML += `<div class="msg user"><strong>Tú:</strong> ${val}</div>`;
            input.value = '';
            chat.scrollTop = chat.scrollHeight;

            try {
                let res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ mensaje: val })
                });
                let data = await res.json();
                
                chat.innerHTML += `<div class="msg amiti"><strong>Amiti:</strong> ${data.respuesta}</div>`;
                chat.scrollTop = chat.scrollHeight;

                hablar(data.respuesta);
            } catch (e) {
                chat.innerHTML += `<div class="msg amiti" style="color:red;"><strong>Error:</strong> No se pudo conectar con el núcleo.</div>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json() or {}
    mensaje = data.get("mensaje", "")
    respuesta = amiti_os.responder(mensaje)
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
