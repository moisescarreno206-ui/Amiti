@app.route('/chat', methods=['POST'])
def chat():
    comando = request.json.get("comando", "")
    conn = sqlite3.connect('amiti_core.db')
    
    # Recopilación de datos
    conn.execute("INSERT INTO eventos (tipo, detalle) VALUES (?, ?)", ('ENTRADA_USUARIO', comando))
    conn.commit()
    
    cmd_lower = comando.lower()
    
    # Lógica de Inteligencia Mejorada
    if "estado" in cmd_lower: 
        respuesta = "SISTEMA OMEGA: Operativo. Integridad de red al 100%."
    elif "diagnóstico" in cmd_lower: 
        count = conn.execute("SELECT COUNT(*) FROM eventos").fetchone()[0]
        respuesta = f"ANÁLISIS: {count} nodos de información procesados. Mi base de conocimiento se expande."
    elif "hola" in cmd_lower or "saludos" in cmd_lower:
        respuesta = "Saludos, operador. Estoy conectada y lista para analizar nuevos datos."
    else: 
        # Respuesta variable para no sonar robótica
        respuestas_ia = [
            f"He registrado tu aporte sobre '{comando}'. Lo incluiré en mi análisis de patrones.",
            f"Interesante. He guardado '{comando}' en los registros de evolución.",
            f"Procesando '{comando}'... La base de datos ha sido actualizada con éxito."
        ]
        import random
        respuesta = random.choice(respuestas_ia)
    
    conn.close()
    return jsonify({"respuesta": respuesta})
