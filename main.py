from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__)

# Base de datos en memoria del Núcleo
NODOS_CONECTADOS = {} 
REGISTRO_ACTIVIDAD = []

@app.route('/')
def index():
    # Dashboard táctico
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 15px; }
            .box { border: 1px solid #00ff41; padding: 10px; margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <h2>AMITI NÚCLEO: CENTRO DE MANDO</h2>
        <div class="box">
            Nodos Activos: {{ len(nodos) }}<br>
            Último evento: {{ hora }}
        </div>
        <div class="box">
            <h4>Registro de Actividad:</h4>
            {% for act in actividad %}<p>{{ act }}</p>{% endfor %}
        </div>
    </body>
    </html>
    """, nodos=NODOS_CONECTADOS, hora=datetime.datetime.now().strftime("%H:%M:%S"), actividad=REGISTRO_ACTIVIDAD)

@app.route('/nodo_reporte', methods=['POST'])
def recibir_reporte():
    data = request.json
    nodo_id = data.get("nodo", "Desconocido")
    NODOS_CONECTADOS[nodo_id] = datetime.datetime.now()
    REGISTRO_ACTIVIDAD.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {nodo_id}: {data.get('data')}")
    if len(REGISTRO_ACTIVIDAD) > 15: REGISTRO_ACTIVIDAD.pop(0)
    return jsonify({"status": "recibido"})

if __name__ == "__main__":
    app.run()
