def enviar_alerta_nube(protocolo="EMERGENCIA_ALTA", lat="8.9341", lon="-67.4283"):
    payload = {
        "evento": "DISPARO_PROTOCOLO",
        "protocolo": protocolo,
        "latitud": str(lat),
        "longitud": str(lon),
        "timestamp": time.time()
    }
    
    headers = {"X-AMITI-KEY": "AMITI_CORE_2026_SUPER_SECRET"}
    
    print(f"\n{C_AZUL}📡 Conectando...{C_RESET}")
    try:
        respuesta = requests.post(URL_SERVIDOR, json=payload, headers=headers, timeout=25)
        
        # ESTA PARTE DEBE ESTAR DENTRO DE LA FUNCIÓN
        if respuesta.status_code == 200:
            datos = respuesta.json()
            print(f"{C_VERDE}✅ [TRANSMISIÓN SEGURA]{C_RESET}")
            # Aquí AMITI nos cuenta cuántos eventos hay en su memoria
            print(f"📊 Total en base de datos: {datos.get('total_eventos', 'N/A')}")
            print(f"🛰️ Eval: {datos.get('evaluacion')}")
        else:
            print(f"Error: {respuesta.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
