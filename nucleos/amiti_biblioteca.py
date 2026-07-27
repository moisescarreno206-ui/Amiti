import os
import json

class AmitiBibliotecaEngine:
    def __init__(self):
        # Directorio o endpoint del servidor biblioteca
        self.categorias_soportadas = [
            "medicina", "derecho", "informatica", 
            "programacion", "ganaderia", "quimica", "fisica"
        ]

    def buscar_en_biblioteca(self, consulta_usuario):
        texto_lower = consulta_usuario.lower()
        
        # 1. Identificar la categoría
        categoria_detectada = "general"
        for cat in self.categorias_soportadas:
            if cat in texto_lower:
                categoria_detectada = cat
                break
                
        # 2. Identificar el nivel de gravedad / complejidad
        nivel = "estándar"
        if "basico" in texto_lower or "básico" in texto_lower:
            nivel = "básico"
        elif "avanzado" in texto_lower:
            nivel = "avanzado"
        elif "grave" in texto_lower or "extremo" in texto_lower:
            nivel = "extremo / urgencia"

        # 3. Simulación de recuperación de fragmento en servidor biblioteca
        # (Aquí se conectará la API o la base de datos documental real)
        respuesta_biblioteca = (
            f"📚 **[SERVIDOR BIBLIOTECA - NÚCLEO CONSULTA]**\n"
            f"📁 **Categoría:** {categoria_detectada.upper()}\n"
            f"⚠️ **Nivel/Gravedad:** {nivel.upper()}\n\n"
            f"📖 *Indexando documento de referencia correspondiente a:* '{consulta_usuario}'...\n"
            f"--------------------------------------------------\n"
            f"✅ Protocolo recuperado con éxito desde la base de datos documental."
        )
        
        return respuesta_biblioteca
      
