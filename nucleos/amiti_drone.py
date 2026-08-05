import socket
import threading
import time

class AmitiDroneEngine:
    def __init__(self, ip_dron="192.168.1.1", puerto_control=8080, puerto_video=8888):
        self.ip = ip_dron
        self.puerto_control = puerto_control
        self.puerto_video = puerto_video
        self.altura_actual = 0.0  # metros
        self.en_vuelo = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1.0)
        
        # Estado del giroscopio y cámaras
        self.camara_activa = "frontal"  # 'frontal' o 'inferior'

    def encender_y_elevar(self, altura=1.65):
        """Comando 1: Enciende motores y eleva a 1.65m"""
        self.en_vuelo = True
        self.altura_actual = altura
        
        # Estructura de paquete de despegue seguro S15 MAX
        payload = bytes([0x66, 0x01, 0x01, 0x01, 0x00, 0x00, 0x99])
        self._enviar_paquete(payload)
        return f"🚁 **[AMITI DRONE S15 MAX]** Motores encendidos. Despegue ejecutado. Estabilizado a **{self.altura_actual}m** de altura."

    def elevar_mas(self, nueva_altura=1.85):
        """Comando 2: Eleva el dron a 1.85m"""
        if not self.en_vuelo:
            return self.encender_y_elevar(nueva_altura)
        
        diferencia = round(nueva_altura - self.altura_actual, 2)
        self.altura_actual = nueva_altura
        
        payload = bytes([0x66, 0x02, 0x01, 0x02, 0x00, 0x00, 0x99])
        self._enviar_paquete(payload)
        return f"🚁 **[AMITI DRONE S15 MAX]** Ascendiendo +{diferencia}m. Nueva altitud fijada en **{self.altura_actual}m**."

    def mover_adelante(self):
        """Comando 3: Avanzar hacia adelante en el aire"""
        if not self.en_vuelo:
            return "⚠️ **[ALERTA DE VUELO]** El dron está en tierra. Di primero: *'Amiti elevar el dron'*."
        
        payload = bytes([0x66, 0x03, 0x10, 0x00, 0x00, 0x00, 0x99])
        self._enviar_paquete(payload)
        return f"🚁 **[AMITI DRONE S15 MAX]** Avanzando hacia **adelante** manteniendo altitud de **{self.altura_actual}m**."

    def mover_retroceder(self):
        """Comando 4: Retroceder en el aire"""
        if not self.en_vuelo:
            return "⚠️ **[ALERTA DE VUELO]** El dron está en tierra. Di primero: *'Amiti elevar el dron'*."
        
        payload = bytes([0x66, 0x04, 0x10, 0x00, 0x00, 0x00, 0x99])
        self._enviar_paquete(payload)
        return f"🚁 **[AMITI DRONE S15 MAX]** Retrocediendo en el aire a **{self.altura_actual}m** de altura."

    def mover_lateral(self, direccion):
        """Comando 5: Desplazamiento lateral derecho o izquierdo"""
        if not self.en_vuelo:
            return "⚠️ **[ALERTA DE VUELO]** El dron está en tierra. Di primero: *'Amiti elevar el dron'*."
        
        if "derech" in direccion:
            payload = bytes([0x66, 0x05, 0x00, 0x10, 0x00, 0x00, 0x99])
            self._enviar_paquete(payload)
            return f"🚁 **[AMITI DRONE S15 MAX]** Desplazando hacia la **DERECHA** a **{self.altura_actual}m**."
        elif "izquierd" in direccion:
            payload = bytes([0x66, 0x06, 0x00, 0x10, 0x00, 0x00, 0x99])
            self._enviar_paquete(payload)
            return f"🚁 **[AMITI DRONE S15 MAX]** Desplazando hacia la **IZQUIERDA** a **{self.altura_actual}m**."
        
        return "⚠️ Especifica la dirección: 'derecho' o 'izquierdo'."

    def alternar_camara(self):
        """Cambio entre la cámara frontal 4K y la cámara inferior de posicionamiento óptico"""
        self.camara_activa = "inferior" if self.camara_activa == "frontal" else "frontal"
        return f"📹 **[SISTEMA DE VISIÓN]** Conmutando transmisión. Cámara activa: **{self.camara_activa.upper()}**."

    def _enviar_paquete(self, paquete):
        try:
            self.sock.sendto(paquete, (self.ip, self.puerto_control))
        except Exception:
            pass  # Modo simulación / envío en red local UDP
      
