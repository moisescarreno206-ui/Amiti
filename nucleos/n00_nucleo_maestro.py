import re
import math
import requests
import os

class NucleoMaestro:
    def __init__(self):
        self.bloqueado = True
        self.log_file = "memoria_amiti.txt"
        self.nivel_seguridad = "EXTREMO"

    def _interceptar_ataque(self, comando):
        # Núcleo 14: Filtro de inyección SQL y comandos maliciosos
        patrones_peligrosos = [r"drop table", r"select \* from", r"union all", r"<script>", r"rm -rf"]
        for patron in patrones_peligrosos:
            if re.search(patron, comando, re.IGNORECASE):
                self._escribir_memoria(f"ALERTA: Ataque bloqueado detectado: {comando}")
                return True
        return False

    def procesar(self, comando):
        cmd = comando.strip().lower()
        
        # Núcleo 13: Defensa Activa
        if self._interceptar_ataque(cmd):
            return "INTENTO DE VIOLACIÓN DETECTADO. Contramedidas activadas. Acceso bloqueado permanentemente para este hilo."

        if cmd == "amiti":
            self.bloqueado = False
            return "SISTEMA SEGURO. Creador identificado. Núcleos de combate en línea."
        
        if self.bloqueado: return "SISTEMA BLOQUEADO."

        # Integración de núcleos existentes
        if "investiga" in cmd: return "Modo investigación activo."
        if any(op in cmd for op in ["suma", "raiz"]): return "Modo científico activo."

        return "Procesando misión..."

    def _escribir_memoria(self, evento):
        with open(self.log_file, "a") as f:
            f.write(f"[SEGURIDAD: {self.nivel_seguridad}] {evento}\n")

amiti = NucleoMaestro()
