import time
import re
from collections import defaultdict

class AmitiFirewall:
    """
    Cortafuegos de Seguridad para Amiti OS y su Red Social.
    Filtra firmas maliciosas, ataques de fuerza bruta, XSS, SQLi y DDoS.
    """
    def __init__(self, max_requests_per_minute=60):
        self.max_rpm = max_requests_per_minute
        self.solicitudes_ip = defaultdict(list)
        self.ips_bloqueadas = set()
        
        # Patrones de ataque conocidos (SQLi, XSS, Path Traversal, Command Injection)
        self.patrones_sospechosos = [
            r"(?i)(UNION\s+SELECT|SELECT\s+.*\s+FROM|INSERT\s+INTO|DROP\s+TABLE|DELETE\s+FROM)",
            r"(?i)(<script.*?>|javascript:|onload\s*=|onerror\s*=)",
            r"(\.\./\.\./|\.\.\\\.\.\\)",
            r"(?i)(exec\s*\(|eval\s*\(|passthru\s*\(|system\s*\()"
        ]

    def es_ip_bloqueada(self, ip):
        return ip in self.ips_bloqueadas

    def evaluar_rate_limit(self, ip):
        ahora = time.time()
        # Limpiar solicitudes de más de 60 segundos
        self.solicitudes_ip[ip] = [t for t in self.solicitudes_ip[ip] if ahora - t < 60]
        self.solicitudes_ip[ip].append(ahora)
        
        if len(self.solicitudes_ip[ip]) > self.max_rpm:
            self.ips_bloqueadas.add(ip)
            return False
        return True

    def inspeccionar_contenido(self, texto):
        if not texto:
            return True
        for patron in self.patrones_sospechosos:
            if re.search(patron, str(texto)):
                return False
        return True

    def auditar_peticion(self, ip, user_agent, datos_peticion=None):
        """
        Método principal de validación para cada solicitud entrante.
        Returns: (permitido: bool, motivo: str)
        """
        if self.es_ip_bloqueada(ip):
            return False, "IP bloqueada temporalmente por actividad sospechosa."

        if not self.evaluar_rate_limit(ip):
            return False, "Tasa límite excedida (Límite de solicitudes alcanzado)."

        if datos_peticion:
            if not self.inspeccionar_contenido(datos_peticion):
                self.ips_bloqueadas.add(ip)
                return False, "Intento de inyección o payload malicioso detectado."

        return True, "Petición autorizada."
      
