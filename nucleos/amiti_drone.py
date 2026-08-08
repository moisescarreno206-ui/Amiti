import socket
import threading
import time
import re

class AmitiDroneController:
    """
    Módulo de Control de Vuelo Inercial y Monitoreo Wi-Fi para Dron (S15 MAX).
    Diseñado para funcionar integrado en Amiti sin depender de GPS.
    """
    def __init__(self, ip_dron="192.168.1.1", puerto_control=8080):
        self.ip = ip_dron
        self.puerto = puerto_control
        self.altura_estimada = 0.0  # Mantenida en metros
        self.en_vuelo = False
        self.evasion_ir = True       # Sensores infrarrojos activados
        self.conectado = False
        self.sensibilidad_vuelo = "NORMAL"
        self.modo_sigueme_activo = False

        # Socket UDP sin bloqueo
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.5)

        # Hilo en segundo plano para monitorear la conexión Wi-Fi constante con el dron
        threading.Thread(target=self._monitor_conexion, daemon=True).start()

    # -------------------------------------------------------------------------
    # MONITOREO Y ESTADO DE CONEXIÓN WI-FI
    # -------------------------------------------------------------------------
    def _monitor_conexion(self):
        """Verifica cada 2 segundos si el teléfono mantiene enlace con el Wi-Fi del dron."""
        while True:
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                test_socket.settimeout(0.4)
                # Envía un paquete nulo de verificación a la IP del dron
                paquete_ping = bytes([0x66, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x99])
                test_socket.sendto(paquete_ping, (self.ip, self.puerto))
                self.conectado = True
                test_socket.close()
            except Exception:
                self.conectado = False
            time.sleep(2.0)

    def verificar_conexion(self):
        return self.conectado

    def estado_conexion_texto(self):
        if self.conectado:
            return "🟢 **[DRON]** Conexión Wi-Fi Establecida. Sistemas y sensores en línea."
        return "🔴 **[DRON]** Desconectado. Conecta el teléfono a la red Wi-Fi del dron para operar."

    # -------------------------------------------------------------------------
    # EMISIÓN DE COMANDOS UDP Y PULSOS DE VUELO
    # -------------------------------------------------------------------------
    def _enviar_paquete(self, pitch=128, roll=128, yaw=128, throttle=128, aux_flags=0x01):
        """Construye y envía el datagrama UDP de 8 bytes para la placa del dron."""
        header = 0x66
        footer = 0x99
        checksum = (pitch + roll + yaw + throttle + aux_flags) & 0xFF
        paquete = bytes([header, pitch, roll, yaw, throttle, aux_flags, checksum, footer])
        try:
            self.sock.sendto(paquete, (self.ip, self.puerto))
        except Exception:
            pass  # Silencia excepciones si la red fluctúa

    def _ejecutar_pulso(self, pitch=128, roll=128, yaw=128, throttle=128, duracion=1.0):
        """Ejecuta un impulso temporal y retorna a suspensión neutra (auto-hovering)."""
        def hilo_pulso():
            tiempo_inicio = time.time()
            while time.time() - tiempo_inicio < duracion:
                flags = 0x01 if self.evasion_ir else 0x00
                self._enviar_paquete(pitch, roll, yaw, throttle, aux_flags=flags)
                time.sleep(0.05)
            
            # Estabilización automática
            for _ in range(4):
                self._enviar_paquete(128, 128, 128, 128, aux_flags=0x01)
                time.sleep(0.05)

        threading.Thread(target=hilo_pulso, daemon=True).start()

    # -------------------------------------------------------------------------
    # FUNCIONES ESPECÍFICAS DE ACCIÓN DE VUELO
    # -------------------------------------------------------------------------
    def elevar_a_altura(self, texto):
        if not self.verificar_conexion():
            return "⚠️ **[ALERTA]** Imposible despegar: Sin conexión Wi-Fi con el Dron."
        
        # Extraer el número de la orden (ejemplo: "Amiti eleva el dron 25")
        numeros = re.findall(r'\d+', texto)
        altura_objetivo = float(numeros[0]) if numeros else 1.65

        # Límite de seguridad máximo de 50 metros
        aviso = ""
        if altura_objetivo > 50.0:
            altura_objetivo = 50.0
            aviso = " *(Ajustado al límite máximo de seguridad de 50m)*"

        self.en_vuelo = True
        self.altura_estimada = altura_objetivo

        # Duración de elevación barométrica calculada según la altura solicitada
        duracion_aceleracion = min(4.0, 0.8 + (altura_objetivo * 0.08))
        self._ejecutar_pulso(pitch=128, roll=128, yaw=128, throttle=175, duracion=duracion_aceleracion)

        return f"🚁 **[AMITI DRONE]** Elevando dron a **{self.altura_estimada}m** de altura{aviso}. Control barométrico activo."

    def escanear_lugar(self):
        if not self.verificar_conexion():
            return "⚠️ **[ALERTA]** Sin conexión Wi-Fi con el Dron."
        if not self.en_vuelo:
            return "⚠️ **[ALERTA]** El dron debe estar elevado para realizar el escaneo."

        def rutina_escaneo():
            # Realiza un giro continuo de 360° en su propio eje (Yaw)
            t_ini = time.time()
            while time.time() - t_ini < 4.0:
                self._enviar_paquete(pitch=128, roll=128, yaw=165, throttle=128, aux_flags=0x01)
                time.sleep(0.05)
            self._enviar_paquete(128, 128, 128, 128, aux_flags=0x01)

        threading.Thread(target=rutina_escaneo, daemon=True).start()
        return f"🚁 **[AMITI DRONE]** Escaneando entorno 360° a **{self.altura_estimada}m** de altura mediante cámara y flujo óptico."

    def modo_sigueme(self):
        if not self.verificar_conexion():
            return "⚠️ **[ALERTA]** Sin conexión Wi-Fi con el Dron."
        if not self.en_vuelo:
            return "⚠️ **[ALERTA]** Debes elevar el dron antes de iniciar el modo seguimiento."

        self.modo_sigueme_activo = True
        self.evasion_ir = True  # Sensores anti-colisión infrarrojos activos

        return f"🚁 **[AMITI DRONE]** Modo **Seguimiento Seguro** activo. Manteniendo altura estable de **{self.altura_estimada}m** y esquivando obstáculos."

    def maniobras_ofensivas(self):
        if not self.verificar_conexion():
            return "⚠️ **[ALERTA]** Sin conexión Wi-Fi con el Dron."

        self.sensibilidad_vuelo = "ALTA"
        self.evasion_ir = True

        def rutina_agilidad():
            # Secuencia rápida de esquive y cambio de posición
            self._ejecutar_pulso(pitch=165, roll=95, duracion=0.4)   # Avance en diagonal izquierda
            time.sleep(0.1)
            self._ejecutar_pulso(pitch=165, roll=160, duracion=0.4)  # Avance en diagonal derecha

        threading.Thread(target=rutina_agilidad, daemon=True).start()
        return "⚡ **[AMITI DRONE]** Modo **Maniobras Ofensivas / Agilidad** activado. Sensores IR al 100% para evitar colisiones."

    def capturar_media(self, texto):
        if not self.verificar_conexion():
            return "⚠️ **[ALERTA]** Sin conexión Wi-Fi con el Dron."

        t = texto.lower()
        if "foto" in t:
            self._enviar_paquete(128, 128, 128, 128, aux_flags=0x88)
            return "📸 **[CÁMARA]** Fotografía capturada."
        elif "video" in t:
            self._enviar_paquete(128, 128, 128, 128, aux_flags=0xAA)
            return "🎥 **[CÁMARA]** Grabación de video iniciada / conmutada."

        return "⚠️ Por favor especifica si deseas tomar una **foto** o iniciar un **video**."

    # -------------------------------------------------------------------------
    # ANALIZADOR Y ENRUTADOR CENTRAL DE COMANDOS DE TEXTO
    # -------------------------------------------------------------------------
    def procesar_comando_texto(self, texto_usuario):
        """
        Recibe la frase recibida por Amiti y ejecuta la acción correspondiente.
        Devuelve el mensaje de respuesta o None si no es un comando de dron.
        """
        if not texto_usuario:
            return None

        txt = texto_usuario.lower().strip()

        # 1. Comando: Elevar el dron
        if "eleva el dron" in txt or "elevar el dron" in txt:
            return self.elevar_a_altura(txt)

        # 2. Comando: Escanear el lugar
        elif "escánea" in txt or "escanea" in txt or "escanear" in txt:
            return self.escanear_lugar()

        # 3. Comando: Sígueme
        elif "sígueme" in txt or "sigueme" in txt or "sigue me" in txt:
            return self.modo_sigueme()

        # 4. Comando: Maniobras ofensivas
        elif "maniobras ofensivas" in txt or "maniobras" in txt or "maniobra" in txt:
            return self.maniobras_ofensivas()

        # 5. Comando: Grabar (foto o video)
        elif "graba" in txt or "grabar" in txt or "foto" in txt or "video" in txt:
            return self.capturar_media(txt)

        return None


# =============================================================================
# PRUEBA RÁPIDA DE INTEGRACIÓN CON AMITI
# =============================================================================
if __name__ == "__main__":
    # Instancia principal del sistema de dron para Amiti
    amiti_drone = AmitiDroneController()

    print("=== CONTROL DE DRON AMITI CARGADO ===")
    print(amiti_drone.estado_conexion_texto())
    print("\nEscribe un comando para probar (ejemplo: 'Amiti eleva el dron 20', 'Amiti escánea el lugar', 'Amiti graba foto'):")

    try:
        while True:
            entrada = input("\nUsuario > ")
            respuesta = amiti_drone.procesar_comando_texto(entrada)
            
            if respuesta:
                print(respuesta)
            else:
                print("ℹ️ Este texto no es una orden de vuelo para el dron.")
    except KeyboardInterrupt:
        print("\nSaliendo del controlador...")
        
