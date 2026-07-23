import os
import requests

class NotificadorTelegram:
    """Módulo para emisión de alertas reales a dispositivos móviles"""
    def __init__(self):
        # Obtenemos los credenciales desde las variables de entorno de Render
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    def enviar_alerta(self, mensaje):
        """Envía un mensaje directo al teléfono del Creador"""
        if not self.bot_token or not self.chat_id:
            return "⚠️ [ALERTA NO ENVIADA] Falta configurar TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID."

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": mensaje,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                return "🚀 **[ACCION REAL EJECUTADA]** Alerta enviada con éxito a tu dispositivo."
            else:
                return f"❌ Error de API Telegram ({response.status_code}): {response.text}"
        except Exception as e:
            return f"❌ Fallo de red al conectar con Telegram: {e}"

notificador = NotificadorTelegram()
