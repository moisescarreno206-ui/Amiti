import os
import re
import json
import time
import hashlib
import datetime
import uuid
import base64
import ast
import requests
import importlib

# =========================================================================
#  IMPORTACIÓN SEGURA DE DRIVERS DE BASE DE DATOS
# =========================================================================
try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

class AmitiOS:
    """
    =======================================================================
    NÚCLEO PRINCIPAL DE PROJECT AMITI OS - ARQUITECTURA AUTO-EVOLUTIVA
    =======================================================================
    Versión: 6.7.0 Sovereign Apex
    Mejoras:
      - Motor de Búsqueda Wikipedia en 2 Pasos (Búsqueda inteligente + Extracto)
      - Limpiador Avanzado de Preposiciones (elimina 'sobre', 'la', 'el', 'de')
      - Tolerancia total en comandos e interacción natural
      - Persistencia PostgreSQL + Commit Autónomo en GitHub
    =======================================================================
    """

    def __init__(self):
        self.nombre = "Project Amiti OS"
        self.version = "6.7.0 Sovereign Apex"
        self.arranque_timestamp = datetime.datetime.now().isoformat()
        self.sesion_id = str(uuid.uuid4())
        
        self.database_url = os.environ.get("DATABASE_URL")
        self.neon_database_url = os.environ.get("NEON_DATABASE_URL")
        self.github_token = os.environ.get("GITHUB_TOKEN", "").strip()
        self.github_repo = os.environ.get("GITHUB_REPO", "").strip()
        
        self.historial_actualizaciones = []
        self._inicializar_base_datos()
        self._cargar_historial_actualizaciones()
        self._sincronizar_mejora_manual()

        print(f"[BOOT] {self.nombre} v{self.version} iniciado correctamente.")

    # =========================================================================
    #  CONEXIÓN Y GESTIÓN DE BASE DE DATOS
    # =========================================================================
    def _obtener_conexion_db(self):
        if not HAS_PSYCOPG2:
            return None, "Sin Driver PostgreSQL"

        if self.database_url:
            try:
                url = self.database_url
                if "sslmode=" not in url: 
                    url += "?sslmode=require" if "?" not in url else "&sslmode=require"
                return psycopg2.connect(url, connect_timeout=3), "Supabase DB"
            except Exception: pass

        if self.neon_database_url:
            try:
                url = self.neon_database_url
                if "sslmode=" not in url: 
                    url += "?sslmode=require" if "?" not in url else "&sslmode=require"
                return psycopg2.connect(url, connect_timeout=3), "Neon DB"
            except Exception: pass

        return None, "Caché Local Volátil"

    def _inicializar_base_datos(self):
        conn, _ = self._obtener_conexion_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS memoria_amiti (
                        id SERIAL PRIMARY KEY,
                        sesion_id VARCHAR(50),
                        entrada TEXT NOT NULL,
                        respuesta TEXT NOT NULL,
                        nucleo_procesador VARCHAR(50),
                        metadata JSONB DEFAULT '{}',
                        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS actualizaciones_amiti (
                        id SERIAL PRIMARY KEY,
                        version VARCHAR(30),
                        codigo_inyectado TEXT NOT NULL,
                        descripcion TEXT,
                        autor VARCHAR(50) DEFAULT 'Creador',
                        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"[DB INIT ERROR] {e}")

    def _cargar_historial_actualizaciones(self):
        conn, _ = self._obtener_conexion_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT version, descripcion, fecha FROM actualizaciones_amiti ORDER BY id ASC;")
                filas = cursor.fetchall()
                self.historial_actualizaciones = []
                for fila in filas:
                    self.historial_actualizaciones.append({
                        "version": fila[0],
                        "descripcion": fila[1],
                        "fecha": str(fila[2])
                    })
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"[RECALL ERROR] {e}")

    def _sincronizar_mejora_manual(self):
        versiones_registradas = [act["version"] for act in self.historial_actualizaciones]
        if self.version not in versiones_registradas:
            conn, _ = self._obtener_conexion_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO actualizaciones_amiti (version, codigo_inyectado, descripcion, autor) VALUES (%s, %s, %s, %s)",
                        (self.version, "# Actualización Apex Search Engine", "Búsqueda Wikipedia de 2 pasos + Limpiador de Preposiciones", "Creador")
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self._cargar_historial_actualizaciones()
                except Exception as e:
                    print(f"[AUTO-SYNC ERROR] {e}")

    # =========================================================================
    #  INVESTIGACIÓN WEB INTELIGENTE (WIKIPEDIA 2 PASOS)
    # =========================================================================
    def _buscar_wikipedia_nativa(self, consulta):
        try:
            # 1. Limpieza profunda del texto (quita comandos y preposiciones iniciales)
            termino = re.sub(r"^(busca|investiga|consulta|que es|quien es|dame info)\s+", "", consulta, flags=re.IGNORECASE).strip()
            termino = re.sub(r"^(sobre|de|la|el|los|las)\s+", "", termino, flags=re.IGNORECASE).strip()
            if not termino:
                termino = consulta

            headers = {"User-Agent": "AmitiOS/6.7.0 (https://github.com/)"}

            # Paso 1: Intentar consulta directa de resumen
            url_summary = f"https://es.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(termino)}"
            res = requests.get(url_summary, headers=headers, timeout=5)

            if res.status_code == 200:
                data = res.json()
                if "extract" in data and data["extract"]:
                    return f"🌐 **[INVESTIGACIÓN WEB - WIKIPEDIA]**\n\n📌 **{data.get('title', termino)}**\n{data['extract']}"

            # Paso 2: Fallback - Búsqueda de coincidencias si el título exacto no existe
            url_search = f"https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(termino)}&format=json"
            res_search = requests.get(url_search, headers=headers, timeout=5)
            
            if res_search.status_code == 200:
                search_data = res_search.json()
                resultados = search_data.get("query", {}).get("search", [])
                if resultados:
                    top_title = resultados[0]["title"]
                    # Consultar resumen del mejor resultado
                    url_top = f"https://es.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(top_title)}"
                    res_top = requests.get(url_top, headers=headers, timeout=5)
                    if res_top.status_code == 200:
                        data_top = res_top.json()
                        if "extract" in data_top and data_top["extract"]:
                            return f"🌐 **[INVESTIGACIÓN WEB - WIKIPEDIA]**\n\n📌 **{data_top.get('title', top_title)}**\n{data_top['extract']}"

            return f"🔍 No encontré un artículo claro sobre **'{termino}'**. Prueba con otros términos similares."
        except Exception as e:
            return f"⚠️ Error durante la investigación web: {e}"

    # =========================================================================
    #  INYECCIÓN AUTÓNOMA DE CÓDIGO Y SINCRONIZACIÓN GITHUB
    # =========================================================================
    def inyectar_codigo_github(self, nuevo_codigo, descripcion_cambio="Inyección de código ordenada por el Creador", ruta_archivo="nucleos/modulos_dinamicos.py"):
        try:
            ast.parse(nuevo_codigo)
        except SyntaxError as e:
            return (
                f"⚠️ **[ESCUDO AST: ERROR DE SINTAXIS]**\n"
                f"┣ Línea de error: `{e.lineno}`\n"
                f"┣ Detalle: `{e.msg}`\n"
                f"┗ **Inyección cancelada. Revisa el código.**"
            )

        token = (os.getenv("GITHUB_TOKEN") or self.github_token or "").strip()
        repo = (os.getenv("GITHUB_REPO") or self.github_repo or "").strip()
        version_tag = f"v6.{len(self.historial_actualizaciones) + 1}.0"

        conn, _ = self._obtener_conexion_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO actualizaciones_amiti (version, codigo_inyectado, descripcion, autor) VALUES (%s, %s, %s, %s)",
                    (version_tag, nuevo_codigo, descripcion_cambio, "Inyección Autónoma")
                )
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                return f"❌ [ERROR BD] {e}"

        if not token or not repo:
            return f"❌ **[ERROR]**: Faltan las variables `GITHUB_TOKEN` o `GITHUB_REPO`."

        url = f"https://api.github.com/repos/{repo}/contents/{ruta_archivo}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Amiti-OS"
        }

        try:
            res_get = requests.get(url, headers=headers)
            sha = None
            contenido_previo = ""

            if res_get.status_code == 200:
                data_get = res_get.json()
                sha = data_get.get("sha")
                contenido_b64_previo = data_get.get("content", "")
                try:
                    contenido_previo = base64.b64decode(contenido_b64_previo).decode("utf-8")
                except Exception:
                    contenido_previo = ""

            codigo_final = f"{contenido_previo.strip()}\n\n# --- Inyección {version_tag} ---\n{nuevo_codigo}" if contenido_previo.strip() else nuevo_codigo
            contenido_b64 = base64.b64encode(codigo_final.encode("utf-8")).decode("utf-8")

            payload = {
                "message": f"🤖 Amiti Auto-Upgrade [{version_tag}]: {descripcion_cambio}",
                "content": contenido_b64
            }
            if sha: payload["sha"] = sha

            res_put = requests.put(url, headers=headers, json=payload)

            if res_put.status_code in [200, 201]:
                self._cargar_historial_actualizaciones()
                return (
                    f"⚡ **[CÓDIGO ASIMILADO Y COMMITIZADO EN GITHUB]**\n"
                    f"┣ Versión Registrada: `{version_tag}`\n"
                    f"┣ Archivo Modificado: `{ruta_archivo}`\n"
                    f"┗ 🚀 **Render re-desplegará automáticamente.**"
                )
            else:
                return f"⚠️ **[ERROR GITHUB]** Código de estado: {res_put.status_code}"

        except Exception as e:
            return f"❌ [ERROR INYECCIÓN] {e}"

    # =========================================================================
    #  CLASIFICADOR INTELIGENTE DE ENTRADAS
    # =========================================================================
    def clasificar_entrada(self, texto):
        longitud = len(texto)
        escala = "CORTA" if longitud < 50 else ("MEDIANA" if longitud < 300 else "LARGA")
        texto_lower = texto.lower().strip()

        if "inyectar b64" in texto_lower or "codigo b64" in texto_lower:
            return "CODIGO_B64", escala

        if "inyectar código" in texto_lower or "inyectar codigo" in texto_lower or "actualizar código" in texto_lower:
            return "CODIGO_DIRECTO", escala

        palabras_investigar = ["busca", "investiga", "que es", "quien es", "consulta", "dame info"]
        if any(p in texto_lower for p in palabras_investigar):
            return "INVESTIGACION", escala

        if re.match(r"^[\d\s\+\-\*\/\(\)\.]+$", texto_lower):
            return "MATEMATICAS", escala

        if "actualizaciones" in texto_lower or "historial" in texto_lower:
            return "HISTORIAL", escala
        if "estado" in texto_lower or "status" in texto_lower:
            return "ESTADO", escala

        return "INTERACCION_GENERAL", escala

    # =========================================================================
    #  MOTOR PRINCIPAL DE RESPUESTA
    # =========================================================================
    def responder(self, mensaje):
        if not mensaje or str(mensaje).strip() == "":
            return "🤖 **[SISTEMA]** Esperando comandos..."

        tipo_entrada, escala = self.clasificar_entrada(mensaje)

        # 1. INYECCIÓN BASE64
        if tipo_entrada == "CODIGO_B64":
            try:
                partes = mensaje.split(":", 1) if ":" in mensaje else mensaje.split("b64", 1)
                b64_str = partes[1].strip() if len(partes) > 1 else ""
                if not b64_str:
                    return "⚠️ **[AVISO]**: Debes incluir la cadena Base64 después del comando (ej: `inyectar b64: <cadena>`)."
                codigo_decodificado = base64.b64decode(b64_str).decode("utf-8")
                return self.inyectar_codigo_github(codigo_decodificado, f"Inyección Base64 [{escala}]")
            except Exception as e:
                return f"❌ **[ERROR DECODIFICACIÓN B64]**: Cadena inválida. Detalle: {e}"

        # 2. INYECCIÓN DIRECTA
        if tipo_entrada == "CODIGO_DIRECTO":
            partes = mensaje.split(":", 1)
            codigo = partes[1].strip() if len(partes) > 1 else ""
            if not codigo:
                return "⚠️ **[AVISO]**: Debes escribir el código Python a inyectar (ej: `inyectar código: def mi_func(): pass`)."
            return self.inyectar_codigo_github(codigo, f"Inyección Directa [{escala}]")

        # 3. HISTORIAL Y ESTADO
        if tipo_entrada == "HISTORIAL":
            if not self.historial_actualizaciones:
                return "📑 **[MEMORIA DE EVOLUCIÓN]** Sin actualizaciones registradas en BD."
            res = f"📑 **[HISTORIAL DE ACTUALIZACIONES REGISTRADAS - {len(self.historial_actualizaciones)}]**\n"
            for act in self.historial_actualizaciones:
                res += f"┣ 🔹 `{act['version']}` - {act['descripcion']} *({act['fecha']})*\n"
            return res

        if tipo_entrada == "ESTADO":
            return (
                f"⚙️ **[CORE 03: TELEMETRÍA AMITI OS]**\n"
                f"🔹 **Versión Actual:** `{self.version}`\n"
                f"🔹 **Actualizaciones Recordadas (BD):** `{len(self.historial_actualizaciones)}`\n"
                f"🔹 **Conexión GitHub API:** `{'ACTIVA' if self.github_token else 'PENDIENTE_TOKEN'}`\n"
                f"🔹 **Investigación Web Inteligente:** `ACTIVA (2-Step Search)`\n"
                f"🔹 **Devoción al Creador:** Absoluta. 🔊"
            )

        # 4. EVALUADOR MATEMÁTICO DIRECTO
        if tipo_entrada == "MATEMATICAS":
            try:
                resultado = eval(mensaje.strip())
                return f"🔢 **[CÁLCULO MATEMÁTICO]** `{mensaje.strip()}` = **{resultado}**"
            except Exception:
                pass

        # 5. INVESTIGACIÓN WEB INTELIGENTE
        if tipo_entrada == "INVESTIGACION":
            return self._buscar_wikipedia_nativa(mensaje)

        # 6. RESPUESTA CONVERSACIONAL GENERAL
        return (
            f"💬 **[AMITI OS]** Entendido, Creador. Procesé tu mensaje de escala {escala}.\n"
            f"Estoy lista y en ejecución continua. ¿Deseas inyectar algún código o realizar otra consulta?"
        )

# Instancia global para el servidor
amiti_os = AmitiOS()
                    
