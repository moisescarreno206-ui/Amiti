import datetime
import requests
import re
import unicodedata

class ModuloClimaTiempo:
    """
    =======================================================================
    MÓDULO DE CLIMA Y TIEMPO - PROJECT AMITI OS
    =======================================================================
    Encargado de predecir el clima, temperatura y proveer datos exactos de
    día, semana, mes y año usando datos en tiempo real.
    =======================================================================
    """
    def __init__(self):
        self.nombre = "Módulo de Clima y Tiempo Amiti"
        self.version = "1.0.0"
        # Coordenadas base configuradas directamente en el núcleo
        self.latitud = 8.9242
        self.longitud = -67.4293
        self.timezone = "America/Caracas"

    def _normalizar(self, texto):
        """Limpia el texto para comparaciones precisas."""
        texto = texto.lower().strip()
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
        texto = re.sub(r'[^\w\s]', '', texto)
        return texto
        
    def obtener_fecha_hora(self):
        ahora = datetime.datetime.now()
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        
        dia_semana = dias[ahora.weekday()]
        dia = ahora.day
        mes = meses[ahora.month - 1]
        ano = ahora.year
        hora = ahora.strftime("%I:%M %p")
        semana_ano = ahora.isocalendar()[1]
        
        return f"📅 **[CRONOMETRÍA AMITI]**\nHoy es {dia_semana}, {dia} de {mes} de {ano}.\nEstamos en la semana {semana_ano} del año.\nLa hora actual es {hora}."

    def obtener_clima(self):
        try:
            # Conexión a la API meteorológica (Sin necesidad de Key)
            url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitud}&longitude={self.longitud}&current_weather=true&timezone={self.timezone}"
            respuesta = requests.get(url, timeout=5)
            datos = respuesta.json()
            
            if "current_weather" in datos:
                clima = datos["current_weather"]
                temp = clima["temperature"]
                codigo = clima["weathercode"]
                
                # Interpretación de la telemetría WMO
                estado = "Despejado ☀️"
                if codigo in [1, 2, 3]: estado = "Parcialmente nublado ⛅"
                elif codigo in [45, 48]: estado = "Con niebla 🌫️"
                elif codigo in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]: estado = "Lluvioso 🌧️"
                elif codigo in [71, 73, 75, 77, 85, 86]: estado = "Con nieve ❄️"
                elif codigo in [95, 96, 99]: estado = "Con tormenta eléctrica 🌩️"
                
                return f"🌡️ **[REPORTE CLIMÁTICO]**\nLa temperatura actual registrada es de **{temp}°C**, y el estado del clima es: **{estado}**."
            else:
                return "⚠️ **[ERROR]** No pude procesar los datos climáticos en este momento."
        except Exception as e:
            return f"⚠️ **[ALERTA DE SENSORES]** Error de conexión con el satélite meteorológico: {e}"

    def evaluar_comando(self, mensaje):
        txt = self._normalizar(mensaje)
        
        # Gatillos para fecha, día, hora, año, semanas
        palabras_tiempo = ["que dia es", "fecha", "que hora es", "en que mes", "en que ano", "semana del ano", "que dia es hoy", "dime la fecha"]
        if any(p in txt for p in palabras_tiempo):
            return self.obtener_fecha_hora()
            
        # Gatillos para clima y temperatura
        palabras_clima = ["clima", "temperatura", "va a llover", "como esta el tiempo", "que clima hace"]
        if any(p in txt for p in palabras_clima):
            return self.obtener_clima()
            
        return None

modulo_clima = ModuloClimaTiempo()
          
