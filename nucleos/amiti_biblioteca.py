import requests

class AmitiBibliotecaEngine:
    def __init__(self):
        self.nombre = "Motor de Biblioteca Multifuente Online"

    def buscar_en_biblioteca(self, consulta):
        query_limpia = consulta.lower()
        
        # 1. Detectar si el usuario busca un concepto teórico o un libro
        palabras_concepto = ["información", "informacion", "teoría", "teoria", "concepto", "qué es", "que es", "explicame"]
        es_concepto = any(p in query_limpia for p in palabras_concepto)

        # 2. Limpiar la consulta para dejar solo la palabra clave pura
        palabras_a_borrar = ["búscame", "buscame", "un libro sobre", "el libro", "libro", "manual", "consulta", "biblioteca", "información sobre", "informacion sobre", "sobre la", "sobre el", "sobre", "teoría de la", "teoria de la"]
        
        for palabra in palabras_a_borrar:
            query_limpia = query_limpia.replace(palabra, "").strip()

        if not query_limpia:
            query_limpia = consulta

        # --- RUTA A: MODO ENCICLOPEDIA (CONCEPTO DIRECTO) ---
        if es_concepto:
            try:
                url_wiki = f"https://es.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(query_limpia)}"
                headers = {"User-Agent": "AmitiOS/1.0 (Bot de consulta educativa)"}
                res = requests.get(url_wiki, headers=headers, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    extracto = data.get("extract")
                    titulo_wiki = data.get("title", query_limpia.capitalize())
                    if extracto:
                        return f"🌐 **[Wikipedia Base de Conocimiento] ({titulo_wiki})**\n\n{extracto}"
            except Exception as e:
                print(f"Error en Wikipedia (Ruta A): {e}")
            
            return f"⚠️ No encontré una definición exacta en la enciclopedia para el concepto: '{query_limpia}'."


        # --- RUTA B: MODO BIBLIOTECARIA (BÚSQUEDA DE LIBROS) ---
        # Intentar con Google Books API
        try:
            url_google = f"https://www.googleapis.com/books/v1/volumes?q={requests.utils.quote(query_limpia)}&maxResults=1"
            res = requests.get(url_google, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if "items" in data and len(data["items"]) > 0:
                    info = data["items"][0]["volumeInfo"]
                    titulo = info.get("title", "Título desconocido")
                    autores = ", ".join(info.get("authors", ["Autor desconocido"]))
                    descripcion = info.get("description", "Sin descripción disponible.")
                    if len(descripcion) > 300:
                        descripcion = descripcion[:300] + "..."
                    
                    return f"📚 **[Google Books API]**\n* **Libro:** {titulo}\n* **Autor(es):** {autores}\n* **Resumen:** {descripcion}"
        except Exception as e:
            print(f"Error en Google Books: {e}")

        # Intentar con Open Library API
        try:
            url_open = f"https://openlibrary.org/search.json?q={requests.utils.quote(query_limpia)}&limit=1"
            res = requests.get(url_open, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if "docs" in data and len(data["docs"]) > 0:
                    doc = data["docs"][0]
                    titulo = doc.get("title", "Título desconocido")
                    autor = ", ".join(doc.get("author_name", ["Autor desconocido"]))
                    anio = doc.get("first_publish_year", "Fecha desconocida")
                    
                    return f"📖 **[Open Library API]**\n* **Libro:** {titulo}\n* **Autor(es):** {autor}\n* **Primer año de publicación:** {anio}"
        except Exception as e:
            print(f"Error en Open Library: {e}")

        # Respaldo final a Wikipedia si no encuentra ningún libro
        try:
            url_wiki = f"https://es.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(query_limpia)}"
            headers = {"User-Agent": "AmitiOS/1.0 (Bot de consulta educativa)"}
            res = requests.get(url_wiki, headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                extracto = data.get("extract")
                titulo_wiki = data.get("title", query_limpia.capitalize())
                if extracto:
                    return f"🌐 **[Wikipedia Respaldo] ({titulo_wiki})**\n\n{extracto}"
        except Exception as e:
            print(f"Error en Wikipedia (Respaldo): {e}")

        return f"⚠️ No se encontraron registros de libros ni en la enciclopedia para: '{query_limpia}'."
        
