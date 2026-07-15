from flask import Flask, jsonify, request
from nucleos.n00_nucleo_maestro import amiti

app = Flask(__name__)

@app.route('/estado', methods=['GET'])
def estado():
    return jsonify({
        "minutos_inteligencia": amiti.obtener_minutos_inteligencia(),
        "errores_pendientes": len(amiti.errores),
        "status": "OPERATIVO"
    })

# ... el resto de tus rutas ...
