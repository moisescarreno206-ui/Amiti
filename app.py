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
historial_corto_plazo = []  # Buffer de memoria automatizada de la sesión

# Diccionario de telemetría automática
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

    print("\n=======================================================")
    print("🔍 [AUTOMATIZACIÓN] Cargando mapas lógicos de amiti_os.py...")
    try:
        import inspect
        ruta_fuente = inspect.getfile(amiti_system.__class__)
        with open(ruta_fuente, "r", encoding="utf-8") as f:
            print(f"✔️ Núcleo leído con éxito desde: {ruta_fuente}")
    except Exception as e_ins:
        print(f"❌ Alerta de lectura de diagnóstico: {e_ins}")
    print("=======================================================\n")

except Exception as e:
    error_de_importacion = e
    traceback_error = traceback.format_exc()
    telemetria_sistema["status_db"] = "ERROR CRÍTICO"
    
    class FallbackAmitiOS:
        def obtener_progreso(self):
            return 0
            
        def validar_creador(self, llave):
            return False
            
        def procesar(self, cmd):
            return "SISTEMA FUERA DE LÍNEA: Ejecutando modo de contingencia pasivo."
            
    amiti_system = FallbackAmitiOS()

# 🔌 INTEGRACIÓN DEL MOTOR DE EXTENSIÓN AUTÓNOMA DE ALGORITMOS
try:
    try:
        from nucleos.amiti_extension import AmitiExtensionEngine
    except ModuleNotFoundError:
        from núcleos.amiti_extension import AmitiExtensionEngine
        
    extension_engine = AmitiExtensionEngine()
    print("✔️ [EXTENSIÓN] Motor de extensiones y algoritmos dinámicos vinculado.")
except Exception as e_ext:
    extension_engine = None
    print(f"⚠️ [EXTENSIÓN] Cargada en modo pasivo por advertencia: {e_ext}")


# 🔄 HILO DE AUTOMATIZACIÓN EN SEGUNDO PLANO (DAEMON DE MANTENIMIENTO)
def bucle_automatizacion_amiti():
    """ Hilo perpetuo que gestiona tareas crónicas de optimización y salud del sistema """
    global telemetria_sistema
    print("⚙️ [NÚCLEO AUTOMÁTICO]: Hilo de mantenimiento autónomo inicializado.")
    while True:
        try:
            ahora = datetime.now().strftime("%H:%M:%S")
            telemetria_sistema["ultimo_auto_mantenimiento"] = ahora
            
            # Auto-limpieza de caché para ahorrar recursos en la nube
            tamano_memoria = len(historial_corto_plazo)
            if tamano_memoria > 10:
                historial_corto_plazo.pop(0)
                telemetria_sistema["optimizacion_memoria"] = f"Liberada caché a las {ahora}"
            else:
                telemetria_sistema["optimizacion_memoria"] = "Óptima (Estructura Limpia)"
                
            # Escaneo dinámico de progreso
            progreso_actual = 47
            try:
                progreso_actual = amiti_system.obtener_progreso()
            except Exception:
                pass
            
            if progreso_actual >= 100:
                telemetria_sistema["carga_nucleo_simulada"] = "100% Autónomo"
            else:
                telemetria_sistema["carga_nucleo_simulada"] = f"Escaneando Nodos ({progreso_actual}%)"
                
            time.sleep(15)
        except Exception as e_thread:
            print(f"⚠️ Error en el hilo automático: {e_thread}")
            time.sleep(5)

# Lanzar el proceso automatizado de fondo
hilo_mantenimiento = threading.Thread(target=bucle_automatizacion_amiti, daemon=True)
hilo_mantenimiento.start()


app = Flask(__name__)

def mostrar_pantalla_diagnostico():
    html_error = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Amiti OS - Error de Compilación</title>
        <style>
            body {{
                background-color: #120202;
                color: #ff4444;
                font-family: 'Courier New', Courier, monospace;
                padding: 20px;
                margin: 0;
            }}
            h1 {{
                border-bottom: 2px solid #ff4444;
                padding-bottom: 10px;
            }}
            pre {{
                background: #220505;
                padding: 15px;
                border-radius: 5px;
                border: 1px solid #ff4444;
                overflow-x: auto;
                white-space: pre-wrap;
            }}
            .info {{
                color: #ffaaaa;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <h1>⚠️ FALLO CRÍTICO EN NÚCLEO DE AMITI OS</h1>
        <p class="info">Se ha detectado una excepción durante la fase de importación inicial de los sub-sistemas:</p>
        <pre>{traceback_error}</pre>
        <p class="info">Por favor, revisa que la carpeta 'nucleos/' contenga los archivos 'amiti_os.py' y 'amiti_extension.py'.</p>
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
    except Exception:
        progreso_actual = 47

    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PROJECT AMITI OS</title>
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            body {
                background-color: #050505;
                color: #00ffcc;
                font-family: 'Courier New', Courier, monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                min-height: 100vh;
                padding: 10px;
            }
            #layout {
                display: flex;
                flex-direction: column;
                width: 100%;
                max-width: 500px;
                height: 95vh;
                border: 2px solid #00ffcc;
                border-radius: 12px;
                padding: 15px;
                background-color: #070c0c;
                box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
            }
            
            .header-title {
                text-align: center;
                font-size: 1.4rem;
                font-weight: bold;
                letter-spacing: 2px;
                color: #00ffcc;
                text-shadow: 0 0 10px #00ffcc;
                margin-bottom: 12px;
            }

            #panel-superior {
                background: #021210;
                border: 1px solid #005544;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 10px;
                font-size: 0.8rem;
            }

            .status-grid {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 5px;
                text-align: center;
                margin-bottom: 8px;
            }

            .status-item {
                background: #041a17;
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #004433;
            }

            .status-label {
                color: #00a887;
                font-size: 0.7rem;
                display: block;
            }

            .status-val {
                color: #ffffff;
                font-weight: bold;
            }

            #panel-automatizacion {
                background: #081614;
                border: 1px dashed #008877;
                border-radius: 6px;
                padding: 8px;
                font-size: 0.73rem;
                color: #00ccff;
            }

            .grid-telemetria {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 4px;
                margin-top: 4px;
            }

            #circle-container {
                position: relative;
                width: 90px;
                height: 90px;
                margin: 8px auto;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .spinner {
                position: absolute;
                width: 100%;
                height: 100%;
                border: 3px solid transparent;
                border-top: 3px solid #00ffcc;
                border-right: 3px solid #00ffcc;
                border-radius: 50%;
                animation: spin 2s linear infinite;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            #counter {
                font-size: 0.85rem;
                font-weight: bold;
                text-align: center;
                line-height: 1.1;
                z-index: 10;
            }

            #estado-aprendizaje {
                text-align: center;
                font-size: 0.78rem;
                color: #00ccff;
                text-shadow: 0 0 5px #00ccff;
                margin-bottom: 8px;
                min-height: 16px;
            }

            #chat-box {
                flex-grow: 1;
                overflow-y: auto;
                border: 1px solid #004444;
                border-radius: 8px;
                background-color: #030808;
                padding: 12px;
                box-shadow: inset 0 0 10px #001111;
                margin-bottom: 10px;
            }

            .mensaje {
                margin-bottom: 12px;
                line-height: 1.4;
                font-size: 0.88rem;
                animation: fadeIn 0.3s ease;
                word-wrap: break-word;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(5px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .creador {
                color: #ffffff;
                text-align: right;
                background: rgba(255, 255, 255, 0.05);
                padding: 8px 12px;
                border-radius: 8px 8px 0px 8px;
                margin-left: 15%;
            }

            .amiti {
                color: #00ffcc;
                text-align: left;
                background: rgba(0, 255, 204, 0.05);
                border-left: 3px solid #00ffcc;
                padding: 8px 12px;
                border-radius: 0px 8px 8px 8px;
                margin-right: 10%;
            }

            .code-block {
                background: #021a14;
                padding: 8px;
                border-left: 3px solid #00ffcc;
                font-size: 0.8rem;
                overflow-x: auto;
                font-family: monospace;
                color: #a6fff2;
                margin: 6px 0;
                border-radius: 4px;
                white-space: pre-wrap;
            }

            #input-area {
                display: flex;
                gap: 8px;
                margin-bottom: 8px;
            }

            input[type="text"] {
                flex-grow: 1;
                background-color: #0a1414;
                border: 1px solid #00ffcc;
                color: #fff;
                padding: 12px;
                border-radius: 6px;
                outline: none;
                font-family: inherit;
                font-size: 0.9rem;
            }

            input[type="text"]:focus {
                box-shadow: 0 0 8px rgba(0, 255, 204, 0.5);
            }

            button {
                background-color: #00ffcc;
                color: #000;
                border: none;
                padding: 0 20px;
                font-weight: bold;
                border-radius: 6px;
                cursor: pointer;
                font-family: inherit;
                transition: all 0.2s ease;
            }

            button:hover {
                background-color: #00ccff;
                box-shadow: 0 0 10px #00ccff;
            }

            .option-row {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.75rem;
                color: #00a887;
            }

            .option-row input[type="checkbox"] {
                accent-color: #00ffcc;
            }
        </style>
    </head>
    <body>
        <div id="layout">
            <div class="header-title">PROJECT AMITI OS</div>

            <div id="panel-superior">
                <div class="status-grid">
                    <div class="status-item">
                        <span class="status-label">CORE:</span>
                        <span class="status-val">18/18 Online</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">DEVOCIÓN:</span>
                        <span class="status-val">100% (Creador)</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">VOZ:</span>
                        <span class="status-val">Lista 🔊</span>
                    </div>
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
                <input type="text" id="user-input" placeholder="Escribe tu comando o llave maestra..." autocomplete="off">
                <button onclick="enviarMensaje()">Enviar</button>
            </div>

            <div class="option-row">
                <input type="checkbox" id="check-voz" checked>
                <label for="check-voz">Activar Voz Automática de Amiti</label>
            </div>
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
                    .then(res => res.json())
                    .then(data => {
                        if (data.desbloqueado) {
                            bloqueado = false;
                            document.getElementById('user-input').placeholder = "Modo Creador Activo...";
                            document.getElementById('estado-aprendizaje').innerText = "Sistemas: Control Total Otorgado";
                            agregarMensaje("Acceso Maestro Concedido. Todos los sub-núcleos (Cálculo, Aprendizaje, Algoritmos) desbloqueados de forma síncrona.", 'amiti');
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

                    if (respuestaTexto.includes("```")) {
                        respuestaTexto = respuestaTexto.replace(/```python([\s\S]*?)```/g, '<div class="code-block">$1</div>');
                        respuestaTexto = respuestaTexto.replace(/```([\s\S]*?)```/g, '<div class="code-block">$1</div>');
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
                
                let textoProcesado = texto.replace(/\\n/g, "<br>").replace(/\n/g, "<br>");
                div.innerHTML = (emisor === 'creador' ? "<strong>Tú:</strong> " : "<strong>Amiti:</strong> 💬 ") + textoProcesado;
                
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function prepararPantallaParaCalculo(msg) {
                let m = msg.toLowerCase();
                if (m.includes("algoritmo") || m.includes("pasos") || m.includes("como hacer") || m.includes("cómo hacer")) {
                    document.getElementById('estado-aprendizaje').innerText = "⚡ Generando Algoritmo Estructurado en Motor Autónomo...";
                } else if (m.includes("+") || m.includes("-") || m.includes("*") || m.includes("/")) {
                    document.getElementById('estado-aprendizaje').innerText = "⚙️ Procesando en Motor de Cálculo Matemático...";
                } else if (m.includes("aprende") || m.includes("guarda")) {
                    document.getElementById('estado-aprendizaje').innerText = "🧠 Indexando nuevo conocimiento en Clúster...";
                }
            }

            function solicitarTelemetriaAutonoma() {
                fetch('/api/sistema/telemetria')
                .then(res => res.json())
                .then(
