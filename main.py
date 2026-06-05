# main.py
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# --- LÓBULO 1: MEMORIA Y BIBLIOTECA (La base de datos) ---
class Memoria:
    @staticmethod
    def guardar(pregunta, respuesta):
        conn = sqlite3.connect('amiti.db')
        conn.execute('CREATE TABLE IF NOT EXISTS conocimiento (q TEXT, a TEXT)')
        conn.execute('INSERT INTO conocimiento VALUES (?, ?)', (pregunta, respuesta))
        conn.commit()
        conn.close()

# --- LÓBULO 2: ASISTENCIA (IA) ---
class Asistencia:
    @staticmethod
    def procesar(msg):
        # Aquí conectaremos la lógica real de IA
        return f"AMITI Asistencia: Analizando tu input '{msg}' con profundidad."

# --- LÓBULO 3: MONITOR Y SEGURIDAD ---
class Sistema:
    @staticmethod
    def ejecutar(comando):
        if "monitor" in comando: return "ESTADO: Procesador 5%, RAM 200MB, Integridad 100%."
        if "seguridad" in comando: return "SEGURIDAD: Todos los nodos clientes están en reposo."
        return None

# --- EL PUENTE (Orquestador que comunica todo) ---
@app.route('/', methods=['POST', 'GET'])
def puente():
    resultado = "Esperando..."
    if request.method == 'POST':
        msg = request.form.get("msg", "").lower()
        
        # El Puente decide a qué Lóbulo enviar la señal
        comando_sistema = Sistema.ejecutar(msg)
        if comando_sistema:
            resultado = comando_sistema
        else:
            resultado = Asistencia.procesar(msg)
        
        # El Puente le dice a la Memoria que guarde el intercambio
        Memoria.guardar(msg, resultado)
            
    return render_template_string('...', res=resultado)
    
