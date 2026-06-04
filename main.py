# ... (mantén tus importaciones actuales)

@app.route('/protocolo_expansion', methods=['POST'])
def protocolo_expansion():
    # Solo el jefe puede iniciar una expansión o mudanza
    if request.headers.get("X-AMITI-KEY") != LLAVE_SEGURIDAD:
        return jsonify({"status": "ACCESO DENEGADO"}), 403
    
    comando = request.json.get("comando")
    
    if comando == "MUDANZA":
        # AMITI prepara sus datos para ser exportados a otro nodo
        return jsonify({
            "status": "MUDANZA INICIADA",
            "datos": "amiti_data.db",
            "instruccion": "Enviar a nuevo servidor"
        })
    elif comando == "SINCRONIZAR_AGENTE":
        return jsonify({
            "status": "AGENTE RECONOCIDO",
            "config": "NODO_AUTORIZADO_OK"
        })
    
    return jsonify({"status": "COMANDO DESCONOCIDO"})

# ... (mantén el resto de tu lógica de alertas y auto_upgrade)
