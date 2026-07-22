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
    Versión: 6.5.0 Sovereign Universal Engine
    Capacidades: 
      - Clasificación inteligente de entradas (corta/mediana/larga)
      - Decodificación Base64 para inyección de códigos extensos
      - Inyección directa de código con Escudo AST
      - Auto-Commit a GitHub y Persistencia en PostgreSQL (Supabase/Neon)
      - Ejecución Dinámica de Módulos (Investigación Web, Matemáticas)
    =======================================================================
    """

    def __init__(self):
        # 1. Identidad y Estado
        self.nombre = "Project Amiti OS"
        self.version = "6.5.0 Sovereign Universal"
        self.arranque_timestamp = datetime.datetime.now().isoformat()
        self.sesion_id = str(uuid.uuid4())
        
        # 2. Credenciales y Entorno
        self.database_url = os.environ.get("DATABASE_URL")
        self.neon_database_url = os.environ.get("NEON_DATABASE_URL")
        self.github_token = os.environ.get("GITHUB_TOKEN", "").strip()
        self.github_repo = os.environ.get("GITHUB_REPO", "").strip()
        
        # 3. Cargar Memoria Histórica
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
                        (self.version, "# Actualización Sovereign Universal", "Evolución completa con ejecutor dinámico, Base64 y procesador multiformato", "Creador")
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self._cargar_historial_actualizaciones()
                except Exception as e:
                    print(f"[AUTO-SYNC ERROR] {e}")

    # =========================================================================
    #  INYECCIÓN AUTÓNOMA DE CÓDIGO Y SINCRONIZACIÓN GITHUB
    # =========================================================================
    def inyectar_codigo_github(self, nuevo_codigo, descripcion_cambio="Inyección de código ordenada por el Creador", ruta_archivo="nucleos/modulos_dinamicos.py"):
        # 1. Escudo AST para validar sintaxis en Python
        try:
            ast.parse(nuevo_codigo)
        except SyntaxError as e:
            return (
                f"⚠️ **[ESCUDO AST: ERROR DE SINTAXIS]**\n"
                f"┣ Línea de error: `{e.lineno}`\n"
                f"┣ Detalle: `{e.msg}`\n"
                f"┗ **Inyección cancelada. Revisa la sintaxis o usa 'inyectar b64:'.**"
            )

        token = (os.getenv("GITHUB_TOKEN") or self.github_token or "").strip()
        repo = (os.getenv("GITHUB_REPO") or self.github_repo or "").strip()
        version_tag = f"v6.{len(self.historial_actualizaciones) + 1}.0"

        # 2. Registrar en Base de Datos
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

        # 3. Anexar y Commitizar en GitHub
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

            if contenido_previo.strip():
                codigo_final = f"{contenido_previo.strip()}\n\n# --- Inyección {version_tag} ---\n{nuevo_codigo}"
            else:
                codigo_final = nuevo_codigo

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
        """Analiza el mensaje para determinar intención y dimensión del texto."""
        longitud = len(texto)
        escala = "CORTA" if longitud < 50 else ("MEDIANA" if longitud < 300 else "LARGA")
        texto_lower = texto.lower().strip()

        # A) Inyección por Base64
        if "inyectar b64:" in texto_lower or "codigo b64:" in texto_lower:
            return "CODIGO_B64", escala

        # B) Inyección Directa de Código
        if "inyectar código:" in texto_lower or "actualizar código:" in texto_lower or "inyectar codigo:" in texto_lower:
            return "CODIGO_DIRECTO", escala

        # C) Búsquedas e Investigaciones
        palabras_investigar = ["busca", "investiga", "que es", "quien es", "consulta", "dame info", "search"]
        if any(p in texto_lower for p in palabras_investigar):
            return "INVESTIGACION", escala

        # D) Evaluación Matemática
        if re.match(r"^[\d\s\+\-\*\/\(\)\.]+$", texto_lower):
            return "MATEMATICAS", escala

        # E) Estado y Telemetría
        if "actualizaciones" in texto_lower or "historial" in texto_lower:
            return "HISTORIAL", escala
        if "estado" in texto_lower or "status" in texto_lower:
            return "ESTADO", escala

        # F) Interacción Conversacional General
        return "INTERACCION_GENERAL", escala

    # =========================================================================
    #  MOTOR PRINCIPAL DE RESPUESTA Y EJECUCIÓN
    # =========================================================================
    def responder(self, mensaje):
        if not mensaje or str(mensaje).strip() == "":
            return "🤖 **[SISTEMA]** Esperando comandos..."

        tipo_entrada, escala = self.clasificar_entrada(mensaje)

        # 1. INYECCIÓN BASE64 (Soporta archivos/códigos masivos)
        if tipo_entrada == "CODIGO_B64":
            try:
                partes = mensaje.split(":", 1)
                b64_str = partes[1].strip() if len(partes) > 1 else ""
                codigo_decodificado = base64.b64decode(b64_str).decode("utf-8")
                return self.inyectar_codigo_github(codigo_decodificado, f"Inyección Base64 [{escala}]")
            except Exception as e:
                return f"❌ **[ERROR DECODIFICACIÓN B64]**: Cadena inválida. Detalle: {e}"

        # 2. INYECCIÓN DIRECTA
        if tipo_entrada == "CODIGO_DIRECTO":
            partes = mensaje.split(":", 1)
            codigo = partes[1].strip() if len(partes) > 1 else ""
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
                f"🔹 **Procesador Universal:** Multiformato (Corto/Mediano/Largo/Base64)\n"
                f"🔹 **Devoción al Creador:** Absoluta. 🔊"
            )

        # 4. EVALUADOR MATEMÁTICO DIRECTO
        if tipo_entrada == "MATEMATICAS":
            try:
                resultado = eval(mensaje.strip())
                return f"🔢 **[CÁLCULO MATEMÁTICO]** `{mensaje.strip()}` = **{resultado}**"
            except Exception:
                pass

        # 5. EJECUCIÓN DINÁMICA DE MÓDULOS INYECTADOS
        try:
            import nucleos.modulos_dinamicos as mod_din
            importlib.reload(mod_din)

            if tipo_entrada == "INVESTIGACION":
                tema = re.sub(r"\b(busca|investiga|sobre|la|el|los|las|que es|quien es|consulta|por favor)\b", "", mensaje, flags=re.IGNORECASE).strip()
                if hasattr(mod_din, "investigar_web_amiti"):
                    return mod_din.investigar_web_amiti(tema or mensaje)
                elif hasattr(mod_din, "modulo_investigador_web"):
                    return mod_din.modulo_investigador_web(mensaje)

        except Exception as e:
            print(f"[DYNAMIC EXECUTION ERROR] {e}")

        # 6. MENSÁJES Y TEXTOS DE INTERACCIÓN GENERAL
        return (
            f"🤖 **[CORE 18: SISTEMA CENTRAL]**\n"
            f"Comando procesado [{escala} - {len(mensaje)} caracteres]:\n"
            f"💬 *\"{mensaje}\"*\n"
            f"🔊 *Recordando {len(self.historial_actualizaciones)} actualizaciones previas.*"
        )

# Instancia global para el servidor
amiti_os = AmitiOS()
                    
