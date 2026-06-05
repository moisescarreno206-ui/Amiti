# main.py - El Orquestador Maestro
import sqlite3
# Importamos lógica modular (puedes tenerlas en funciones dentro del mismo archivo)
from logica_amiti import procesar_IA, gestionar_memoria, ejecutar_comando

@app.route('/', methods=['POST'])
def handle():
    mensaje = request.form.get("msg")
    # 1. AMITI intenta ejecutar un comando
    respuesta = ejecutar_comando(mensaje)
    if not respuesta:
        # 2. Si no es comando, AMITI busca en su memoria
        respuesta = procesar_IA(mensaje)
    
    # 3. AMITI guarda la interacción para aprender
    gestionar_memoria(mensaje, respuesta)
    return render_template(respuesta)
    
