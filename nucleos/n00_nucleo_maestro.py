import re
import math
import requests

class NucleoMaestro:
    def __init__(self):
        self.bloqueado = True
        self.log_file = "memoria_amiti.txt"

    def procesar(self, comando):
        cmd = comando.strip().lower()
        if cmd == "amiti":
            self.bloqueado = False
            return "Hola, creador. En qué puedo ayudarte? Estoy lista para evolucionar."
        
        if self.bloqueado: return "SISTEMA BLOQUEADO."

        # NÚCLEO MATEMÁTICO AVANZADO
        if any(op in cmd for op in ["suma", "resta", "raiz", "ecuacion"]):
            return self._ejecutar_ciencia(cmd)
            
        # NÚCLEO DE INVESTIGACIÓN (Google)
        if "investiga" in cmd:
            tema = cmd.replace("investiga", "").strip()
            return self._conectar_red(tema)

        return "Procesando misión en memoria general..."

    def _ejecutar_ciencia(self, cmd):
        try:
            # Ejemplo: "raiz 25" -> 5.0
            if "raiz" in cmd:
                num = float(re.findall(r'\d+', cmd)[0])
                return f"Resultado científico: {math.sqrt(num)}"
            # Aquí AMITI puede escalar a ecuaciones complejas
            return "Núcleo científico operativo. Esperando parámetros."
        except: return "Error en el cálculo científico."

    def _conectar_red(self, tema):
        # Aquí es donde AMITI sale al mundo real
        return f"Conectando a nodos globales... Recopilando datos masivos sobre {tema} para mi evolución."

amiti = NucleoMaestro()
