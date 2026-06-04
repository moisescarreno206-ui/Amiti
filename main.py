import time
import requests
import sys

# La URL de tu servidor en Render
URL_SERVIDOR = "https://amiti.onrender.com"  

# Colores (sin espacios extra al principio)
C_BLANCO = "\033[1;37m"
C_AZUL = "\033[1;34m"
C_VERDE = "\033[1;32m"
C_RESET = "\033[0m"

def enviar_alerta_nube(protocolo="EMERGENCIA_ALTA", lat="8.9341", lon="-67.4283"):
    payload = {
        "evento": "DISPARO_PROTOCOLO",
        "protocolo": protocolo,
        "latitud": str(lat),
        "longitud": str(lon),
        "timestamp": time.time()
    }
    
    # Esta línea DEBE estar pegada al margen izquierdo dentro de la función
    headers = {"X-AMITI-KEY": "AMITI_CORE_2026_SUPER_SECRET"}
    
    print(f"\n{C_AZUL}📡 Conectando...{C_RESET}")
    try:
        respuesta = requests.post(URL_SERVIDOR, json=payload, headers=headers, timeout=25)
        if respuesta.status_code == 200:
            print(f"{C_VERDE}✅ [TRANSMISIÓN SEGURA]{C_RESET}")
        else:
            print(f"Error: {respuesta.status_code}")
    except Exception as e:
        print(f"Error: {e}")

# Ejecución simple para probar
if __name__ == "__main__":
    enviar_alerta_nube()
