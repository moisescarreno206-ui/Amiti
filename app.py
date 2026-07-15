from flask import Flask, render_template, request, jsonify
# La importación debe ser relativa a la carpeta nucleos
from nucleos.n00_nucleo_maestro import amiti

app = Flask(__name__)

@app.route('/')
def home():
    # Asegúrate de que index.html esté dentro de la carpeta 'templates'
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    data = request.json
    comando = data.get('comando', '')
    return jsonify({"respuesta": amiti.procesar(comando)})

if __name__ == '__main__':
    app.run()
    
