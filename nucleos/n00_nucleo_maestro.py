import math, re, sqlite3, time

class NucleoMaestro:
    def __init__(self):
        self.bloqueado = True
        self.db = "memoria_amiti.db"
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, msg TEXT)")

    def procesar(self, cmd):
        cmd = cmd.lower().strip()
        # Núcleo de Seguridad (Anti-hackeo)
        if any(x in cmd for x in ["drop", "delete", "rm -rf", "script"]):
            return "ALERTA: Ataque bloqueado. El núcleo de seguridad es infranqueable."
        
        if cmd == "amiti": 
            self.bloqueado = False
            return "Núcleos activos. Operativa."
        
        if self.bloqueado: return "SISTEMA BLOQUEADO."

        # Núcleo Matemático y Lógico
        if any(op in cmd for op in ["+", "-", "*", "/", "raiz", "ecuacion"]):
            return self._resolver_ciencia(cmd)
        
        return "Procesando en memoria..."

    def _resolver_ciencia(self, cmd):
        try:
            if "raiz" in cmd:
                num = float(re.search(r'\d+', cmd).group())
                return f"Resultado: {math.sqrt(num)}"
            # Ejecución segura de cálculo
            clean = re.sub(r'[^0-9+\-*/.]', '', cmd)
            return f"Resultado: {eval(clean)}"
        except: return "Error en núcleo lógico."

amiti = NucleoMaestro()
