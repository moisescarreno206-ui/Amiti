# main.py - El Casco Central
import time, threading
from flask import Flask
import modulo_memoria as cerebro 

app = Flask(__name__)

# AMITI despierta en un hilo separado para poder hablarte por iniciativa propia
def bucle_autonomo():
    while True:
        time.sleep(60) # AMITI piensa cada minuto
        if cerebro.necesita_saludar():
            cerebro.enviar_saludo_iniciativa()

# Iniciar el hilo de pensamiento paralelo
threading.Thread(target=bucle_autonomo, daemon=True).start()

@app.route('/')
def index():
    return "NUCLEO CENTRAL ONLINE - CASCO ACTIVO"

if __name__ == "__main__":
    app.run(port=10000)
    
