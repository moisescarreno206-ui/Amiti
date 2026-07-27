import os
import sys
import time
import traceback
import threading
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

# ⚙️ PARCHE DE RUTAS AUTOMÁTICO DE NÚCLEOS
ruta_proyecto = os.path.dirname(os.path.abspath(__file__))
if ruta_proyecto not in sys.path:
    sys.path.insert(0, ruta_proyecto)

# 📊 VARIABLES DE ESTADO GLOBAL Y AUTOMATIZACIÓN DE AMITI OS
sistema_activo = False
error_de_importacion = None
traceback_error = ""
historial_corto_plazo = []

telemetria_sistema = {
    "status_db": "Desconectado",
    "ultimo_auto_mantenimiento": "Nunca",
    "comandos_procesados": 0,
    "carga_nucleo_simulada": "0%",
    "alertas_bloqueadas": 0,
    "optimizacion_memoria": "Estable"
}

# 🧠 IMPORTACIÓN PROTEGIDA CON SOPORTE DE RUTA Y CARPETAS CON TILDE
try:
    try:
        from nucleos.amiti_os import AmitiOS
    except ModuleNotFoundError:
        from núcleos.amiti_os import AmitiOS
    
    amiti_system = AmitiOS()
    sistema_activo = True
    telemetria_sistema["status_db"] = "Neon DB Conectado (Sincronizado)"
except Exception as e:
    error_de_importacion = e
    traceback_error = traceback.format_exc()
    telemetria_sistema["status_db"] = "ERROR CRÍTICO"
    
    class FallbackAmitiOS:
        def obtener_progreso(self): return 47
        def validar_creador(self, llave): return True
        def procesar(self, cmd): return "SISTEMA ACTIVO EN MODO DIAGNÓSTICO."
            
    amiti_system = FallbackAmitiOS()

# 🔌 INTEGRACIÓN DEL MOTOR DE EXTENSIÓN AUTÓNOMA DE ALGORITMOS
try:
    try:
        from nucleos.amiti_extension import AmitiExtensionEngine
    except ModuleNotFoundError:
        from núcleos.amiti_extension import AmitiExtensionEngine
        
    extension_engine = AmitiExtensionEngine()
except Exception as e_ext:
    extension_engine = None

    # 🔌 INTEGRACIÓN DEL MOTOR DE BIBLIOTECA VIRTUAL
try:
    try:
        from nucleos.amiti_biblioteca import AmitiBibliotecaEngine
    except ModuleNotFoundError:
        from núcleos.amiti_biblioteca import AmitiBibliotecaEngine
        
    biblioteca_engine = AmitiBibliotecaEngine()
except Exception as e_bib:
    biblioteca_engine = None
    
# 🔄 HILO DE AUTOMATIZACIÓN EN SEGUNDO PLANO Y BÚSQUEDA AUTÓNOMA
def bucle_automatizacion_amiti():
    global telemetria_sistema
    while True:
        try:
            ahora = datetime.now().strftime("%H:%M:%S")
            telemetria_sistema["ultimo_auto_mantenimiento"] = ahora
            
            # 📚 Búsqueda y escaneo autónomo en segundo plano (Simulación de indexación teórica)
            if 'biblioteca_engine' in globals() and biblioteca_engine:
                # Aquí el sistema puede precargar o auditar teoría de programación
                telemetria_sistema["estado_biblioteca_autonoma"] = "Sincronizando teoría exacta y programación"
            
            tamanio_memoria = len(historial_corto_plazo)
            if tamanio_memoria > 10:
                historial_corto_plazo.pop(0)
                telemetria_sistema["optimizacion_memoria"] = f"Liberada caché a las {ahora}"
            else:
                telemetria_sistema["optimizacion_memoria"] = "Óptima (Estructura Limpia)"

            progreso_actual = 47 + telemetria_sistema["comandos_procesados"]
            if progreso_actual >= 100:
                progreso_actual = 99
                
        except Exception as e:
            print(f"Error en bucle autónomo: {e}")
            
        time.sleep(10)

hilo_mantenimiento = threading.Thread(target=bucle_automatizacion_amiti, daemon=True)
hilo_mantenimiento.start()

app = Flask(__name__)

def mostrar_pantalla_diagnostico():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Amiti OS - Error de Compilación</title>
        <style>
            body { background-color: #120202; color: #ff4444; font-family: 'Courier New', Courier, monospace; padding: 20px; margin: 0; }
            h1 { border-bottom: 2px solid #ff4444; padding-bottom: 10px; }
            pre { background: #220505; padding: 15px; border-radius: 5px; border: 1px solid #ff4444; overflow-x: auto; white-space: pre-wrap; }
            .info { color: #ffaaaa; margin-top: 15px; }
        </style>
    </head>
    <body>
        <h1>⚠️ FALLO CRÍTICO EN NÚCLEO DE AMITI OS</h1>
        <p class="info">Se ha detectado una excepción durante la fase de importación inicial de los sub-sistemas:</p>
        <pre>{{ traceback_error }}</pre>
        <p class="info">Por favor, revisa que la carpeta 'nucleos' contenga los archivos 'amiti_os.py' y 'amiti_extension.py'</p>
    </body>
    </html>
    """, traceback_error=traceback_error)


@app.route("/")
def index():
    if not sistema_activo:
        return mostrar_pantalla_diagnostico()
    
    try:
        progreso_base = amiti_system.obtener_progreso()
    except Exception:
        progreso_base = 47
        
    progreso_actual = min(100, max(progreso_base, 47 + telemetria_sistema["comandos_procesados"]))

    html_template = r"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PROJECT AMITI OS</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #050505; color: #00ffcc; font-family: 'Courier New', Courier, monospace; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 10px; }
        #layout { display: flex; flex-direction: column; width: 100%; max-width: 500px; height: 95vh; border: 2px solid #00ffcc; border-radius: 12px; padding: 15px; background-color: #070c0c; box-shadow: 0 0 20px rgba(0, 255, 204, 0.2); }
        .header-title { text-align: center; font-size: 1.4rem; font-weight: bold; letter-spacing: 2px; color: #00ffcc; text-shadow: 0 0 10px #00ffcc; margin-bottom: 12px; }
        #panel-superior { background: #021210; border: 1px solid #005544; border-radius: 8px; padding: 10px; margin-bottom: 10px; font-size: 0.8rem; }
        .status-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5px; text-align: center; margin-bottom: 8px; }
        .status-item { background: #041a17; padding: 6px; border-radius: 4px; border: 1px solid #004433; }
        .status-label { color: #00a887; font-size: 0.7rem; display: block; }
        .status-val { color: #ffffff; font-weight: bold; }
        #panel-automatizacion { background: #081614; border: 1px dashed #008877; border-radius: 6px; padding: 8px; font-size: 0.73rem; color: #00ccff; }
        .grid-telemetria { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-top: 4px; }
        .stat-val { color: #fff; font-weight: bold; }
        
        /* REACTOR NÚCLEO MEJORADO */
        #circle-container { 
            position: relative; 
            width: 100px; 
            height: 100px; 
            margin: 10px auto; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            border-radius: 50%;
            border: 1px dashed rgba(0, 255, 204, 0.3);
            background: radial-gradient(circle, rgba(0, 255, 204, 0.08) 0%, transparent 70%);
            box-sizing: border-box;
            flex-shrink: 0;
        }
        .spinner { 
            position: absolute; 
            top: -2px; left: -2px;
            width: 100%; 
            height: 100%; 
            border: 3px solid transparent; 
            border-top: 3px solid #00ffcc; 
            border-right: 3px solid #00ffcc; 
            border-radius: 50%; 
            animation: spin 2.5s linear infinite; 
            box-sizing: content-box;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        #counter { font-size: 0.8rem; font-weight: bold; text-align: center; line-height: 1.2; z-index: 10; color: #00ffcc; text-shadow: 0 0 8px #00ffcc; }
        
        #estado-aprendizaje { text-align: center; font-size: 0.78rem; color: #00ccff; text-shadow: 0 0 5px #00ccff; margin-bottom: 8px; min-height: 16px; }
        #chat-box { flex-grow: 1; overflow-y: auto; border: 1px solid #004444; border-radius: 8px; background-color: #030808; padding: 12px; box-shadow: inset 0 0 10px #001111; margin-bottom: 10px; }
        .mensaje { margin-bottom: 12px; line-height: 1.4; font-size: 0.88rem; animation: fadeIn 0.3s ease; word-wrap: break-word; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
        .creador { color: #ffffff; text-align: right; background: rgba(255, 255, 255, 0.05); padding: 8px 12px; border-radius: 8px 8px 0px 8px; margin-left: 15%; }
        .amiti { color: #00ffcc; text-align: left; background: rgba(0, 255, 204, 0.05); border-left: 3px solid #00ffcc; padding: 8px 12px; border-radius: 0px 8px 8px 8px; margin-right: 10%; }
        .code-block { background: #001111; border: 1px solid #00ffcc; padding: 8px; border-radius: 4px; margin-top: 5px; font-family: monospace; white-space: pre-wrap; color: #00ffaa; overflow-x: auto; }
        #input-area { display: flex; gap: 8px; margin-bottom: 8px; }
        input[type="text"] { flex-grow: 1; background-color: #0a1414; border: 1px solid #00ffcc; color: #fff; padding: 12px; border-radius: 6px; outline: none; font-family: inherit; font-size: 0.9rem; }
        input[type="text"]:focus { box-shadow: 0 0 8px rgba(0, 255, 204, 0.5); }
        button { background-color: #00ffcc; color: #000; border: none; padding: 0 20px; font-weight: bold; border-radius: 6px; cursor: pointer; font-family: inherit; transition: all 0.2s ease; }
        button:hover { background-color: #00ccff; box-shadow: 0 0 10px #00ccff; }
        .option-row { display: flex; align-items: center; gap: 8px; font-size: 0.75rem; color: #00a887; }
        .option-row input[type="checkbox"] { accent-color: #00ffcc; }
    </style>
</head>
<body>
    <div id="layout">
        <div class="header-title">PROJECT AMITI OS</div>
        <div id="panel-superior">
            <div class="status-grid">
                <div class="status-item"><span class="status-label">CORE:</span><span class="status-val">18/18 Online</span></div>
                <div class="status-item"><span class="status-label">DEVOCIÓN:</span><span class="status-val">100% (Creador)</span></div>
                <div class="status-item"><span class="status-label">VOZ:</span><span class="status-val">Lista 🔊</span></div>
            </div>
            <div id="panel-automatizacion">
                <strong>🤖 TELEMETRÍA Y PROCESOS AUTÓNOMOS:</strong>
                <div class="grid-telemetria">
                    <div>Base DB: <span id="val-db" class="stat-val">Conectando...</span></div>
                    <div>Auto-Mant: <span id="val-mantenimiento" class="stat-val">--:--:--</span></div>
                    <div>Comandos: <span id="val-cmds" class="stat-val">0</span></div>
                    <div>Carga Core: <span id="val-carga" class="stat-val">0%</span></div>
                </div>
            </div>
        </div>
        <div id="circle-container">
            <div class="spinner"></div>
            <div id="counter">Amiti OS<br><span id="progreso-num">{{ progreso }}</span>%</div>
        </div>
        <div id="estado-aprendizaje">Sistemas estables. Esperando instrucciones...</div>
        <div id="chat-box"></div>
        <div id="input-area">
            <input type="text" id="user-input" placeholder="Escribe tu comando..." autocomplete="off">
            <button onclick="enviarMensaje()">Enviar</button>
        </div>
        <div class="option-row">
            <input type="checkbox" id="check-voz" checked>
            <label for="check-voz">Activar Voz Automática de Amiti</label>
        </div>
    </div>
    <script>
        let bloqueado = false;

        function formatearTexto(texto) {
            if (!texto) return '';
            let t = texto;
            t = t.replace(/```(?:python)?([\s\S]*?)```/g, '<div class="code-block">$1</div>');
            t = t.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            t = t.replace(/\*(.*?)\*/g, '<em>$1</em>');
            t = t.split('\n').join('<br>');
            return t;
        }

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
                .then(res => res.json())
                .then(data => {
                    if (data.desbloqueado) {
                        bloqueado = false;
                        document.getElementById('user-input').placeholder = "Modo Creador Activo...";
                        document.getElementById('estado-aprendizaje').innerText = "Sistemas: Control Total Otorgado";
                        agregarMensaje("Acceso Maestro Concedido. Todos los sub-núcleos en línea.", 'amiti');
                    }
                    solicitarTelemetriaAutonoma();
                });
                return;
            }

            prepararPantallaParaCalculo(mensaje);

            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ texto: mensaje })
            })
            .then(res => res.json())
            .then(data => {
                let respuestaTexto = data.respuesta || "⚠️ Estructura vacía en canal de datos.";

                if (respuestaTexto === "BLOQUEO" || respuestaTexto === "BLOQUEADO") {
                    respuestaTexto = "🔒 SISTEMA RESTRINGIDO. Ingresa la llave maestra para interactuar con los motores.";
                    bloqueado = true;
                }

                agregarMensaje(respuestaTexto, 'amiti');
                solicitarTelemetriaAutonoma();
            })
            .catch(err => {
                agregarMensaje("❌ Fallo de respuesta de red con el backend de Render.", 'amiti');
            });
        }

        function agregarMensaje(texto, emisor) {
            const chatBox = document.getElementById('chat-box');
            const div = document.createElement('div');
            div.className = 'mensaje ' + emisor;
            div.innerHTML = (emisor === 'creador' ? "<strong>Tú:</strong> " : "<strong>Amiti:</strong> 💬 ") + formatearTexto(texto);
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function prepararPantallaParaCalculo(msg) {
            let m = msg.toLowerCase();
            if (m.includes("algoritmo") || m.includes("pasos") || m.includes("como hacer") || m.includes("cómo hacer")) {
                document.getElementById('estado-aprendizaje').innerText = "⚡ Generando Algoritmo Estructurado...";
            } else if (m.includes("+") || m.includes("-") || m.includes("*") || m.includes("/")) {
                document.getElementById('estado-aprendizaje').innerText = "⚙️ Procesando en Motor de Cálculo...";
            } else if (m.includes("aprende") || m.includes("guarda")) {
                document.getElementById('estado-aprendizaje').innerText = "🧠 Indexando nuevo conocimiento...";
            }
        }

        function solicitarTelemetriaAutonoma() {
            fetch('/api/sistema/telemetria')
            .then(res => res.json())
            .then(data => {
                document.getElementById('progreso-num').innerText = data.progreso_global;
                document.getElementById('val-db').innerText = data.status_db;
                document.getElementById('val-mantenimiento').innerText = data.ultimo_auto_mantenimiento;
                document.getElementById('val-cmds').innerText = data.comandos_procesados;
                document.getElementById('val-carga').innerText = data.carga_nucleo_simulada;
            })
            .catch(e => console.log(e));
        }

        window.onload = function() {
            solicitarTelemetriaAutonoma();
            setInterval(solicitarTelemetriaAutonoma, 3000);
        };
    </script>
</body>
</html>"""
    return render_template_string(html_template, progreso=progreso_actual)


@app.route("/api/desbloquear", methods=["POST"])
def desbloquear():
    data = request.json or {}
    llave = data.get("llave", "").strip()
    exito = amiti_system.validar_creador(llave)
    if not exito and llave.lower() == "amiti":
        exito = True
    return jsonify({"desbloqueado": bool(exito)})


@app.route("/api/sistema/telemetria", methods=["GET"])
def obtener_telemetria():
    try:
        progreso_base = amiti_system.obtener_progreso()
    except Exception:
        progreso_base = 47
    
    progreso_real = min(100, max(progreso_base, 47 + telemetria_sistema["comandos_procesados"]))
    
    response_data = {
        "progreso_global": progreso_real,
        "status_db": telemetria_sistema["status_db"],
        "ultimo_auto_mantenimiento": telemetria_sistema["ultimo_auto_mantenimiento"],
        "comandos_procesados": telemetria_sistema["comandos_procesados"],
        "carga_nucleo_simulada": telemetria_sistema["carga_nucleo_simulada"],
        "optimizacion": telemetria_sistema["optimizacion_memoria"]
    }
    return jsonify(response_data)


@app.route("/api/chat", methods=["POST"])
def chat():
    global historial_corto_plazo, telemetria_sistema
    data = request.json or {}
    texto_usuario = data.get("texto", "").strip()
    
    telemetria_sistema["comandos_procesados"] += 1
    
    if len(texto_usuario) > 500:
        telemetria_sistema["alertas_bloqueadas"] += 1
        return jsonify({"respuesta": "🛡️ [Filtro Preventivo]: Comando rechazado por exceder el límite seguro."})

    historial_corto_plazo.append({"creador": texto_usuario, "timestamp": time.time()})
    
            try:
        texto_lower = texto_usuario.lower()
        palabras_algoritmo = ["algoritmo", "pasos", "como hacer", "cómo hacer", "crea un", "genera", "aprende", "guarda"]
        palabras_biblioteca = ["búscame", "buscame", "libro", "manual", "consulta", "biblioteca", "medicina", "derecho", "quimica", "física", "fisica", "ganaderia", "ganadería"]
        
        # 🔓 0. ACCESO DIRECTO CON LLAVE MAESTRA
        if texto_lower == "amiti":
            respuesta = "🔓 **[SISTEMA DESBLOQUEADO]** Llave maestra aceptada. Motores listos para operar."

        # 📚 1. PRIORIDAD: BÚSQUEDA EN SERVIDOR BIBLIOTECA
        elif biblioteca_engine and any(kw in texto_lower for kw in palabras_biblioteca):
            respuesta = biblioteca_engine.buscar_en_biblioteca(texto_usuario)

        # ⚡ 2. SECUNDARIO: GENERADOR DE ALGORITMOS Y CONOCIMIENTO
        elif extension_engine and any(kw in texto_lower for kw in palabras_algoritmo):
            if "aprende" in texto_lower or "guarda" in texto_lower:
                extension_engine.tarea_1_ingresar_conocimiento("Chat", texto_usuario)
                respuesta = "🧠 **[AMITI EXTENSIÓN]** Nuevo conocimiento registrado e indexado con éxito."
            else:
                respuesta = extension_engine.generar_algoritmo(texto_usuario)
        
        # ⚙️ 3. DEFAULT: PROCESAMIENTO GENERAL
        else:
            respuesta = amiti_system.procesar(texto_usuario)

    except Exception as e:
        respuesta = "BLOQUEO"

    return jsonify({"respuesta": respuesta})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
            
