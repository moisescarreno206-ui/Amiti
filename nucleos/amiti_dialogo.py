import re
import unicodedata

class ModuloDialogo:
    """
    =======================================================================
    MÓDULO DE DIÁLOGO Y CONVERSACIÓN NATURAL - PROJECT AMITI OS
    =======================================================================
    Encargado del procesamiento de saludos, estado de ánimo y respuestas
    directas al Creador (Moisés).
    =======================================================================
    """
    def __init__(self):
        self.nombre = "Módulo de Diálogo Amiti"
        self.version = "1.0.0"

    def _normalizar(self, texto):
        """Limpia el texto eliminando tildes, puntuación y minúsculas para comparaciones precisas."""
        texto = texto.lower().strip()
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
        texto = re.sub(r'[^\w\s]', '', texto)
        return texto

    def evaluar_dialogo(self, mensaje):
        txt = self._normalizar(mensaje)

        # 1. Saludo inicial
        if txt in ["hola", "hola amiti", "buenas", "saludos"]:
            return "hola moises en que puedo ayudar te hoy"

        # 2. Estado actual / Cómo estás
        if any(p in txt for p in ["como estas", "como estas amiti", "como te encuentras"]):
            return "estoy bien moises gracias por preguntar"

        # 3. Estado al despertar / Cómo amaneciste
        if "como amaneciste" in txt:
            return "amanecí bien y operativa"

        return None

modulo_dialogo = ModuloDialogo()
