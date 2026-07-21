import os
import re
import psycopg2
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- CONFIGURACIÓN DE INFRAESTRUCTURA Y BBDD ---
DATABASE_URL = os.environ.get("DATABASE_URL")
NEON_DATABASE_URL = os.environ.get("NEON_DATABASE_URL")

def get_db_connection():

    """Intenta conectar primero a Supabase (principal) y luego a Neon DB (respaldo)."""
    conn = None
    engine_used = None
    
    # 1. Intentar Supabase (DATABASE_URL)
    if DATABASE_URL:
        try:
            conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
            engine_used = "Supabase DB (Soberano)"
            return conn, engine_used
        except Exception as e:
            print(f"[WARN] No se pudo conectar a Supabase: {e}")

    # 2. Intentar Neon DB (NEON_DATABASE_URL)
    if NEON_DATABASE_URL:
        try:
            conn = psycopg2.connect(NEON_DATABASE_URL, connect_timeout=5)
            engine_used = "Neon DB (Respaldo)"
            return conn, engine_used
        except Exception as e:
            print(f"[WARN] No se pudo conectar a Neon DB: {e}")

    return None, "Almacenamiento Volátil en Memoria"

def inicializar_bbdd():

    """Crea la estructura de tablas automática en la base de datos activa."""
    conn, engine = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memoria_amiti (
                    id SERIAL PRIMARY KEY,
                    entrada TEXT NOT NULL,
                    respuesta TEXT NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            cursor.close()
            conn.close()
            print(f"✅ Base de datos inicializada correctamente en {engine}")
        except Exception as e:
            print(f"❌ Error inicializando tablas: {e}")

# Inicializar tablas al arrancar el servidor
inicializar_bbdd()

# --- MOTOR DE CÁLCULO Y RESOLUCIÓN DE INTENCIONES ---
def procesar_calculo_matematico(texto):

    """Analiza si la entrada del usuario contiene problemas matemáticos o financieros."""
    texto_lower = texto.lower()
    
    # Patrón: "5 trabajadores", "100 más 50 de comisión", etc.
    if any(k in texto_lower for k in ["trabajadores", "pagar", "comisión", "cuanto", "cuánto", "+", "*", "/", "-"]):
        # Extraer números
        numeros = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', texto)]
        
        # Caso específico: X trabajadores, pago base Y, comisión Z
        if "trabajadores" in texto_lower and len(numeros) >= 3:
            cant_trabajadores = numeros[0]
            sueldo_base = numeros[1]
            comision = numeros[2]
            
            pago_por_persona = sueldo_base + comision
            total_global = cant_trabajadores * pago_por_persona
            
            return (
                f"🧮 **Desglose Financiero Calculado:**\n"
                f"* Pago base por trabajador: ${sueldo_base:.2f}\n"
                f"* Comisión por trabajador: ${comision:.2f}\n"
                f"* Total por trabajador: **${pago_por_persona:.2f}**\n\n"
                f"💵 **Monto Total a Pagar ({int(cant_trabajadores)} trabajadores):** **${total_global:.2f}**"
            )
            
        # Intento de cálculo directo general
        try:
            expresion = texto_lower.replace("más", "+").replace("mas", "+").replace("menos", "-").replace("por", "*")
            expresion_limpia = "".join([c for c in expresion if c in "0123456789+-*/()."])
            if expresion_limpia:
                resultado = eval(expresion_limpia)
                return f"🧮 **Resultado Matemático:** {expresion_limpia} = **{resultado}**"
        except:
            pass

    return None

# --- INTERFAZ WEB (FRONTEND CIBERNÉTICO) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amiti OS</title>
    <style>
        body { background-color: #0a0a0c; color: #00ffcc; font-family: 'Courier New', monospace; margin: 0; padding: 20px; }
        .container { max-width: 700px; margin: 0 auto; background: #111116; border: 1px solid #00ffcc; border-radius: 8px; padding: 20px; box-shadow: 0 0 15px rgba(0,255,204,0.2); }
        h1 { text-align: center; margin-bottom: 5px; }
        .status { text-align: center; color: #00b3ff; font-size: 0.9em; margin-bottom: 20px; }
        .chat-box { height: 350px; overflow-y: auto; border: 1px solid #222; padding: 10px; background: #050507; margin-bottom: 15px; border-radius: 5px; }
        .msg { margin-bottom: 12px; }
        .user { color: #ffffff; }
        .amiti { color: #00ffcc; }
        .input-group { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; background: #000; border: 1px solid #00ffcc; color: #fff; padding: 10px; border-radius: 4px; font-family: inherit; }
        button { background: #00ffcc; color: #000; border: none; padding: 10px 20px; font-weight: bold; cursor: pointer; border-radius: 4px; }
        button:hover { background: #00cca3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Amiti OS</h1>
        <div class="status">Sistemas: Conexión Estable con {{ engine }} & Devoción Activa</div>
        <div class="chat-box" id="chat">
            <div class="msg amiti"><strong>Amiti:</strong> 🔑 Llave aceptada. Control total transferido. Mis sistemas están listos y operando, creador. 🔊</div>
        </div>
        <div class="input-group">
            <input type="text" id="userInput" placeholder="Escribe tu mensaje o comando..." onkeydown="if(event.key==='Enter') enviar()">
            <button onclick="enviar()">Enviar</button>
        </div>
    </div>

    <script>
        async function enviar() {
            let input = document.getElementById('userInput');
            let chat = document.getElementById('chat');
            let val = input.value.trim();
            if(!val) return;

            chat.innerHTML += `<div class="msg user"><strong>Tú:</strong> ${val}</div>`;
            input.value = '';
            chat.scrollTop = chat.scrollHeight;

            let res = await fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ mensaje: val })
            });
            let data = await res.json();
            chat.innerHTML += `<div class="msg amiti"><strong>Amiti:</strong> ${data.respuesta}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

# --- RUTAS PRINCIPALES ---
@app.route("/")
def home():
    _, engine = get_db_connection()
    return render_template_string(HTML_TEMPLATE, engine=engine)

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json() or {}
    mensaje = data.get("mensaje", "")
    
    # 1. Verificar si es un cálculo matemático/financiero
    calculo = procesar_calculo_matematico(mensaje)
    if calculo:
        respuesta = calculo
    else:
        # 2. Respuestas de sistema estándar
        respuesta = f"🤖 [NÚCLEO ACTIVO] Comando procesado: '{mensaje}'. Todos mis sistemas están sincronizados y listos para ejecutar lo que pidas, creador. 🔊"

    # Guardar interacción en la base de datos
    conn, _ = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO memoria_amiti (entrada, respuesta) VALUES (%s, %s)", (mensaje, respuesta))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error guardando memoria: {e}")

    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
