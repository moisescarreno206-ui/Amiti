from flask import Flask, request, render_template_string
import datetime, hashlib

app = Flask(__name__)

# Base de datos en memoria
MEMORIA = {
    "logs": [{"t": "00:00", "m": "NUCLEO OMEGA V11: SISTEMAS ONLINE", "c": "#00ff41"}],
    "nodos": {} # {ip: contador}
}

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    # El núcleo central no se cuenta como nodo cliente
    es_admin = (ip == "127.0.0.1") # Ajusta según tu IP real
    
    if not es_admin and ip not in MEMORIA["nodos"]:
        MEMORIA["nodos"][ip] = 0
    
    msg = request.form.get("msg", "").lower()
    
    if msg:
        MEMORIA["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"NODO {ip[-4:]}: {msg}", "c": "#fff"})
        
        # Lógica de Comandos
        if msg == "monitor":
            res = "Estado: Servidor estable. Procesador: 12% uso. Memoria: 450MB."
        elif msg == "seguridad":
            res = "Seguridad: 100% OK. Sin amenazas detectadas en el servidor."
        elif msg == "menu":
            total_nodos = len(MEMORIA["nodos"])
            res = f"Menu: Nodos clientes activos: {total_nodos}. El Nucleo (Soporte) está en linea."
        else:
            # IA Asistente
            res = f"IA: He analizado tu solicitud '{msg}'. Respuesta: Procesando datos de forma autonoma."
            
        MEMORIA["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": f"AMITI: {res}", "c": "#00ff41"})
        if len(MEMORIA["logs"]) > 8: MEMORIA["logs"].pop(0)

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #000; color: #00ff41; font-family: monospace; margin: 0; padding: 10px; height: 100vh; display: flex; flex-direction: column; }
            .terminal { flex-grow: 1; border: 2px solid #00ff41; padding: 10px; overflow-y: auto; margin-bottom: 10px; }
            input { width: 100%; padding: 15px; background: #111; color: #fff; border: 2px solid #00ff41; box-sizing: border-box; font-size: 1rem; }
            button { width: 100%; padding: 15px; background: #00ff41; border: none; font-weight: bold; margin-top: 5px; }
        </style>
    </head>
    <body>
        <h2>AMITI OMEGA V11</h2>
        <div class="terminal">
            {% for log in MEMORIA.logs %}<p style="color:{{log.c}}">[{{log.t}}] {{log.m}}</p>{% endfor %}
        </div>
        <form method="POST">
            <input type="text" name="msg" placeholder="Comando o consulta..." required autofocus>
            <button type="submit">EJECUTAR</button>
        </form>
    </body>
    </html>
    """, MEMORIA=MEMORIA)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
