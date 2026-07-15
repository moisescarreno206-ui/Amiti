from flask import Flask, render_template, request, jsonify
# La ruta correcta es nucleos.n00_nucleo_maestro
from nucleos.n00_nucleo_maestro import amiti

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
# ... resto de tu código ...
