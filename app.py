from flask import Flask, render_template, request, jsonify
from nucleos.n00_nucleo_maestro import amiti

app = Flask(__name__)

@app.route('/')
def home(): return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    data = request.json
    comando = data.get('comando', '')
    return jsonify({"respuesta": amiti.procesar(comando)})

@app.route('/memoria')
def ver_memoria():
    with open("memoria_amiti.txt", "r") as f:
        return f.read().replace("\n", "<br>")

if __name__ == '__main__':
    app.run()
    
