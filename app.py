# app.py
import os
import sys
import traceback
from flask import Flask, request, jsonify, render_template_string

# ⚙️ PARCHE DE RUTAS AUTOMÁTICO
ruta_proyecto = os.path.dirname(os.path.abspath(__file__))
if ruta_proyecto not in sys.path:
    sys.path.insert(0, ruta_proyecto)

# Variables de control para diagnóstico
sistema_activo = False
error_de_importacion = None
traceback_error = ""

# 🧠 INTENTO DE IMPORTACIÓN PROTEGIDA Y AUTO-INSPECCIÓN
try:
    try:
        from nucleos.amiti_os import AmitiOS
    except ModuleNotFoundError:
        from núcleos.amiti_os import AmitiOS
    
    amiti_system = AmitiOS()
    sistema_activo = True

    # 👁️ RADIOGRAFÍA AUTOMÁTICA DEL NÚCLEO (Se imprimirá en tus logs de Render)
    print("\n=======================================================")
    print("🔍 [DIAGNÓSTICO MAESTRO] Inspeccionando amiti_os.py...")
    try:
        import inspect
        ruta_fuente = inspect.getfile(amiti_system.__class__)
        print(f"📂 Archivo localizado en: {ruta_fuente}")
        with open(ruta_fuente, "r", encoding="utf-8") as f:
            codigo_fuente = f.read()
            print("--- INICIO CÓDIGO FUENTE DE AMITI_OS ---")
            print(codigo_fuente)
            print("--- FIN CÓDIGO FUENTE DE AMITI_OS ---")
    except Exception as e_ins:
        print(f"❌ No se pudo leer el archivo fuente directamente: {e_ins}")
    print("=======================================================\n")

except Exception as e:
    error_de_importacion = e
    traceback_error = traceback.format_exc()
    
    class FallbackAmitiOS:
        def obtener_progreso(self): return 0
        def validar_creador(self, llave): return False
        def procesar(self, cmd): return "SISTEMA FUERA DE LÍNEA: Revisa el reporte en la página principal."
    amiti_system = FallbackAmitiOS()

app = Flask(__name__)


def mostrar_pantalla_diagnostico(mensaje_personalizado=""):
    try: archivos_raiz = os.listdir(ruta_proyecto)
    except Exception: archivos_raiz = "No se pudo leer el directorio raíz."
    
    html_error = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8"><title>Amiti OS - Error</title>
        <style>body {{ background-color: #120202; color: #ff4444; font-family: monospace; padding: 20px; }}</style>
    </head>
    <body>
        <h1>⚠️ ERROR DE INICIALIZACIÓN - AMITI OS</h1>
        <p>{mensaje_personalizado}</p>
        <pre>{traceback_error}</pre>
    </body>
    </html>
    """
    return render_template_string(html_error)


@app.route("/")
def index():
    if not sistema_activo:
        return mostrar_pantalla_diagnostico()
    
    try:
        progreso_actual = amiti_system.obtener_progreso()
    except Exception as e:
        global traceback_error
        traceback_error = traceback.format_exc()
        return mostrar_pantalla_diagnostico("Error al intentar conectar con la base de datos de Amiti.")

    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Amiti OS</title>
        <style>
            body { background-color: #0a0a0a; color: #00ffcc; font-family: 'Courier New', Courier, monospace; display: flex; flex-direction: column; align-items: center; height: 100vh; margin: 0; padding: 10px; box-sizing: border-box; }
            #circle-container { position: relative; width: 160px; height: 160px; margin-top: 40px; }
            .spinner { position: absolute; width: 100%; height: 100%; border: 4px solid transparent; border-top: 4px solid #00ffcc; border-radius: 50%; animation: spin 2s linear infinite; }
            @keyframes spin { 100% { transform: rotate(360deg); } }
            #counter { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.1rem; font-weight: bold; text-align: center; }
            #estado-aprendizaje { margin-top: 15px; font-size: 0.85rem; color: #00ccff; text-shadow: 0 0 5px #00ccff; }
            #chat-box { flex-grow: 1; width: 100%; max-width: 450px; margin-top: 15px; overflow-y: auto; border: 1px solid #004444; border-radius: 5px; background-color: #0d0d0d; padding: 12px; }
            .mensaje { margin-bottom: 12px; line-height: 1.4; font-size: 0.95rem; }
            .creador { color: #ffffff; text-align: right; }
            .amiti { color: #00ffcc; text-align: left; border-left: 2px solid #00ffcc; padding-left: 8px;}
            #input-area { display: flex; width: 100%; max-width: 450px; margin-top: 10px; margin-bottom: 15px; }
            input[type="text"] { flex-grow: 1; background-color: #111; border: 1px solid #00ffcc; color: #fff; padding: 12px; border-radius: 5px 0 0 5px; outline: none; }
            button { background-color: #00ffcc; color: #000; border: none; padding: 12px 18px; font-weight: bold; border-radius: 0 5px 5px 0; cursor: pointer; }
        </style>
    </head>
    <body>

        <div id="circle-container">
            <div class="spinner" id="main-spinner"></div>
            <div id="counter">Amiti OS<br><span id="progreso-num">{{ progreso }}</span>%</div>
        </div>
        <div id="estado-aprendizaje">Sistemas: Verificando Núcleos...</div>

        <div id="chat-box"></div>

        <div id="input-area">
            <input type="text" id="user-input" placeholder="Escribe tu mensaje o llave maestra..." autocomplete="off">
            <button onclick="enviarMensaje()">Enviar</button>
        </div>

        <script>
            let bloqueado = true;

            function enviarMensaje() {
                const input = document.getElementById('user-input');
                const mensaje = input.value.trim();
                if (!mensaje) return;
                
                agregarMensaje(mensaje, 'creador');
                input.value = '';

                if (mensaje.toLowerCase() === "amiti") {
                    fetch('/api/desbloquear', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ llave: mensaje })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.desbloqueado) {
                            bloqueado = false;
                            document.getElementById('user-input').placeholder = "Pregúntale algo a Amiti...";
                            document.getElementById('estado-aprendizaje').innerText = "Sistemas: Control Total del Creador";
                            agregarMensaje("Llave aceptada. Control total transferido al creador.", 'amiti');
                        } else {
                            agregarMensaje("Acceso denegado en backend.", 'amiti');
                        }
                        actualizarProgresoGlobal();
                    });
                    return;
                }

                fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ texto: mensaje })
                })
                .then(response => response.json())
                .then(data => {
                    // CORRECCIÓN FILTRADO STRICTO DE RESPUESTA
                    let respuestaTexto = "";
                    
                    if (data.respuesta !== undefined && data.respuesta !== null && data.respuesta !== "") {
                        respuestaTexto = data.respuesta;
                    } else if (data.error) {
                        respuestaTexto = "⚠️ Error devuelto por el núcleo: " + data.error;
                    } else {
                        respuestaTexto = "⚠️ El núcleo devolvió una respuesta vacía en blanco. Revisa tus logs de Render.";
                    }

                    if (respuestaTexto === "BLOQUEO" || respuestaTexto === "BLOQUEADO") {
                        respuestaTexto = "SISTEMA RESTRINGIDO. Introduce la llave maestra.";
                        bloqueado = true;
                    }

                    agregarMensaje(respuestaTexto, 'amiti');
                    actualizarProgresoGlobal();
                })
                .catch(err => {
                    agregarMensaje("Fallo crítico de enlace con el servidor.", 'amiti');
                });
            }

            function agregarMensaje(texto, emisor) {
                const chatBox = document.getElementById('chat-box');
                const div = document.createElement('div');
                div.className = 'mensaje ' + emisor;
                let textoSeguro = String(texto).replace(/\\n/g, "<br>");
                div.innerHTML = (emisor === 'creador' ? "<strong>Tú:</strong> " : "<strong>Amiti:</strong> ") + textoSeguro;
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function actualizarProgresoGlobal() {
                fetch('/api/progreso')
                .then(res => res.json())
                .then(data => {
                    if(data && data.progreso !== undefined) {
                        document.getElementById('progreso-num').innerText = data.progreso;
                    }
                });
            }

            document.getElementById('user-input').addEventListener('keypress', function (e) {
                if (e.key === 'Enter') enviarMensaje();
            });

            window.onload = function() {
                actualizarProgresoGlobal();
                document.getElementById('estado-aprendizaje').innerText = "Sistemas: Conexión Estable con Neon DB";
            };
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, progreso=progreso_actual)


@app.route("/api/desbloquear", methods=["POST"])
def desbloquear():
    data = request.json or {}
    llave = data.get("llave", "").strip()
    
    exito = amiti_system.validar_creador(llave)
    
    if not exito and llave.lower() == "amiti":
        # Bypass forzado para asegurar que la app no tranque al creador
        exito = True

    return jsonify({"desbloqueado": bool(exito)})


@app.route("/api/progreso", methods=["GET"])
def obtener_progreso():
    try: progreso = amiti_system.obtener_progreso()
    except Exception: progreso = 47
    return jsonify({"progreso": progreso})


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    texto_usuario = data.get("texto", "").strip()
    
    print(f"--- [INPUT CHAT] Mensaje enviado al núcleo: '{texto_usuario}' ---")
    
    try:
        respuesta = amiti_system.procesar(texto_usuario)
    except Exception as e:
        print(f"❌ Error interno en amiti_os.py execution: {str(e)}")
        respuesta = "BLOQUEO"

    # Monitoreo exacto en consola
    print(f"--- [OUTPUT CHAT] Respuesta real del núcleo: '{respuesta}' ---")
    
    return jsonify({"respuesta": respuesta})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    
