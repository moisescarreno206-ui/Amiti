import requests
import re
import unicodedata
import urllib.parse

class ModuloInvestigacion:
    """
    =======================================================================
    MÓDULO DE EXTRACCIÓN DE DATOS - PROJECT AMITI OS
    =======================================================================
    Encargado de realizar consultas de información general y especificaciones
    técnicas utilizando la API pública de Wikipedia (Sin necesidad de Keys).
    =======================================================================
    """
    def __init__(self):
        self.nombre = "Módulo de Investigación Amiti"
        self.version = "1.0.0"

    def _normalizar(self, texto):
        """Limpia el texto para detectar los comandos con precisión."""
        texto = texto.lower().strip()
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
        return texto

    def extraer_termino(self, texto):
        """Filtra la instrucción inicial para dejar únicamente el término a buscar."""
        txt = texto.lower()
        patrones = [
            r"investiga sobre\s+", r"investiga\s+", 
            r"busca sobre\s+", r"busca\s+", 
            r"que es\s+(un |una |el |la )?", r"que es\s+", 
            r"quien es\s+", r"consulta sobre\s+", r"consulta\s+"
        ]
        for p in patrones:
            txt = re.sub(p, "", txt, count=1)
        return txt.strip().capitalize()

    def buscar_datos(self, termino):
        if not termino:
            return "⚠️ **[ERROR DE SINTAXIS]** No especificaste qué debo investigar en la red."
        
        try:
            # Conexión a la red de datos pública (Wikipedia API)
            url = f"https://es.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles={urllib.parse.quote(termino)}"
            respuesta = requests.get(url, timeout=5)
            datos = respuesta.json()
            
            paginas = datos.get("query", {}).get("pages", {})
            for page_id, info in paginas.items():
                if page_id == "-1":
                    return f"🌐 **[RED DE DATOS]** No encontré registros exactos en la base de datos pública para: `{termino}`. Intenta usar otro nombre."
                
                extracto = info.get("extract", "").strip()
                if extracto:
                    # Limitamos el texto a 600 caracteres para no desbordar la interfaz de la consola
                    resumen = extracto[:600] + "..." if len(extracto) > 600 else extracto
                    return f"🌐 **[INVESTIGACIÓN COMPLETADA]**\n**Término Extraído:** `{info.get('title')}`\n\n{resumen}"
                
            return "⚠️ **[ERROR DE EXTRACCIÓN]** No pude procesar el texto de la fuente de origen."
        except Exception as e:
            return f"⚠️ **[ALERTA DE CONEXIÓN]** Error al acceder a la red externa: {e}"

    def evaluar_comando(self, mensaje):
        txt = self._normalizar(mensaje)
        
        # Gatillos de investigación
        palabras_investigar = ["busca ", "investiga ", "que es ", "quien es ", "consulta "]
        if any(p in txt for p in palabras_investigar):
            termino = self.extraer_termino(mensaje)
            return self.buscar_datos(termino)
            
        return None

modulo_investigacion = ModuloInvestigacion()
              
