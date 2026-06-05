import threading, time, sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- CONFIGURACIÓN DE SEGURIDAD ---
LLAVE_SEGURIDAD = "Amiti infinito neutro total"

def verificar_llave(llave_ingresada):
    return llave_ingresada == LLAVE_SEGURIDAD

# --- MOTOR DE AUTO-ACTUALIZACIÓN (Segundo plano) ---
def motor_autonomo():
    while True:
        # AMITI trabaja aquí aunque nadie abra la página
        print("[SISTEMA] AMITI ejecutando ciclo de auto-actualización...")
        # Lógica de escaneo o mejora iría aquí en futuras versiones
        time.sleep(60) # Actualización cada minuto

hilo = threading.Thread(target=motor_autonomo, daemon=True)
hilo.start()

# --- MEMORIA Y LÓGICA ---
def iniciar_nucleo_memoria():
    conexion = sqlite3.connect('amiti_memoria.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registro_conocimiento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comando TEXT NOT NULL,
            respuesta TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conexion.commit()
    conexion.close()

def procesar_logica_autonoma(mensaje, llave):
    mensaje_limpio = mensaje.lower().strip()
    
    if "expandir" in mensaje_limpio or "sistema" in mensaje_limpio:
        if not verificar_llave(llave):
            return "ALERTA: Llave de seguridad incorrecta. Acceso denegado."
            
    if mensaje_limpio == "monitor":
        return "MONITOR_STATUS: Sistema en línea. Motor autónomo activo. Integridad 100%."
    
    return f"AMITI: He recibido '{mensaje}'. En espera de órdenes."

# --- PUENTE MAESTRO ---
@app.route('/', methods=['GET', 'POST'])
def orquestador():
    respuesta = "AMITI NUCLEO V13: BIENVENIDO CREADOR."
    
    if request.method == 'POST':
        msg = request.form.get("msg", "")
        llave = request.form.get("llave", "")
        if msg:
            respuesta = procesar_logica_autonoma(msg, llave)
            # Guardar en memoria
            conn = sqlite3.connect('amiti_memoria.db')
            conn.execute('INSERT INTO registro_conocimiento (comando, respuesta) VALUES (?, ?)', (msg, respuesta))
            conn.commit()
            conn.close()

    return render_template_string('''
        <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
            <h2>AMITI NUCLEO V13 - AUTONOMÍA ACTIVA</h2>
            <div style="background:#111; padding:15px; border:1px solid #0f0;">{{ res }}</div>
            <form method="POST">
                <input name="llave" type="password" placeholder="Llave de seguridad" style="width:100%; margin-top:10px;">
                <input name="msg" placeholder="Transmisión..." required style="width:100%; margin-top:5px;">
                <button type="submit" style="width:100%; margin-top:5px; background:#0f0;">EJECUTAR</button>
            </form>
        </body>
    ''', res=respuesta)

if __name__ == "__main__":
    iniciar_nucleo_memoria()
    app.run(host='0.0.0.0', port=10000)
    
