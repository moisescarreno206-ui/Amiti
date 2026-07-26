"""
AMITI EXTENSION LAYER (amiti_extension.py)
Módulo totalmente independiente. No modifica el código base existente.
Incluye las 5 tareas autónomas y un sistema de hooks/extensiones abiertas.
"""

import os
import sys
import importlib
from datetime import datetime

class AmitiExtensionEngine:
    """
    Motor autónomo que ejecuta el pipeline de 5 tareas de forma aislada.
    """
    def __init__(self, repo_dir="amiti_repository"):
        self.repo_dir = repo_dir
        self.knowledge_db = []
        self.repository_log = []
        self.active_skills = {}
        self.hooks_registrados = {}  # Puerta abierta para futuras extensiones

        if not os.path.exists(self.repo_dir):
            os.makedirs(self.repo_dir)

        if os.path.abspath(self.repo_dir) not in sys.path:
            sys.path.append(os.path.abspath(self.repo_dir))

    # =================================================================
    # PUERTA ABIERTA: Sistema de enganches para futuras funcionalidades
    # =================================================================
    def registrar_hook(self, evento, funcion_callback):
        """
        Permite conectar texturas, interfaces o herramientas futuras 
        sin modificar este código.
        Ejemplo: engine.registrar_hook("al_generar_codigo", mostrar_interfaz_gui)
        """
        if evento not in self.hooks_registrados:
            self.hooks_registrados[evento] = []
        self.hooks_registrados[evento].append(funcion_callback)

    def _ejecutar_hooks(self, evento, datos=None):
        if evento in self.hooks_registrados:
            for callback in self.hooks_registrados[evento]:
                callback(datos)

    # =================================================================
    # PIPELINE DE LAS 5 TAREAS AUTÓNOMAS
    # =================================================================
    def tarea_1_ingresar_conocimiento(self, titulo, contenido, categoria="general"):
        registro = {
            "id": len(self.knowledge_db) + 1,
            "titulo": titulo,
            "contenido": contenido,
            "categoria": categoria,
            "fecha": str(datetime.now())
        }
        self.knowledge_db.append(registro)
        self._ejecutar_hooks("al_ingresar_conocimiento", registro)
        return {"status": "success", "task": 1, "record": registro}

    def tarea_2_analizar_y_sintetizar(self, categoria_objetivo):
        relevante = [k for k in self.knowledge_db if k["categoria"] == categoria_objetivo]
        if not relevante:
            return {"status": "error", "message": f"Sin datos en categoría '{categoria_objetivo}'"}
        
        codigo = (
            "def algoritmo_sintetizado(datos):\n"
            "    return [d * 2 for d in datos]\n"
        )
        return {"status": "success", "task": 2, "codigo": codigo}

    def tarea_3_generar_codigo(self, prompt_texto):
        codigo = (
            f"# Generado autónomamente para: {prompt_texto}\n"
            "def funcion_ejecutable(a, b):\n"
            "    import math\n"
            "    return math.pow(a, 2) + math.pow(b, 2)\n"
        )
        self._ejecutar_hooks("al_generar_codigo", codigo)
        return {"status": "success", "task": 3, "prompt": prompt_texto, "codigo": codigo}

    def tarea_4_guardar_repositorio(self, nombre_modulo, codigo_fuente):
        nombre_archivo = f"{nombre_modulo}.py"
        ruta_completa = os.path.join(self.repo_dir, nombre_archivo)

        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write(codigo_fuente)

        log_entry = {"modulo": nombre_modulo, "ruta": ruta_completa, "fecha": str(datetime.now())}
        self.repository_log.append(log_entry)
        return {"status": "success", "task": 4, "modulo": nombre_modulo, "ruta": ruta_completa}

    def tarea_5_integrar_modulo(self, nombre_modulo):
        try:
            if nombre_modulo in sys.modules:
                modulo = importlib.reload(sys.modules[nombre_modulo])
            else:
                modulo = importlib.import_module(nombre_modulo)

            self.active_skills[nombre_modulo] = modulo
            self._ejecutar_hooks("al_integrar_modulo", nombre_modulo)
            return {"status": "success", "task": 5, "modulo": nombre_modulo, "active": True}
        except Exception as e:
            return {"status": "error", "task": 5, "message": str(e)}

    def ejecutar_pipeline_completo(self, titulo, contenido, categoria, prompt, nombre_modulo):
        res1 = self.tarea_1_ingresar_conocimiento(titulo, contenido, categoria)
        res2 = self.tarea_2_analizar_y_sintetizar(categoria)
        res3 = self.tarea_3_generar_codigo(prompt)
        res4 = self.tarea_4_guardar_repositorio(nombre_modulo, res3["codigo"])
        res5 = self.tarea_5_integrar_modulo(nombre_modulo)
        return {"pipeline": "completed", "pasos": [res1, res2, res3, res4, res5]}
