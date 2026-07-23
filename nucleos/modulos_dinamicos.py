import ast
import hashlib
import datetime

def validar_codigo_python(codigo):
    """ Módulo dinámico """
    try:
        ast.parse(codigo)
        return True
    except SyntaxError:
        return False

# --- Inyección v6.9.0 ---
def verificar_modulo_v2(): 
    return "Módulo acumulativo activo y listo"

# --- Inyección v6.10.0 ---
def investigar_web_amiti(query): 
    import urllib.parse, requests
    r = requests.get(f"https://es.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}")
    return r.json().get("extract", "Sin información")

# --- Inyección v6.12.0 ---
def test_nucleo(): 
    return "Núcleo dinámico respondiendo en tiempo real"

# --- Inyección v6.13.0 ---
def funcion_b64():
    return "Base64 funcionando correctamente"

# --- Inyección v6.14.0 (Módulo de Telemetría y Seguridad) ---
class TelemetriaYEmergencia:
    def __init__(self):
        self.modo_emergencia = False
        self.motivo_bloqueo = ""
        self.logs = []

    def registrar_evento(self, evento, nivel="INFO"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registro = {"timestamp": timestamp, "nivel": nivel.upper(), "mensaje": str(evento)}
        self.logs.append(registro)
        if len(self.logs) > 100: 
            self.logs.pop(0)
        return f"📌 [{timestamp}] [{nivel.upper()}] {evento}"

    def activar_emergencia(self, motivo="Activación manual de seguridad"):
        self.modo_emergencia = True
        self.motivo_bloqueo = motivo
        self.registrar_evento(f"EMERGENCIA ACTIVADA: {motivo}", nivel="CRITICAL")
        return f"🚨 **[KILLSWITCH ACTIVADO]** Motivo: {motivo}"

    def desactivar_emergencia(self):
        self.modo_emergencia = False
        self.motivo_bloqueo = ""
        self.registrar_evento("Emergencia desactivada.", nivel="INFO")
        return "✅ **[SISTEMA RESTABLECIDO]** Operación normal."

    def obtener_telemetria(self):
        if not self.logs: 
            return "📊 **[TELEMETRÍA]** Sin eventos registrados."
        reporte = "📊 **[ÚLTIMOS EVENTOS DE RASTREO]**\n"
        for log in self.logs[-5:]:
            reporte += f"┣ `[{log['timestamp']}]` **[{log['nivel']}]**: {log['mensaje']}\n"
        return reporte

# --- Inyección v6.15.0 (Cifrado y Salud) ---
class ProteccionDatos:
    """Módulo de Hash e Integridad de Datos Criptográfica"""
    def generar_hash(self, texto):
        return hashlib.sha256(texto.encode('utf-8')).hexdigest()

class SaludYPrimerosAuxilios:
    """Módulo de Triaje Médico y Guía de Emergencia"""
    def __init__(self):
        self.protocolos = {
            "quemadura": "1. Enfriar con agua corriente (no helada) por 10-15 min. 2. No reventar ampollas. 3. Cubrir con gasa limpia.",
            "corte": "1. Hacer presión firme con compresa o paño limpio. 2. Lavar con agua y jabón. 3. Elevar la zona afectada.",
            "asfixia": "1. Verificar si la persona puede hablar o toser. 2. Aplicar Maniobra de Heimlich si la vía aérea está obstruida.",
            "golpe": "1. Aplicar frío local intermitente. 2. Monitorear si hay mareos, náuseas o pérdida de conciencia."
        }

    def evaluar_triaje(self, sintomas):
        sintomas_l = sintomas.lower()
        if any(p in sintomas_l for p in ["dolor de pecho", "falta de aire", "inconsciente", "hemorragia"]):
            return "🚨 **[TRIAJE CRÍTICO - ALERTA ROJA]** Síntomas graves detectados. Requiere atención médica inmediata."
        elif any(p in sintomas_l for p in ["fiebre alta", "corte profundo", "quemadura", "fractura"]):
            return "⚠️ **[TRIAJE URGENTE - ALERTA AMARILLA]** Requiere atención médica prioritaria o aplicación inmediata de primeros auxilios."
        else:
            return "🟢 **[TRIAJE LEVE - ALERTA VERDE]** Sintomatología menor. Mantener observación y reposo."

    def consultar_protocolo(self, condicion):
        condicion_l = condicion.lower()
        for clave, guia in self.protocolos.items():
            if clave in condicion_l:
                return f"🩺 **[GUÍA DE PRIMEROS AUXILIOS: {clave.upper()}]**\n{guia}"
        return "🩺 **[CONSULTA MÉDICA]** Para esa sintomatología específica, se recomienda evaluación médica presencial."

# Instancias globales
modulo_seguridad = TelemetriaYEmergencia()
modulo_proteccion = ProteccionDatos()
modulo_salud = SaludYPrimerosAuxilios()
