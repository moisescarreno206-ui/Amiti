from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__)

# Base de datos en memoria
NODOS_CONECTADOS = {} 
REGISTRO_ACTIVIDAD = []

@app.route('/', methods=['GET'])
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 15px; }
            .box { border: 1px solid #00ff41; padding: 10px; margin-bottom: 10px; }
            .blue { color: #00aaff; }
            .purple { color: #aa00ff; }
        </style>
    </head>
    <body>
        <h2>AMITI NÚCLEO: CENTRO DE MANDO</h2>
        <div class="box">Nodos Activos: {{ len(nodos) }}</div>
        <div class="box">
            <h4>Registro de Actividad:</h4>
            {% for act in actividad %}
                <p class="{{act.color}}">[{{act.time}}] {{act.msg}}</p>
            {% endfor %}
        </div>
    </body>
    </html>
    """, nodos=NODOS_CONECTADOS, actividad=REGISTRO_ACTIVIDAD)

@app.route('/nodo_reporte', methods=['POST'])
def recibir_reporte():
    data = request.json
    msg = str(data.get('data', ''))
    
    # Clasificación de colores
    color = "green"
    if any(x in msg.lower() for x in ["cuanto", "+", "-", "*", "/"]): color = "blue"
    elif any(x in msg.lower() for x in ["contabilidad", "saldo", "pago"]): color = "purple"
    
    REGISTRO_ACTIVIDAD.append({
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "msg": msg,
        "color": color
    })
    if len(REGISTRO_ACTIVIDAD) > 15: REGISTRO_ACTIVIDAD.pop(0)
    return jsonify({"status": "recibido"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
