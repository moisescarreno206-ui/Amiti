from flask import Flask, render_template, request, jsonify
from nucleos.n00_nucleo_maestro import amiti

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    data = request.json
    res = amiti.procesar(data.get('comando', ''))
    return jsonify({"respuesta": res})

if __name__ == '__main__':
    app.run()
    
