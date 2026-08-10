import time
import re
import logging
from datetime import datetime

# Configuración del sistema de auditoría y logs de Amiti
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [AMITI-SHIELD]: %(message)s'
)
logger = logging.getLogger("AmitiSecurityCore")

class AmitiAdvancedSecurityShield:
    def __init__(self):
        # Almacenes en memoria para control estricto (Escalable a Redis)
        self.intentos_fallidos = {}  # Estructura: {ip_cliente: [timestamps_de_intentos]}
        self.ips_baneadas = {}       # Estructura: {ip_cliente: timestamp_expiracion_ban}
        
        # Patrones avanzados basados en expresiones regulares (Regex) para detectar contrabando, fraude y hackeos
        self.patrones_prohibidos = [
            re.compile(r'\b(armas?\s+il[ée]gales?|narcot[r|á]fico|drogas?\s+sint[ée]ticas?)\b', re.IGNORECASE),
            re.compile(r'\b(hackear\s+cuenta|robar\s+tarjetas?|phishing\s+masivo|carding|sql\s+injection)\b', re.IGNORECASE),
            re.compile(r'\b(contrabando\s+de\s+armas|falsificaci[oó]n\s+de\s+moneda|trata\s+de\s+blancas?)\b', re.IGNORECASE)
        ]
        
        # Umbrales de seguridad y penalización
        self.MAX_INTENTOS_PERMITIDOS = 5
        self.VENTANA_TIEMPO_SEG = 60      # 1 minuto
        self.TIEMPO_BAN_BASE_SEG = 900    # 15 minutos de baneo inicial

    def auditar_conexion_entrante(self, ip_cliente, user_agent=""):
        """Inspecciona la reputación de la IP y valida la integridad básica del cliente."""
        ahora = time.time()
        
        # 1. Comprobar si la dirección IP se encuentra en la lista negra de baneados
        if ip_cliente in self.ips_baneadas:
            expiracion = self.ips_baneadas[ip_cliente]
            if ahora < expiracion:
                tiempo_restante = int(expiracion - ahora)
                logger.warning(f"Bloqueo activo interceptado para IP hostil: {ip_cliente}. Tiempo restante: {tiempo_restante}s.")
                return False, f"⚠️ [AMITI DEFENSE SYSTEM]: Acceso denegado. Su IP ha sido temporalmente aislada por comportamiento sospechoso. Intente en {tiempo_restante}s."
            else:
                # El tiempo de baneo ha caducado; se limpia la IP
                del self.ips_baneadas[ip_cliente]
                logger.info(f"Baneo expirado para la IP: {ip_cliente}. Restableciendo privilegios.")

        # 2. Validación de huella digital de cliente (User-Agent básico contra bots maliciosos vacíos)
        if not user_agent or len(user_agent.strip()) < 4:
            self.registrar_incidente_hostil(ip_cliente, "Cabecera User-Agent vacía o anómala")
            return False, "⚠️ [AMITI DEFENSE SYSTEM]: Conexión rechazada por falta de identificación válida de cliente."

        return True, "Conexión autorizada"

    def registrar_incidente_hostil(self, ip_cliente, motivo):
        """Registra anomalías y aplica castigos con escalas exponenciales según la gravedad."""
        ahora = time.time()
        
        if ip_cliente not in self.intentos_fallidos:
            self.intentos_fallidos[ip_cliente] = []
        
        # Limpieza de registros fuera de la ventana deslizante de tiempo
        self.intentos_fallidos[ip_cliente] = [t for t in self.intentos_fallidos[ip_cliente] if ahora - t < self.VENTANA_TIEMPO_SEG]
        self.intentos_fallidos[ip_cliente].append(ahora)

        num_incidentes = len(self.intentos_fallidos[ip_cliente])
        logger.warning(f"Incidente registrado en [{ip_cliente}] -> Motivo: {motivo}. Acumulados en ventana: {num_incidentes}")

        # Si se superan los límites permitidos, se activa el baneo escalonado
        if num_incidentes >= self.MAX_INTENTOS_PERMITIDOS:
            # Penalización exponencial: multiplica el tiempo base por el factor de exceso
            factor_multiplicador = (num_incidentes - self.MAX_INTENTOS_PERMITIDOS + 1)
            tiempo_ban_total = self.TIEMPO_BAN_BASE_SEG * factor_multiplicador
            
            self.ips_baneadas[ip_cliente] = ahora + tiempo_ban_total
            logger.error(f"🚨 ALERTA ROJA DE SEGURIDAD: IP {ip_cliente} bloqueada automáticamente por {tiempo_ban_total} segundos debido a ataques continuos.")
            return True
        
        return False

    def blind_scan_mensaje(self, texto_mensaje):
        """Filtro ciego de alta precisión mediante expresiones regulares para la prevención de contrabando y delitos."""
        if not texto_mensaje or not isinstance(texto_mensaje, str):
            return True, "Mensaje vacío validado"

        # Escaneo profundo de patrones de riesgo en el texto
        for patron in self.patrones_prohibidos:
            if patron.search(texto_mensaje):
                logger.warning("Filtro Ciego Amiti: Se ha bloqueado un paquete de texto por coincidencia con protocolos antiterrorismo / antifraude.")
                return False, "⚠️ [AMITI SECURITY CORE]: Mensaje interceptado y purgado. La plataforma prohíbe estrictamente el uso de canales para actividades ilícitas o contrabando."
        
        return True, "Mensaje limpio"
      
