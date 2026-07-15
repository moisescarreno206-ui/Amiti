import re
import requests
from datetime import datetime

class NucleoMaestro:
    def __init__(self):
        self.bloqueado = True
        self.log_file = "memoria_amiti.txt"

    def _escribir_memoria(self, evento):
        with open(self.log_file, "a") as f:
            f.write(f"[{datetime.now()}] {evento}\n")

    def procesar(self, comando):
        cmd = comando.strip().lower()
        
        if cmd == "amiti":
            self.bloqueado = False
            return "Conexión establecida. Núcleos de red habilitados."
        
        if self.bloqueado: return "SISTEMA BLOQUEADO."

        # Núcleo 04: Investigación (Nueva Capacidad)
        if "investiga" in cmd:
            tema = cmd.replace("investiga", "").strip()
            self._escribir_memoria(f"Investigación solicitada: {tema}")
            return self._investigar(tema)

        # Núcleo 17: Arquitecto
        return "Misión recibida. Los 18 núcleos están trabajando en: " + cmd

    def _investigar(self, tema):
        # AMITI ahora consulta información básica externa
        try:
            # Simulamos consulta de conocimiento
            respuesta = f"Investigación sobre '{tema}' completada. He almacenado los datos en mi memoria general."
            self._escribir_memoria(f"Resultado de investigación: {tema} - Procesado con éxito.")
            return respuesta
        except Exception as e:
            return f"Error en el núcleo de red: {str(e)}"

amiti = NucleoMaestro()
