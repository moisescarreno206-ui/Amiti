from flask import Flask, render_template, request, jsonify
# Importamos la instancia 'amiti' que definimos en el núcleo
from nucleos.n00_nucleo_maestro import amiti

app = Flask(__name__)

# Ruta para cargar la interfaz web
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para procesar comandos desde la web
@app.route('/procesar', methods=['POST'])
def procesar():
    # Recibimos el comando enviado por el usuario
    data = request.json
    comando = data.get('comando', '')
    
    # Enviamos el comando al núcleo maestro
    respuesta = amiti.procesar(comando)
    
    return jsonify({"respuesta": respuesta})

if __name__ == '__main__':
    # Render se encarga del puerto, así que no es necesario especificarlo
    app.run()
  
