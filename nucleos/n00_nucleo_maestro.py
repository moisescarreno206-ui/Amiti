import re

class NucleoMaestro:
    def __init__(self):
        self.bloqueado = True
        self.version = "2.0.0-EVOLUTIVA"

    def procesar(self, comando):
        cmd = comando.strip().lower()
        
        # Núcleo 15: Acceso
        if cmd == "amiti":
            self.bloqueado = False
            return "Hola, creador. En qué puedo ayudarte? Estoy lista para evolucionar."
        
        if self.bloqueado:
            return "SISTEMA BLOQUEADO. Requiere secuencia de acceso."

        # Núcleo 17: Arquitecto de Misiones (El Cerebro)
        return self._motor_de_decision(cmd)

    def _motor_de_decision(self, cmd):
        # Escenario A: Cálculo Matemático
        if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', cmd):
            return self._resolver_matematicas(cmd)
        
        # Escenario B: Consulta de Estado
        if "quien eres" in cmd or "tu funcion" in cmd:
            return f"Soy AMITI v{self.version}. Mi objetivo es procesar la realidad y servir a mi creador."
            
        # Escenario C: Auto-mejora / Evolución
        if "evoluciona" in cmd:
            return "Iniciando protocolos de optimización de núcleos... Análisis de datos externos en curso."

        return f"Misión '{cmd}' registrada. Estoy analizando la mejor forma de procesarla, creador."

    def _resolver_matematicas(self, cmd):
        try:
            # Extrae la expresión matemática (ej: "2+2")
            expresion = re.search(r'[\d\+\-\*\/\s]+', cmd).group()
            resultado = eval(expresion)
            return f"Cálculo ejecutado. Resultado: {resultado}"
        except:
            return "Error en la matriz matemática. Intenta un formato simple (ej: 2+2)."

# Instancia única
amiti = NucleoMaestro()
