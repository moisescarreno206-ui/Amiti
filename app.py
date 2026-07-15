# app.py
import os
import sys
from flask import Flask, request, jsonify, render_template_string

# ⚙️ PARCHE DE RUTAS: Obliga a Python a buscar carpetas dentro del directorio del script.
# Esto previene el 99% de los fallos de importación en celulares y servidores.
ruta_proyecto = os.path.dirname(os.path.abspath(__file__))
if ruta_proyecto not in sys.path:
    sys.path.insert(0, ruta_proyecto)

# 🧠 IMPORTACIÓN INTELIGENTE DE AMITI
try:
    # Intento 1: Importar desde carpeta sin tilde (Recomendado para Render)
    from nucleos.amiti_os import AmitiOS
except ModuleNotFoundError:
    try:
        # Intento 2: Respaldo por si tu carpeta en el celular tiene tilde
        from núcleos.amiti_os import AmitiOS
    except ModuleNotFoundError as e:
        print("\n[!] ERROR CRÍTICO: No se pudo encontrar la carpeta de los núcleos.")
        print("Asegúrate de que tu estructura de archivos sea exactamente así:")
        print("mi_proyecto/")
        print("  ├── app.py")
        print("  └── nucleos/ (o núcleos/)")
        print("        ├── __init__.py")
        print("        └── amiti_os.py\n")
        raise e

app = Flask(__name__)

# Instanciamos el cerebro que acabamos de importar de forma segura
amiti_system = AmitiOS()

@app.route("/")
def index():
    progreso_actual = amiti_system.obtener_progreso()
    
    # Interfaz HTML + CSS + JS unificada
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Amiti OS</title>
        <style>
            body {
                background-color: #0a0a0a;
                color: #00ffcc;
                font-family: 'Courier New', Courier, monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                height: 100vh;
                margin: 0;
                padding: 10px;
                box-sizing: border-box;
            }
            #circle-container {
                position: relative;
                width: 160px;
                height: 160px;
                margin-top: 40px;
                transition: opacity 1s;
            }
            .spinner {
                position: absolute;
                width: 100%;
                height: 100%;
                border: 4px solid transparent;
                border-top: 4px solid #00ffcc;
                border-radius: 50%;
                animation: spin 2s linear infinite;
            }
            .spinner::before {
                content: '';
                position: absolute;
                top: 5px; left: 5px; right: 5px; bottom: 5px;
                border: 4px solid transparent;
                border-left: 4px solid #00ccff;
                border-radius: 50%;
                animation: spin 3s linear infinite reverse;
            }
            @keyframes spin { 100% { transform: rotate(360deg); } }
            
            #counter {
                position: absolute;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                font-size: 1.1rem;
                font-weight: bold;
                text-align: center;
                line-height: 1.3;
            }

            #estado-aprendizaje {
                margin-top: 15px;
                font-size: 0.85rem;
                color: #00ccff;
                text-shadow: 0 0 5px #00ccff;
                height: 20px;
            }
            
            #chat-box {
                flex-grow: 1;
                width: 100%;
                max-width: 450px;
                margin-top: 15px;
                overflow-y: auto;
                border: 1px solid #004444;
                border-radius: 5px;
                background-color: #0d0d0d;
                padding: 12px;
                box-shadow: 0 0 15px rgba(0,255,204,0.1);
                display: none;
            }
            .mensaje { margin-bottom: 12px; line-height: 1.4; font-size: 0.95rem; }
            .creador { color: #ffffff; text-align: right; }
            .amiti { color: #00ffcc; text-align: left; border-left: 2px solid #00ffcc; padding-left: 8px;}
            
            #input-area {
                display: flex;
                width: 100%;
                max-width: 450px;
                margin-top: 10px;
                margin-bottom: 15px;
            }
            input[type="text"] {
                flex-grow: 1;
                background-color: #111;
                border: 1px solid #00ffcc;
                color: #fff;
                padding: 12px;
                border-radius: 5px 0 0 5px;
                outline: none;
                font-family: inherit;
            }
            button {
                background-color: #00ffcc;
                color: #000;
                border: none;
                padding: 12px 18px;
                font-weight: bold;
                border-radius: 0 5px 5px 0;
                cursor: pointer;
                font-family: inherit;
                transition: background-color 0.2s;
            }
            button:hover {
                background-color: #00ccff;
            }
        </style>
    </head>
    <body>

        <div id="circle-container">
            <div class="spinner" id="main-spinner"></div>
            <div id="counter">Amiti OS<br><span id="progreso-num">{{ progreso }}</span>%</div>
        </div>
        <div id="estado-aprendizaje">Modo: Espera Segura</div>

        <div id="chat-box"></div>

        <div id="input-area">
            <input type="text" id="user-input" placeholder="Escribe la contraseña maestra..." autocomplete="off">
            <button onclick="enviarMensaje()">Enviar</button>
        </div>

        <script>
            let bloqueado = true;
            let progresoActual = parseInt(document.getElementById('progreso-num').innerText);

            function enviarMensaje() {
                const input = document.getElementById('user-input');
                const mensaje = input.value.trim();
                if (!mensaje) return;
                
                agregarMensaje(mensaje, 'creador');
                input.value = '';

                if (bloqueado && mensaje === "Amiti") {
                    bloqueado = false;
                    document.getElementById('user-input').placeholder = "Pregúntale algo a Amiti...";
                    document.getElementById('chat-box').style.display = 'block';
                    document.getElementById('estado-aprendizaje').innerText = "Sistemas: Control Total del Creador";
                    
                    fetch('/api/desbloquear', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ llave: "Amiti" })
                    });

                    agregarMensaje("Llave aceptada. Control total transferido al creador. Todos los núcleos en línea.", 'amiti');
                    return;
                }

                if (bloqueado) {
                    agregarMensaje("Acceso denegado. Se requiere llave de seguridad.", 'amiti');
                    return;
                }

                let esInvestigacion = mensaje.toLowerCase().includes("investiga") || mensaje.toLowerCase().includes("busca");
                if (esInvestigacion) {
                    simularInvestigacionWeb();
                }

                fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ texto: mensaje })
                })
                .then(response => response.json())
                .then(data => {
                    agregarMensaje(data.respuesta, 'amiti');
                    actualizarProgresoGlobal();
                })
                .catch(err => console.error("Error de comunicación:", err));
            }

            function agregarMensaje(texto, emisor) {
                const chatBox = document.getElementById('chat-box');
                const div = document.createElement('div');
                div.className = 'mensaje ' + emisor;
                div.innerHTML = (emisor === 'creador' ? "<strong>Tú:</strong> " : "<strong>Amiti:</strong> ") + texto.replace(/\\n/g, "<br>");
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function simularInvestigacionWeb() {
                let duracion = 5; 
                let contadorSegundos = 0;
                document.getElementById('estado-aprendizaje').innerText = "🌐 Investigando en la red y extrayendo recursos...";
                document.getElementById('main-spinner').style.borderTopColor = "#00ccff";
                
                let intervalo = setInterval(() => {
                    progresoActual = Math.min(100, progresoActual + 1);
                    document.getElementById('progreso-num').innerText = progresoActual;
                    contadorSegundos++;
                    
                    if (contadorSegundos >= duracion) {
                        clearInterval(intervalo);
                        document.getElementById('estado-aprendizaje').innerText = "Sistemas: Base de Conocimiento Actualizada";
                        document.getElementById('main-spinner').style.borderTopColor = "#00ffcc";
                    }
                }, 1000);
            }

            function actualizarProgresoGlobal() {
                fetch('/api/progreso')
                .then(res => res.json())
                .then(data => {
                    progresoActual = data.progreso;
                    document.getElementById('progreso-num').innerText = progresoActual;
                });
            }

            document.getElementById('user-input').addEventListener('keypress', function (e) {
                if (e.key === 'Enter') enviarMensaje();
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, progreso=progreso_actual)

@app.route("/api/desbloquear", methods=["POST"])
def desbloquear():
    data = request.json
    llave = data.get("llave", "")
    exito = amiti_system.validar_creador(llave)
    return jsonify({"desbloqueado": exito})

@app.route("/api/progreso", methods=["GET"])
def obtener_progreso():
    return jsonify({"progreso": amiti_system.obtener_progreso()})

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    texto_usuario = data.get("texto", "")
    respuesta = amiti_system.procesar(texto_usuario)
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    
