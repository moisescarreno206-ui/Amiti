# ... (mantén tus importaciones y la función init_db)

@app.route('/', methods=['POST'])
def manejar_alerta():
    token = request.headers.get("X-AMITI-KEY")
    if token != LLAVE_SEGURIDAD:
        return jsonify({"status": "ACCESO DENEGADO"}), 403

    datos = request.json
    conn = sqlite3.connect('amiti_data.db')
    cursor = conn.cursor()
    
    # Insertar y guardar
    cursor.execute("INSERT INTO alertas (fecha, protocolo, lat, lon) VALUES (?, ?, ?, ?)",
                   (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datos['protocolo'], datos['latitud'], datos['longitud']))
    
    # Contar registros totales
    cursor.execute("SELECT COUNT(*) FROM alertas")
    total_alertas = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()

    return jsonify({
        "status": "Registro Exitoso", 
        "total_eventos": total_alertas, 
        "evaluacion": "Nivel NORMAL"
    })
