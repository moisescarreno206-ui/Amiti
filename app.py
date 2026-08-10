import os
import sys
import time
import traceback
import threading
import random
import socket
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

# ⚙️ PARCHE DE RUTAS AUTOMÁTICO DE NÚCLEOS
ruta_proyecto = os.path.dirname(os.path.abspath(__file__))
if ruta_proyecto not in sys.path:
    sys.path.insert(0, ruta_proyecto)

# 🌐 CONFIGURACIÓN DE RED LOCAL DRON (MODO OFFLINE)
DRONE_IP = "192.168.169.1"
DRONE_PORT = 8888

def enviar_comando_udp(hex_code):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes.fromhex(hex_code), (DRONE_IP, DRONE_PORT))
        sock.close()
        return True
    except Exception as e:
        print(f"Error de transmisión UDP: {e}")
        return False

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
    "optimizacion_memoria": "Estable",
    "estado_biblioteca_autonoma": "En espera",
    "estado_dron": "Tierra (0.0m)"
}

# 🧠 IMPORTACIÓN PROTEGIDA DE NÚCLEOS
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

# 🔌 INTEGRACIÓN DEL MOTOR DRON S15 MAX Y COMUNICACIÓN UDP
try:
    from amiti_drone import AmitiDroneEngine
    drone_engine = AmitiDroneEngine()
except Exception:
    class FallbackDrone:
        def __init__(self): 
            self.altura_actual = 0.0
            self.en_vuelo = False
            self.camara_activa = "frontal"
            
        def encender_y_elevar(self, a=1.65): 
            enviar_comando_udp("6601020000")
            self.en_vuelo = True
            self.altura_actual = a
            return f"🚁 **[AMITI DRONE]** Comando UDP enviado. Motores encendidos. Elevando a **{a}m** de altura."
            
        def aterrizar(self):
            enviar_comando_udp("6601030000")
            self.en_vuelo = False
            self.altura_actual = 0.0
            return "🚁 **[AMITI DRONE]** Comando UDP de aterrizaje enviado. Descendiendo a tierra."
            
        def elevar_mas(self, a=1.85): 
            self.altura_actual = a
            return f"🚁 **[AMITI DRONE]** Ascendiendo a **{a}m** de altura."
            
        def mover_adelante(self): 
            return f"🚁 **[AMITI DRONE]** Avanzando hacia **adelante** a {self.altura_actual}m."
            
        def mover_retroceder(self): 
            return f"🚁 **[AMITI DRONE]** Retrocediendo a {self.altura_actual}m."
            
        def mover_lateral(self, d): 
            return f"🚁 **[AMITI DRONE]** Moviendo hacia la **{d.upper()}** a {self.altura_actual}m."
            
        def alternar_camara(self): 
            self.camara_activa = "inferior" if self.camara_activa == "frontal" else "frontal"
            return f"📹 Cámara conmutada a: {self.camara_activa}"
            
    drone_engine = FallbackDrone()

# 🔌 INTEGRACIÓN MOTOR DE EXTENSIÓN Y BIBLIOTECA
try:
    try: from nucleos.amiti_extension import AmitiExtensionEngine
    except ModuleNotFoundError: from núcleos.amiti_extension import AmitiExtensionEngine
    extension_engine = AmitiExtensionEngine()
except Exception: extension_engine = None

try:
    try: from nucleos.amiti_biblioteca import AmitiBibliotecaEngine
    except ModuleNotFoundError: from núcleos.amiti_biblioteca import AmitiBibliotecaEngine
    biblioteca_engine = AmitiBibliotecaEngine()
except Exception: biblioteca_engine = None

# 🔄 HILO DE AUTOMATIZACIÓN EN SEGUNDO PLANO
def bucle_automatizacion_amiti():
    global telemetria_sistema
    while True:
        try:
            ahora = datetime.now().strftime("%H:%M:%S")
            telemetria_sistema["ultimo_auto_mantenimiento"] = ahora
            telemetria_sistema["estado_dron"] = f"En Vuelo ({drone_engine.altura_actual}m)" if drone_engine.en_vuelo else "En Tierra"
        except Exception as e:
            print(f"Error en bucle autónomo: {e}")
        time.sleep(10)

hilo_mantenimiento = threading.Thread(target=bucle_automatizacion_amiti, daemon=True)
hilo_mantenimiento.start()

app = Flask(__name__)

def mostrar_pantalla_diagnostico():
    return render_template_string("""
    <!DOCTYPE html><html><head><title>Amiti OS - Error</title></head>
    <body style="background:#120202; color:#ff4444; font-family:monospace; padding:20px;">
        <h1>⚠️ FALLO CRÍTICO EN NÚCLEO DE AMITI OS</h1><pre>{{ traceback_error }}</pre>
    </body></html>""", traceback_error=traceback_error)

@app.route("/")
def index():
    if not sistema_activo: return mostrar_pantalla_diagnostico()
    
    try: progreso_base = amiti_system.obtener_progreso()
    except Exception: progreso_base = 47
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
        
        #circle-container { 
            position: relative; width: 100px; height: 100px; margin: 10px auto; 
            display: flex; justify-content: center; align-items: center; border-radius: 50%;
            border: 1px dashed rgba(0, 255, 204, 0.3); background: radial-gradient(circle, rgba(0, 255, 204, 0.08) 0%, transparent 70%); flex-shrink: 0;
        }
        .spinner { position: absolute; top: -2px; left: -2px; width: 100%; height: 100%; border: 3px solid transparent; border-top: 3px solid #00ffcc; border-right: 3px solid #00ffcc; border-radius: 50%; animation: spin 2.5s linear infinite; }
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
        
        /* HUD Y CÁMARA DEL DRON */
        .drone-hud { width: 100%; height: 210px; border: 1px solid #00ffcc; border-radius: 8px; background: #001510; position: relative; overflow: hidden; margin-top: 10px; display: flex; align-items: center; justify-content: center; }
        .drone-cam-overlay { position: absolute; top: 10px; left: 10px; font-size: 0.7rem; color: #00ffcc; background: rgba(0,0,0,0.6); padding: 4px 8px; border-radius: 4px; z-index: 5; }
        .crosshair { position: absolute; width: 20px; height: 20px; border: 1px solid rgba(0, 255, 204, 0.6); border-radius: 50%; z-index: 4; }
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
                    <div>Estado Dron: <span id="val-dron" class="stat-val">En Tierra</span></div>
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
            <input type="text" id="user-input" placeholder="Escribe tu comando o control de dron..." autocomplete="off">
            <button onclick="enviarMensaje()">Enviar</button>
        </div>
        <div class="option-row">
            <input type="checkbox" id="check-voz" checked>
            <label for="check-voz">Activar Voz Automática de Amiti</label>
        </div>
    </div>
    <script>
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
                agregarMensaje(respuestaTexto, 'amiti');
                solicitarTelemetriaAutonoma();
            })
            .catch(err => {
                agregarMensaje("❌ Fallo de respuesta de red con el backend.", 'amiti');
            });
        }

        function agregarMensaje(texto, emisor) {
            const chatBox = document.getElementById('chat-box');
            const div = document.createElement('div');
            div.className = 'mensaje ' + emisor;
            
            let contenidoHTML = (emisor === 'creador' ? "<strong>Tú:</strong> " : "<strong>Amiti:</strong> 💬 ") + formatearTexto(texto);
            
            // 🗺️ INTERCEPTOR GPS / MAPA
            if (emisor === 'amiti' && (texto.includes("Sincronizando coordenadas GPS") || texto.includes("Desplegando interfaz de mapas"))) {
                const mapId = 'map-' + Date.now();
                contenidoHTML += `<br><br><div id="${mapId}" style="width: 100%; height: 230px; border: 1px dashed #00ffcc; border-radius: 8px; background-color: #021210; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; color: #00ffcc;">📡 Conectando con satélite...</div>`;
                setTimeout(() => {
                    if(navigator.geolocation) {
                        navigator.geolocation.getCurrentPosition((pos) => {
                            let lat = pos.coords.latitude;
                            let lon = pos.coords.longitude;
                            let iframeHTML = `<iframe width="100%" height="100%" frameborder="0" scrolling="no" style="filter: invert(100%) hue-rotate(180deg) brightness(90%) contrast(120%); border-radius: 8px;" src="https://www.openstreetmap.org/export/embed.html?bbox=${lon-0.008}%2C${lat-0.008}%2C${lon+0.008}%2C${lat+0.008}&layer=mapnik&marker=${lat}%2C${lon}"></iframe>`;
                            document.getElementById(mapId).innerHTML = iframeHTML;
                        }, (err) => { document.getElementById(mapId).innerHTML = "⚠️ Señal GPS denegada."; }, { enableHighAccuracy: true });
                    }
                }, 800);
            }

            // 🚁 INTERCEPTOR DE CÁMARA Y HUD DRON
            if (emisor === 'amiti' && (texto.includes("DRONE") || texto.includes("SISTEMA DE VISIÓN"))) {
                const hudId = 'hud-' + Date.now();
                contenidoHTML += `<br><div class="drone-hud" id="${hudId}">
                    <div class="drone-cam-overlay">🔴 DRONE CAM STREAM | OPTICAL LOCK</div>
                    <div class="crosshair"></div>
                    <canvas id="canvas-${hudId}" width="400" height="200" style="width:100%; height:100%;"></canvas>
                </div>`;
                
                setTimeout(() => {
                    let canvas = document.getElementById(`canvas-${hudId}`);
                    if(canvas) {
                        let ctx = canvas.getContext('2d');
                        let angle = 0;
                        setInterval(() => {
                            ctx.fillStyle = '#01120f';
                            ctx.fillRect(0, 0, canvas.width, canvas.height);
                            // Renderizado simulación de visión óptica
                            ctx.strokeStyle = '#00ffcc';
                            ctx.lineWidth = 1;
                            ctx.beginPath();
                            ctx.arc(canvas.width/2, canvas.height/2, 40 + Math.sin(angle)*5, 0, Math.PI*2);
                            ctx.stroke();
                            ctx.fillStyle = '#00ffcc';
                            ctx.font = '10px monospace';
                            ctx.fillText(`ALTITUD: EN VUELO | SENSOR OPTICO OK`, 10, canvas.height - 10);
                            angle += 0.1;
                        }, 100);
                    }
                }, 300);
            }

            div.innerHTML = contenidoHTML;
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function prepararPantallaParaCalculo(msg) {
            let m = msg.toLowerCase();
            if (m.includes("dron") || m.includes("elevar") || m.includes("avanca") || m.includes("retrocede") || m.includes("aterriza")) {
                document.getElementById('estado-aprendizaje').innerText = "🚁 Transmitiendo paquete UDP de telemetría...";
            }
        }

        function solicitarTelemetriaAutonoma() {
            fetch('/api/sistema/telemetria')
            .then(res => res.json())
            .then(data => {
                document.getElementById('progreso-num').innerText = data.progreso_global;
                document.getElementById('val-db').innerText = data.status_db;
                document.getElementById('val-mantenimiento').innerText = data.ultimo_auto_mantenimiento;
                document.getElementById('val-dron').innerText = data.estado_dron;
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
    exito = amiti_system.validar_creador(llave) or (llave.lower() == "amiti")
    return jsonify({"desbloqueado": bool(exito)})

@app.route("/api/sistema/telemetria", methods=["GET"])
def obtener_telemetria():
    try: progreso_base = amiti_system.obtener_progreso()
    except Exception: progreso_base = 47
    
    progreso_real = min(100, max(progreso_base, 47 + telemetria_sistema["comandos_procesados"]))
    return jsonify({
        "progreso_global": progreso_real,
        "status_db": telemetria_sistema["status_db"],
        "ultimo_auto_mantenimiento": telemetria_sistema["ultimo_auto_mantenimiento"],
        "comandos_procesados": telemetria_sistema["comandos_procesados"],
        "carga_nucleo_simulada": telemetria_sistema["carga_nucleo_simulada"],
        "estado_dron": telemetria_sistema["estado_dron"]
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    global historial_corto_plazo, telemetria_sistema
    data = request.json or {}
    texto_usuario = data.get("texto", "").strip()
    texto_lower = texto_usuario.lower()
    telemetria_sistema["comandos_procesados"] += 1

    try:
        # 🚁 1. CONTROLADORES NLP DIRECTOS PARA LOS COMANDOS DEL DRON
        
        # COMANDO 1: Elevación básica (1.65m)
        if "elevar el dron" in texto_lower or "eleva el dron" in texto_lower:
            respuesta = drone_engine.encender_y_elevar(1.65)

        # COMANDO 2: Elevar más alto (1.85m)
        elif "eleva el un poco más alto dron" in texto_lower or "más alto dron" in texto_lower or "mas alto" in texto_lower:
            respuesta = drone_engine.elevar_mas(1.85)
            
        # COMANDO NUEVO: Aterrizar
        elif "aterriza" in texto_lower or "bajar dron" in texto_lower or "detener vuelo" in texto_lower:
            respuesta = drone_engine.aterrizar()

        # COMANDO 3: Avanzar hacia adelante
        elif "avanca el dron" in texto_lower or "avanza el dron" in texto_lower or "para de lante" in texto_lower or "adelante" in texto_lower:
            respuesta = drone_engine.mover_adelante()

        # COMANDO 4: Retroceder
        elif "retrocede" in texto_lower or "atras" in texto_lower or "retroceder" in texto_lower:
            respuesta = drone_engine.mover_retroceder()

        # COMANDO 5: Mover a la derecha o izquierda
        elif "derecho" in texto_lower or "derecha" in texto_lower:
            respuesta = drone_engine.mover_lateral("derecho")
        elif "izquierdo" in texto_lower or "izquierda" in texto_lower:
            respuesta = drone_engine.mover_lateral("izquierdo")

        # CAMBIO DE CÁMARA / VISIÓN
        elif "camara" in texto_lower or "cámara" in texto_lower or "ver entorno" in texto_lower:
            respuesta = drone_engine.alternar_camara()

        # 🗺️ MAPA Y GPS
        elif any(kw in texto_lower for kw in ["mapa", "donde estoy", "dónde estoy", "ubicacion", "ubicación"]):
            respuesta = "Sincronizando coordenadas GPS en tiempo real. Desplegando interfaz de mapas en pantalla, Creador."

        # 🔓 LLAVE MAESTRA
        elif texto_lower == "amiti":
            respuesta = "🔓 **[SISTEMA DESBLOQUEADO]** Llave maestra aceptada. Motores listos para operar."

        # 📚 BIBLIOTECA VIRTUAL
        elif biblioteca_engine and any(kw in texto_lower for kw in ["búscame", "buscame", "consulta", "biblioteca", "información"]):
            respuesta = biblioteca_engine.buscar_en_biblioteca(texto_usuario)

        # ⚙️ PROCESAMIENTO GENERAL
        else:
            respuesta = amiti_system.procesar(texto_usuario)

    except Exception as e:
        respuesta = f"⚠️ **ERROR DE NÚCLEO DRON:** {str(e)}"

    return jsonify({"respuesta": respuesta})

@app.route('/enviar', methods=['POST'])
def enviar():
    global telemetria_sistema
    comando = request.form.get('comando', '').strip()
    telemetria_sistema["comandos_procesados"] += 1
    
    try: respuesta_cruda = amiti_system.procesar(comando)
    except Exception as e: respuesta_cruda = f"⚠️ Error: {str(e)}"

    return jsonify({
        "respuesta": respuesta_cruda,
        "progreso": min(100, 47 + telemetria_sistema["comandos_procesados"]),
        "identidad": "AMITI OS"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
