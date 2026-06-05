from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# Interfaz HTML sencilla para tu App
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>AMITI OMEGA</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #000; color: #0f0; padding: 20px; }
        #chat { height: 300px; border: 1px solid #0f0; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        input { width: 70%; padding: 10px; }
        button { padding: 10px; background: #0f0; border: none; }
    </style>
</head>
<body>
    <h3>AMITI OMEGA VIGILANTE</h3>
    <div id="chat"></div>
    <input type="text" id="msg" placeholder="Escribe un comando...">
    <button onclick="enviar()">Enviar</button>

    <script>
        function enviar() {
            let msg = document.getElementById('msg').value;
            document.getElementById('chat').innerHTML += '<p>Yo: ' + msg + '</p>';
            document.getElementById('chat').innerHTML += '<p>AMITI: Procesando comando...</p>';
            document.getElementById('msg').value = '';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_INTERFACE)

@app.route('/favicon.ico')
def favicon():
    return "", 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
