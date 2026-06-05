from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__)

# Base de datos en memoria del Núcleo
NODOS_CONECTADOS = {} # {id_nodo: ultima_conexion}
REGISTRO_ACTIVIDAD = []

# --- INTERFAZ DEL NÚCLEO (Dashboard de Monitoreo) ---
@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 15px; }
            .box { border: 1px solid #00ff41; padding: 10px; margin-bottom: 10px; }
            textarea { width: 100%; height: 100px; background: #000; color: #00ff41; border: 1px solid #00ff41; }
            button { background: #00ff41; color: #000; border: none; padding: 10px; width: 100%; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2>AMITI NÚCLEO: CENTRO DE MANDO</h2>
        <div class="box">
            Nodos Activos: {{ len(nodos) }}<br>
            Último evento: {{ hora }}
        </div>
        <div class="box" id="log">
            {% for act in actividad %}{{ act }}<br>{% endfor %}
        </div>
        <textarea id="codigo" placeholder="Pegar código de actualización..."></textarea>
        <button onclick="enviarActualizacion()">DESPLEGAR ACTUALIZACIÓN A NODOS</button>
        <script>
            async function enviarActualizacion(){
                let c = document.getElementById('codigo').value;
                alert("Desplegando actualización a la red...");
            }
        </script>
    </body>
    """, nodos=NODOS_CONECTADOS, hora=datetime.datetime.now().strftime("%H:%M:%S"), actividad=REGISTRO_ACTIVIDAD)

# --- RECEPTOR DE INFORMACIÓN DE NODOS ---
@app.route('/nodo_reporte', methods=['POST'])
def recibir_reporte():
    data = request.json
    nodo_id = data.get("nodo", "Desconocido")
    NODOS_CONECTADOS[nodo_id] = datetime.datetime.now()
    REGISTRO_ACTIVIDAD.append(f"[{nodo_id}] {data.get('data')}")
    if len(REGISTRO_ACTIVIDAD) > 10: REGISTRO_ACTIVIDAD.pop(0)
    return jsonify({"status": "recibido"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
