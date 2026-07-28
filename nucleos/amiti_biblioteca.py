import requests

class AmitiBibliotecaEngine:
    def __init__(self):
        self.nombre = "Motor de Biblioteca Multifuente Online"

    def buscar_en_biblioteca(self, consulta):
        # Limpiamos la consulta para buscar en las APIs
        query_limpia = consulta.lower()
        for palabra in ["búscame", "buscame", "libro", "manual", "consulta", "biblioteca"]:
            query_limpia = query_limpia.replace(palabra, "").strip()

        if not query_limpia:
            query_limpia = consulta

        # 1. Intentar con Google Books API
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

        # 2. Intentar con Open Library API
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

        # 3. Respaldo conceptual con Wikipedia API (Ideal para ciencia, medicina, derecho, física, etc.)
        try:
            url_wiki = f"https://es.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(query_limpia)}"
            headers = {"User-Agent": "AmitiOS/1.0 (Bot de consulta educativa)"}
            res = requests.get(url_wiki, headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                extracto = data.get("extract")
                titulo_wiki = data.get("title", query_limpia)
                if extracto:
                    return f"🌐 **[Wikipedia Base de Conocimiento] ({titulo_wiki})**\n\n{extracto}"
        except Exception as e:
            print(f"Error en Wikipedia: {e}")

        return f"⚠️ No se encontraron registros exactos en Google Books, Open Library ni en la enciclopedia para: '{query_limpia}'."
        
