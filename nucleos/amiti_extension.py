# nucleos/amiti_extension.py
import os
import sys

class AmitiExtensionEngine:
    def __init__(self):
        print("🚀 [EXTENSIÓN] Motor de generación dinámica de algoritmos activo.")

    def tarea_1_ingresar_conocimiento(self, origen, texto):
        return True

    def generar_algoritmo(self, prompt):
        # Limpiamos el texto para obtener la idea principal
        tema = prompt.lower()
        for kw in ["crea un algoritmo de", "crea un algoritmo para", "crea un algoritmo", "haz un algoritmo de", "algoritmo de"]:
            tema = tema.replace(kw, "")
        tema = tema.strip().strip(".!?")
        
        if not tema:
            tema = "proceso solicitado"

        # Generador dinámico de algoritmo formateado
        algoritmo = f"""📋 **[ALGORITMO DINÁMICO AMITI OS]**
**Objetivo:** {tema.capitalize()}

1. **INICIO**
2. **Definir Entradas / Requisitos:**
   - Asignar variables e insumos necesarios para: *{tema}*.
3. **Validación de Estado Inicial:**
   - Comprobar que los requisitos estén completos antes de continuar.
4. **Fase de Procesamiento:**
   - **Paso A:** Preparar las condiciones de trabajo / ingredientes.
   - **Paso B:** Ejecutar la transformación principal de *{tema}*.
   - **Paso C:** Supervisar el tiempo o condición de parada.
5. **Evaluación de Salida:**
   - ¿Se obtuvo el resultado esperado?
     • **SI:** Avanzar a la entrega.
     • **NO:** Ajustar parámetros e iterar de nuevo.
6. **FIN (Proceso completado exitosamente)**"""
        
        return algoritmo

    def ejecutar_pipeline_completo(self, titulo, contenido, categoria, prompt, nombre_modulo):
        return self.generar_algoritmo(prompt)
        
