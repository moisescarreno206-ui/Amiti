import os
from flask import Flask, render_template, request, jsonify
import math, re, sqlite3

# --- NÚCLEO MAESTRO FUSIONADO ---
class NucleoMaestro:
    def __init__(self):
        self.bloqueado = True
        self.db = "amiti_core.db"
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS conocimiento (id INTEGER PRIMARY KEY, info TEXT)")

    def procesar(self, cmd):
        cmd = cmd.lower().strip()
        if cmd == "amiti": self.bloqueado = False; return "SISTEMA DESBLOQUEADO."
        if self.bloqueado: return "SISTEMA BLOQUEADO."
        
        # Núcleo Matemático
        if any(x in cmd for x in ["+", "-", "*", "/", "raiz", "suma"]):
            try:
                if "raiz" in cmd: return f"Resultado: {math.sqrt(float(re.search(r'\d+', cmd).group()))}"
                return f"Resultado: {eval(re.sub(r'[^0-9+\-*/.]', '', cmd))}"
            except: return "Error en cálculo."
            
        return "Misión recibida y procesada."

amiti = NucleoMaestro()

# --- CONFIGURACIÓN APP ---
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def ejecutar():
    try:
        data = request.json
        return jsonify({"respuesta": amiti.procesar(data.get('comando', ''))})
    except Exception as e:
        return jsonify({"respuesta": f"ERROR: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
                        
