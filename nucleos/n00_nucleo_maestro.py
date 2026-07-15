import math, time, sqlite3, os, re

class NucleoMaestro:
    def __init__(self):
        self.bloqueado = True
        self.db_path = "memoria_amiti.db"
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS memoria (id INTEGER PRIMARY KEY, accion TEXT)")

    def procesar(self, comando):
        cmd = comando.lower().strip()
        if cmd == "amiti": 
            self.bloqueado = False
            return "Hola, creador. En qué puedo ayudarte? Estoy lista para evolucionar."
        if self.bloqueado: return "SISTEMA BLOQUEADO."
        
        # Núcleo 07: Motor Científico (Suma, resta, raíz, etc.)
        if any(x in cmd for x in ["+", "-", "*", "/", "raiz", "suma", "resta"]):
            return self._ejecutar_ciencia(cmd)
        
        return "Misión registrada."

    def _ejecutar_ciencia(self, cmd):
        try:
            # Lógica extendida para cálculos
            if "raiz" in cmd: return math.sqrt(float(re.search(r'\d+', cmd).group()))
            return str(eval(re.sub(r'[^0-9+\-*/.]', '', cmd)))
        except: return "Error en núcleo lógico."

amiti = NucleoMaestro()
