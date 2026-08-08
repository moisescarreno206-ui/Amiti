import os
import sys
import time
import traceback
import threading
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

# ⚙️ PARCHE DE RUTAS AUTOMÁTICO
ruta_proyecto = os.path.dirname(os.path.abspath(__file__))
if ruta_proyecto not in sys.path:
    sys.path.insert(0, ruta_proyecto)

# 📊 VARIABLES DE ESTADO GLOBAL Y AUTOMATIZACIÓN
sistema_activo = False
error_de_importacion = None
traceback_error = ""
historial_corto_plazo = []  # Buffer de memoria automatizada de la sesión

# Diccionario de telemetría automática simulada y real
telemetria_sistema = {
    "status_db": "Desconectado",
    "ultimo_auto_mantenimiento": "Nunca",
    "comandos_procesados": 0,
    "carga_nucleo_simulada": "0%",
    "alertas_bloqueadas": 0,
    "optimizacion_memoria": "Estable",
    "status_dron": "Esperando enlace..." # <-- INYECCIÓN: Estado inicial del Dron
}

# 🧠 INTENTO DE IMPORTACIÓN PROTEGIDA Y RADIOGRAFÍA DEL NÚCLEO
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
        def obtener_progreso(self): return 0
        def validar_creador(self, llave): return False
        def procesar(self, cmd): return "SISTEMA FUERA DE LÍNEA: Ejecutando modo de contingencia."
    amiti_system = FallbackAmitiOS()

# 🔌 INTEGRACIÓN DE LA EXTENSIÓN AUTÓNOMA (Sin modificar el código base)
try:
    from nucleos.amiti_extension import AmitiExtensionEngine
    extension_engine = AmitiExtensionEngine()
    print("✔️ [EXTENSIÓN] Motor de extensiones autónomas vinculado.")
except Exception as e_ext:
    extension_engine = None
    print(f"⚠️ [EXTENSIÓN] Cargada en modo pasivo: {e_ext}")


# 🔄 HILO DE AUTOMATIZACIÓN EN SEGUNDO PLANO (Background Daemon)
def bucle_automatizacion_amiti():
    """ Hilo perpetuo que simula tareas crónicas de optimización y salud del sistema """
    global telemetria_sistema
    print("⚙️ [NÚCLEO AUTOMÁTICO]: Hilo de mantenimiento autónomo inicializado.")
    while True:
        try:
            ahora = datetime.now().strftime("%H:%M:%S")
            telemetria_sistema["ultimo_auto_mantenimiento"] = ahora
            
            # Automatización 1: Balancear cargas e indexar buffers
            tamano_memoria = len(historial_corto_plazo)
            if tamano_memoria > 10:
                historial_corto_plazo.pop(0) # Auto-limpieza de caché para ahorrar recursos en teléfonos/Render
                telemetria_sistema["optimizacion_memoria"] = f"Liberada caché a las {ahora}"
            else:
                telemetria_sistema["optimizacion_memoria"] = "Óptima (Estructura Limpia)"
                
            # Automatización 2: Simulación dinámica de procesamiento de núcleos
            progreso_actual = 47
            try: progreso_actual = amiti_system.obtener_progreso()
            except: pass
            
            if progreso_actual >= 100:
                telemetria_sistema["carga_nucleo_simulada"] = "100% Autónomo"
            else:
                telemetria_sistema["carga_nucleo_simulada"] = f"Escaneando Nodos ({progreso_actual}%)"
            
            # --- INYECCIÓN: ACTUALIZACIÓN TELEMETRÍA DRON ---
            try:
                if hasattr(amiti_system, 'dron'):
                    estado_vuelo = "🚁 EN VUELO" if amiti_system.dron.en_vuelo else "🛬 TIERRA"
                    conexion = "Señal Activa" if amiti_system.dron.conectado else "Buscando IP..."
                    telemetria_sistema["status_dron"] = f"{conexion} | {estado_vuelo}"
                else:
                    telemetria_sistema["status_dron"] = "Módulo no inicializado"
            except:
                pass
            # ------------------------------------------------
                
            time.sleep(15)  # Se ejecuta automáticamente cada 15 segundos
        except Exception as e_thread:
            print(f"⚠️ Error en el hilo automático: {e_thread}")
            time.sleep(5)

# Lanzar el proceso automatizado de fondo sin retrasar el arranque de Flask
hilo_mantenimiento = threading.Thread(target=bucle_automatizacion_amiti, daemon=True)
hilo_mantenimiento.start()


app = Flask(__name__)
def mostrar_pantalla_diagnostico():
    html_error = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><title>Amiti OS - Error</title></head>
    <body style="background:#120202; color:#ff4444; font-family:monospace; padding:20px;">
        <h1>⚠️ FALLO DE COMPILACIÓN EN NÚCLEO</h1>
        <pre>{traceback_error}</pre>
    </body>
    </html>
    """
    return render_template_string(html_error)


@app.route("/")
def index():
    if not sistema_activo:
        return mostrar_pantalla_diagnostico()
    
    try: progreso_actual = amiti_system.obtener_progreso()
    except: progreso_actual = 47

    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Amiti OS - Consola Suprema</title>
        <style>
            body { background-color: #050505; color: #00ffcc; font-family: 'Courier New', Courier, monospace; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 10px; box-sizing: border-box; }
            #layout { display: flex; flex-direction: column; width: 100%; max-width: 500px; height: 95vh; }
            
            /* Panel de automatización superior */
            #panel-automatizacion { background: #0b1311; border: 1px dashed #00ffcc; border-radius: 5px; padding: 8px 12px; margin-top: 10px; font-size: 0.75rem; color: #00ccff; }
            .grid-telemetria { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-top: 5px; }
            .stat-val { color: #ffffff; font-weight: bold; }
            
            #circle-container { position: relative; width: 110px; height: 110px; margin: 15px auto 5px auto; display: flex; justify-content: center; align-items: center; }
            .spinner { position: absolute; width: 100%; height: 100%; border: 3px solid transparent; border-top: 3px solid #00ffcc; border-radius: 50%; animation: spin 2s linear infinite; }
            @keyframes spin { 100% { transform: rotate(360deg); } }
            #counter { font-size: 0.9rem; font-weight: bold; text-align: center; line-height: 1.2; z-index: 10; }
            
            #estado-aprendizaje { text-align: center; font-size: 0.8rem; color: #00ccff; text-shadow: 0 0 5px #00ccff; margin-bottom: 10px; height: 15px; }
            
            /* Ventana de chat extendida */
            #chat-box { flex-grow: 1; overflow-y: auto; border: 1px solid #004444; border-radius: 5px; background-color: #080808; padding: 12px; box-shadow: inset 0 0 10px #002222; }
            .mensaje { margin-bottom: 12px; line-height: 1.4; font-size: 0.9rem; animation: fadeIn 0.3s ease; }
            @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
            .creador { color: #ffffff; text-align: right; }
            .amiti { color: #00ffcc; text-align: left; border-left: 2px solid #00ffcc; padding-left: 8px; }
            
            #input-area { display: flex; margin-top: 10px; margin-bottom: 5px; }
            input[type="text"] { flex-grow: 1; background-color: #111; border: 1px solid #00ffcc; color: #fff; padding: 12px; border-radius: 5px 0 0 5px; outline: none; font-family: inherit; }
            button { background-color: #00ffcc; color: #000; border: none; padding: 0 20px; font-weight: bold; border-radius: 0 5px 5px 0; cursor: pointer; font-family: inherit; }
            button:hover { background-color: #00ccff; }
            
            .code-block { background: #021a14; padding: 6px; border-left: 3px solid #00ffcc; font-size: 0.8rem; overflow-x: auto; font-family: monospace; color: #a6fff2; margin: 5px 0; }
        </style>
    </head>
    <body>
        <div id="layout">
            <!-- PANEL DE TELEMETRÍA AUTOMÁTICA -->
            <div id="panel-automatizacion">
                <strong>🤖 TELEMETRÍA Y PROCESOS AUTÓNOMOS:</strong>
                <div class="grid-telemetria">
                    <div>Base de Datos: <span id="val-db" class="stat-val">Conectando...</span></div>
                    <div>Auto-Mantenimiento: <span id="val-mantenimiento" class="stat-val">--:--:--</span></div>
                    <div>Comandos Auditados: <span id="val-cmds" class="stat-val">0</span></div>
                    <div>Carga del Núcleo: <span id="val-carga" class="stat-val">0%</span></div>
                    <!-- INYECCIÓN: GUI del Dron -->
                    <div style="grid-column: span 2; border-top: 1px dashed #004444; padding-top: 5px; margin-top: 2px;">
                        Estado Dron S15: <span id="val-dron" class="stat-val" style="color: #ff99ff;">--</span>
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
                            agregarMensaje("Acceso Maestro Concedido. Todos los sub-núcleos (Cálculo, Aprendizaje, Finanzas) desbloqueados de forma síncrona.", 'amiti');
                        }
                        solicitarTelemetriaAutonoma();
                    });
                    return;
                }

                // Si el usuario escribe una operación matemática o contable, el estado avanza visualmente
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
                    // Formatear bloques de código automáticamente si el núcleo devuelve un script contable
                    if (respuestaTexto.includes("```python")) {
                        respuestaTexto = respuestaTexto.replace(/```python([\s\S]*?)```/g, '<div class="code-block">$1</div>');
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
                
                // Conversión segura de saltos de línea a etiquetas HTML
                let textoProcesado = texto.replace(/\\n/g, "<br>").replace(/\n/g, "<br>");
                div.innerHTML = (emisor === 'creador' ? "<strong>Tú:</strong> " : "<strong>Amiti:</strong> ") + textoProcesado;
                
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function prepararPantallaParaCalculo(msg) {
                let m = msg.toLowerCase();
                // INYECCIÓN: Estado visual del dron en el Frontend
                if (m.includes("eleva el dron") || m.includes("aterriza") || m.includes("dron")) {
                    document.getElementById('estado-aprendizaje').innerText = "📡 Transmitiendo protocolo de vuelo a Dron S15 Max...";
                } else if (m.includes("+") || m.includes("-") || m.includes("*") || m.includes("/") || m.includes("raiz") || m.includes("raíz")) {
                    document.getElementById('estado-aprendizaje').innerText = "⚙️ Procesando en Motor de Cálculo Matemático...";
                } else if (m.includes("contable") || m.includes("monetaria")) {
                    document.getElementById('estado-aprendizaje').innerText = "📊 Compilando algoritmo financiero en Neo DB...";
                } else if (m.includes("aprende") || m.includes("neo")) {
                    document.getElementById('estado-aprendizaje').innerText = "🧠 Indexando nuevo conocimiento en clúster...";
                }
            }

            // Petición automática para refrescar los datos del hilo de mantenimiento
            function solicitarTelemetriaAutonoma() {
                fetch('/api/sistema/telemetria')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('progreso-num').innerText = data.progreso_global;
                    document.getElementById('val-db').innerText = data.status_db;
                    document.getElementById('val-mantenimiento').innerText = data.ultimo_auto_mantenimiento;
                    document.getElementById('val-cmds').innerText = data.comandos_procesados;
                    document.getElementById('val-carga').innerText = data.carga_nucleo_simulada;
                    // INYECCIÓN: Refresco de texto UI Dron
                    if(document.getElementById('val-dron') && data.status_dron) {
                        document.getElementById('val-dron').innerText = data.status_dron;
                    }
                    
                    if (!bloqueado) {
                        document.getElementById('estado-aprendizaje').innerText = "Sistemas: Autónomo con persistencia Neon DB";
                    }
                });
            }

            // Bucle autónomo de actualización visual cada 4 segundos
            window.onload = function() {
                solicitarTelemetriaAutonoma();
                setInterval(solicitarTelemetriaAutonoma, 4000);
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
        exito = True
    return jsonify({"desbloqueado": bool(exito)})


# 📡 RUTA DE CONTROL DE TELEMETRÍA AUTOMÁTICA
@app.route("/api/sistema/telemetria", methods=["GET"])
def obtener_telemetria():
    try: progreso = amiti_system.obtener_progreso()
    except: progreso = 47
    
    response_data = {
        "progreso_global": progreso,
        "status_db": telemetria_sistema["status_db"],
        "ultimo_auto_mantenimiento": telemetria_sistema["ultimo_auto_mantenimiento"],
        "comandos_procesados": telemetria_sistema["comandos_procesados"],
        "carga_nucleo_simulada": telemetria_sistema["carga_nucleo_simulada"],
        "optimizacion": telemetria_sistema["optimizacion_memoria"],
        # INYECCIÓN: Exposición del estado del dron vía API JSON
        "status_dron": telemetria_sistema.get("status_dron", "Inactivo")
    }
    return jsonify(response_data)


@app.route("/api/chat", methods=["POST"])
def chat():
    global historial_corto_plazo, telemetria_sistema
    data = request.json or {}
    texto_usuario = data.get("texto", "").strip()
    
    # Automatización 3: Registro automático en contadores de auditoría
    telemetria_sistema["comandos_procesados"] += 1
    
    # Automatización 4: Pre-procesador de Seguridad antes de llamar al Core
    if len(texto_usuario) > 300:
        telemetria_sistema["alertas_bloqueadas"] += 1
        return jsonify({"respuesta": "🛡️ [Filtro Preventivo app.py]: Comando rechazado por exceder los límites de bytes seguros."})

    # Guardar en la memoria automática de sesión
    historial_corto_plazo.append({"creador": texto_usuario, "timestamp": time.time()})
    
    print(f"--- [INPUT AUTOMÁTICO] Procesando comando #{telemetria_sistema['comandos_procesados']}: '{texto_usuario}' ---")
    
    try:
        texto_lower = texto_usuario.lower()
        
        # 1. Evaluación por el Motor Autónomo (Extensión)
        if extension_engine and any(kw in texto_lower for kw in ["crea un algoritmo", "genera codigo", "crea un modulo", "aprende", "guarda"]):
            if "aprende" in texto_lower or "guarda" in texto_lower:
                res = extension_engine.tarea_1_ingresar_conocimiento("Chat", texto_usuario)
                respuesta = "🧠 **[Extensión]** Conocimiento registrado en la base de datos autónoma."
            else:
                nombre_mod = f"mod_{abs(hash(texto_usuario)) % 1000}"
                res = extension_engine.ejecutar_pipeline_completo(
                    titulo="Solicitud Web",
                    contenido=texto_usuario,
                    categoria="desarrollo",
                    prompt=texto_usuario,
                    nombre_modulo=nombre_mod
                )
                respuesta = f"⚙️ **[Extensión]** Módulo `{nombre_mod}` generado e integrado al repositorio."

        # 2. Evaluación por el Sistema Base Original
        else:
            respuesta = amiti_system.procesar(texto_usuario)

    except Exception as e:
        print(f"❌ Fallo crítico en ejecución diferida de amiti_os: {str(e)}")
        respuesta = "BLOQUEO"

    print(f"--- [OUTPUT AUTOMÁTICO] Retorno enviado al cliente: '{respuesta}' ---")
    return jsonify({"respuesta": respuesta})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
