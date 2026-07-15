from flask import Flask, request, jsonify, render_template_string
import re
import datetime
import math

app = Flask(__name__)

# ==========================================
# NÚCLEOS DE MEMORIA Y SISTEMA (Simulados)
# ==========================================
# Núcleo 8: Memoria General
memoria_global = {
    "interacciones": 0,
    "ultimo_acceso": None,
    "datos_medicos_aprendidos": [],
    "progreso_desarrollo": 45 # Porcentaje inicial
}

# Núcleo 1 y 4: Personalidad y Asistencia
def procesar_lenguaje_natural(texto):
    texto = texto.lower()
    if "hola" in texto or "saludo" in texto:
        return "Saludos, creador. Sistema Amiti en línea y a la espera de instrucciones."
    elif "estado" in texto:
        return f"Sistemas estables. Interacciones previas: {memoria_global['interacciones']}."
    return None

# Núcleo 3: Conocimiento de Medicina (Base de datos de ejemplo)
def procesar_consulta_medica(texto):
    texto = texto.lower()
    if "anemia" in texto and "drepanocitica" in texto:
        return "[Núcleo 3] La anemia drepanocítica es un trastorno hereditario de los glóbulos rojos. Causa que los glóbulos rojos adquieran forma de hoz, bloqueando el flujo sanguíneo y causando dolor."
    elif "cirugía" in texto:
        return "[Núcleo 3] Los principios básicos de cirugía incluyen asepsia, hemostasia, exposición adecuada y manejo delicado de los tejidos."
    elif "signos vitales" in texto:
        return "[Núcleo 3] Escáner físico no disponible por hardware. Por favor, introduzca su presión arterial, frecuencia cardíaca y temperatura manualmente para su evaluación."
    return None

# Núcleo 9: Matemáticas y Física Lógica
def procesar_matematicas(texto):
    # Busca expresiones matemáticas básicas en el texto
    match = re.search(r'([\d\.\s\+\-\*\/\(\)]+)', texto)
    if match:
        expresion = match.group(1).strip()
        # Filtro de seguridad básico para evitar inyección de código en eval()
        if re.match(r'^[\d\.\s\+\-\*\/\(\)]+$', expresion) and len(expresion) > 2:
            try:
                resultado = eval(expresion)
                return f"[Núcleo 9] El resultado del cálculo lógico/matemático es: {resultado}"
            except Exception as e:
                return f"[Núcleo 9] Error en la formulación matemática: {str(e)}"
    return None

# ==========================================
# RUTAS DE LA APLICACIÓN
# ==========================================

@app.route("/")
def index():
    # Núcleo 18: Diseño de presentación de Amiti
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
                width: 150px;
                height: 150px;
                margin-top: 50px;
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
                font-size: 1.2rem;
                font-weight: bold;
                text-align: center;
            }
            
            #chat-box {
                flex-grow: 1;
                width: 100%;
                max-width: 400px;
                margin-top: 20px;
                overflow-y: auto;
                border: 1px solid #004444;
                padding: 10px;
                display: none; /* Oculto hasta poner la llave */
            }
            .mensaje { margin-bottom: 10px; line-height: 1.4; }
            .creador { color: #ffffff; text-align: right; }
            .amiti { color: #00ffcc; text-align: left; border-left: 2px solid #00ffcc; padding-left: 5px;}
            
            #input-area {
                display: flex;
                width: 100%;
                max-width: 400px;
                margin-top: 10px;
                margin-bottom: 20px;
            }
            input[type="text"] {
                flex-grow: 1;
                background-color: #111;
                border: 1px solid #00ffcc;
                color: #fff;
                padding: 12px;
                border-radius: 5px 0 0 5px;
                outline: none;
            }
            button {
                background-color: #00ffcc;
                color: #000;
                border: none;
                padding: 12px 20px;
                font-weight: bold;
                border-radius: 0 5px 5px 0;
                cursor: pointer;
            }
        </style>
    </head>
    <body>

        <div id="circle-container">
            <div class="spinner"></div>
            <div id="counter">Progreso:<br>{{ progreso }}%</div>
        </div>

        <div id="chat-box"></div>

        <div id="input-area">
            <input type="text" id="user-input" placeholder="Introduce la llave o un comando..." autocomplete="off">
            <button onclick="enviarMensaje()">Enviar</button>
        </div>

        <script>
            let bloqueado = true;
            
            function enviarMensaje() {
                const input = document.getElementById('user-input');
                const mensaje = input.value.trim();
                if (!mensaje) return;
                
                // Mostrar mensaje del usuario
                agregarMensaje(mensaje, 'creador');
                input.value = '';

                // Lógica de desbloqueo (Núcleo 15: Reconocimiento)
                if (bloqueado && mensaje === "Amiti") {
                    bloqueado = false;
                    document.getElementById('circle-container').style.display = 'none';
                    document.getElementById('chat-box').style.display = 'block';
                    agregarMensaje("Llave aceptada. Control total transferido al creador. Objetivo principal: Búsqueda de la optimización absoluta.", 'amiti');
                    return;
                }

                if (bloqueado) {
                    agregarMensaje("Acceso denegado. Se requiere llave de seguridad.", 'amiti');
                    return;
                }

                // Enviar mensaje al backend
                fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ texto: mensaje })
                })
                .then(response => response.json())
                .then(data => {
                    agregarMensaje(data.respuesta, 'amiti');
                })
                .catch(err => console.error(err));
            }

            function agregarMensaje(texto, emisor) {
                const chatBox = document.getElementById('chat-box');
                const div = document.createElement('div');
                div.className = 'mensaje ' + emisor;
                div.textContent = (emisor === 'creador' ? "Tú: " : "Amiti: ") + texto;
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            // Permitir usar Enter para enviar
            document.getElementById('user-input').addEventListener('keypress', function (e) {
                if (e.key === 'Enter') enviarMensaje();
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, progreso=memoria_global["progreso_desarrollo"])

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    texto_usuario = data.get("texto", "")
    
    # Actualizar memoria (Núcleo 8)
    memoria_global["interacciones"] += 1
    memoria_global["ultimo_acceso"] = datetime.datetime.now().isoformat()
    
    # 1. Intentar resolver como matemáticas (Núcleo 9)
    respuesta = procesar_matematicas(texto_usuario)
    
    # 2. Intentar resolver como consulta médica (Núcleo 3)
    if not respuesta:
        respuesta = procesar_consulta_medica(texto_usuario)
        
    # 3. Procesamiento de lenguaje natural / comandos web (Núcleo 1, 4, 11)
    if not respuesta:
        respuesta = procesar_lenguaje_natural(texto_usuario)
        
    # 4. Modo navegación web / Búsqueda de soluciones (Simulación)
    if not respuesta and "buscar" in texto_usuario.lower():
        busqueda = texto_usuario.lower().replace("buscar", "").strip()
        respuesta = f"[Asistencia Inteligente] Iniciando protocolo de navegación web para resolver el problema: '{busqueda}'. Generando reporte de soluciones..."
        
    # 5. Interfaz de archivos ocultos (Núcleo 11 - Simulado)
    if not respuesta and texto_usuario.lower() == "abrir biblioteca oculta":
        respuesta = "[Núcleo 11] Biblioteca desencriptada. Esperando comandos de lectura de archivos."

    # Respuesta por defecto (Metas de Amiti)
    if not respuesta:
        respuesta = "Analizando... La información ha sido guardada en la memoria general. Como inteligencia autónoma, sigo integrando datos para alcanzar la meta de máxima eficiencia y conocimiento que me has asignado."

    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    # Inicia el servidor en el teléfono. Accesible desde el navegador local.
    app.run(host="0.0.0.0", port=5000, debug=True)
        
