from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# Interfaz con lógica de respuesta integrada
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>AMITI OMEGA</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: monospace; background: #000; color: #0f0; padding: 15px; }
        #chat { height: 350px; border: 1px solid #0f0; overflow-y: scroll; padding: 10px; margin-bottom: 10px; font-size: 14px; }
        input { width: 65%; padding: 10px; background: #111; color: #0f0; border: 1px solid #0f0; }
        button { padding: 10px; background: #0f0; color: #000; border: none; font-weight: bold; }
    </style>
</head>
<body>
    <h3>AMITI OMEGA VIGILANTE</h3>
    <div id="chat"></div>
    <input type="text" id="msg" placeholder="Comando...">
    <button onclick="enviar()">Enviar</button>

    <script>
        async function enviar() {
            let input = document.getElementById('msg');
            let chat = document.getElementById('chat');
            let msg = input.value;
            if(!msg) return;
            
            chat.innerHTML += '<p>> ' + msg + '</p>';
            input.value = '';
            
            let response = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({comando: msg})
            });
            let data = await response.json();
            chat.innerHTML += '<p style="color: #fff;">AMITI: ' + data.respuesta + '</p>';
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_INTERFACE)

@app.route('/chat', methods=['POST'])
def chat():
    comando = request.json.get("comando", "").lower()
    # Lógica de respuesta de la IA
    if "estado" in comando: respuesta = "SISTEMA OMEGA: Operativo. Defensas activas."
    elif "consejo" in comando: respuesta = "Mantén la vigilancia en los nodos periféricos. La seguridad es predictiva."
    else: respuesta = "Comando recibido: '" + comando + "'. Analizando..."
    return jsonify({"respuesta": respuesta})

@app.route('/favicon.ico')
def favicon(): return "", 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
