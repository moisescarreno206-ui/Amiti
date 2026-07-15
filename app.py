# Añade esto en app.py dentro de la función procesar
@app.route('/procesar', methods=['POST'])
def procesar():
    data = request.json
    comando = data.get('comando', '')
    
    # Capa de contra-ataque: Limpieza de caracteres de escape
    comando_seguro = "".join(char for char in comando if char.isalnum() or char.isspace() or char in "+-*/")
    
    return jsonify({"respuesta": amiti.procesar(comando_seguro)})
    
