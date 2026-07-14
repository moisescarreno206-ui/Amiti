
from flask import Flask, request, jsonify, render_template
from nucleos.n00_nucleo_maestro import amiti

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    # POST es más seguro y eficiente para transmitir datos
    data = request.json
    comando = data.get('comando', '')
    return jsonify({"status": "ok", "respuesta": amiti.procesar(comando)})

if __name__ == '__main__':
    app.run()
  
