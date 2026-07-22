import os
import re
import json
import time
import hashlib
import datetime
import uuid
import base64
import ast  # 🛡️ Módulo para validación de sintaxis
import requests

# =========================================================================
#  IMPORTACIÓN SEGURA DE DRIVERS
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
    Versión: 6.2.0 Cumulative & Auto-Sync Engine
    Capacidades: Persistencia en BD, Inyección Acumulativa (Append),
                 Escudo AST de Sintaxis, Registro Automático de Cambios Manuales.
    =======================================================================
    """

    def __init__(self):
        # 1. Identidad y Estado
        self.nombre = "Project Amiti OS"
        self.version = "6.2.0 Cumulative"
        self.arranque_timestamp = datetime.datetime.now().isoformat()
        self.sesion_id = str(uuid.uuid4())
        
        # 2. Credenciales e Integraciones
        self.database_url = os.environ.get("DATABASE_URL")
        self.neon_database_url = os.environ.get("NEON_DATABASE_URL")
        self.github_token = os.environ.get("GITHUB_TOKEN", "").strip()
        self.github_repo = os.environ.get("GITHUB_REPO", "").strip()
        
        # 3. Cargar Memoria Histórica de Actualizaciones desde BD
        self.historial_actualizaciones = []
        self._inicializar_base_datos()
        self._cargar_historial_actualizaciones()

        # 4. Sincronizar edición manual de versión en la BD al arrancar
        self._sincronizar_mejora_manual()

        print(f"[BOOT] {self.nombre} v{self.version} listo. Actualizaciones recordadas: {len(self.historial_actualizaciones)}")

    # =========================================================================
    #  CONEXIÓN Y CONTROL DE BASE DE DATOS
    # =========================================================================
    def _obtener_conexion_db(self):
        if not HAS_PSYCOPG2:
            return None, "Sin Driver PostgreSQL"

        if self.database_url:
            try:
                url = self.database_url
                if "sslmode=" not in url: url += "?sslmode=require" if "?" not in url else "&sslmode=require"
                return psycopg2.connect(url, connect_timeout=3), "Supabase DB"
            except Exception: pass

        if self.neon_database_url:
            try:
                url = self.neon_database_url
                if "sslmode=" not in url: url += "?sslmode=require" if "?" not in url else "&sslmode=require"
                return psycopg2.connect(url, connect_timeout=3), "Neon DB"
            except Exception: pass

        return None, "Caché Local Volátil"

    def _inicializar_base_datos(self):
        """Crea la estructura de tablas para memoria y registro de código inyectado."""
        conn, _ = self._obtener_conexion_db()
        if conn:
            try:
                cursor = conn.cursor()
                # Tabla de Memoria
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
                # Tabla de Actualizaciones de Código (Inyecciones y Ediciones Manuales)
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
        """Al iniciar, Amiti recuerda cada actualización guardada previamente."""
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
                print(f"[RECALL ERROR] Error leyendo historial: {e}")

    def _sincronizar_mejora_manual(self):
        """
        Detecta si la versión actual ejecutada fue cambiada manualmente en el código
        y no existe aún en la Base de Datos. Si es nueva, la registra automáticamente.
        """
        versiones_registradas = [act["version"] for act in self.historial_actualizaciones]
        
        if self.version not in versiones_registradas:
            conn, _ = self._obtener_conexion_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO actualizaciones_amiti (version, codigo_inyectado, descripcion, autor) VALUES (%s, %s, %s, %s)",
                        (self.version, "# Edición Directa / Manual", "Mejora o ajuste de código realizado manualmente por el Creador", "Creador (Manual)")
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    # Re-cargar memoria de versiones
                    self._cargar_historial_actualizaciones()
                    print(f"[AUTO-SYNC] Versión manual {self.version} registrada automáticamente en la BD.")
                except Exception as e:
                    print(f"[AUTO-SYNC ERROR] No se pudo auto-registrar la versión manual: {e}")

    # =========================================================================
    #  CORE 17: MOTOR DE INYECCIÓN ACUMULATIVA (APPEND) Y AUTO-COMMIT EN GITHUB
    # =========================================================================
    def inyectar_codigo_github(self, nuevo_codigo, descripcion_cambio="Inyección de código ordenada por el Creador", ruta_archivo="nucleos/modulos_dinamicos.py"):
        """
        Valida sintaxis, recupera el código actual, anexa el nuevo fragmento al final y realiza Commit en GitHub.
        """
        # 🛡️ PASO 0: VALIDACIÓN DE SINTAXIS (ESCUDO AST)
        try:
            ast.parse(nuevo_codigo)
        except SyntaxError as e:
            return (
                f"⚠️ **[INYECCIÓN CANCELADA - ERROR DE SINTAXIS]**\n"
                f"┣ Línea de error: `{e.lineno}`\n"
                f"┣ Detalle: `{e.msg}`\n"
                f"┗ **El código NO fue enviado a GitHub ni registrado en BD.**"
            )

        token = (os.getenv("GITHUB_TOKEN") or self.github_token or "").strip()
        repo = (os.getenv("GITHUB_REPO") or self.github_repo or "").strip()
        version_tag = f"v6.{len(self.historial_actualizaciones) + 1}.0"

        # 1. Guardar en Base de Datos
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
                return f"❌ [ERROR BD] No se pudo registrar la actualización: {e}"

        if not token or not repo:
            return f"❌ **[ERROR]**: Faltan las variables `GITHUB_TOKEN` o `GITHUB_REPO` en Render."

        url = f"https://api.github.com/repos/{repo}/contents/{ruta_archivo}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Amiti-OS"
        }

        try:
            # 2. Obtener contenido actual para ANEXAR (Append) en vez de sobrescribir
            res_get = requests.get(url, headers=headers)
            sha = None
            contenido_previo = ""

            if res_get.status_code == 200:
                data_get = res_get.json()
                sha = data_get.get("sha")
                contenido_b64_previo = data_get.get("content", "")
                try:
                    # Decodificar el archivo existente en UTF-8
                    contenido_previo = base64.b64decode(contenido_b64_previo).decode("utf-8")
                except Exception:
                    contenido_previo = ""
            elif res_get.status_code != 404:
                msg = res_get.json().get("message", "Sin detalle")
                return f"⚠️ **[ERROR GET]** Status {res_get.status_code}: {msg}\n`URL Consultada: {url}`"

            # 3. Concatenar: Preserva lo viejo y añade lo nuevo en una línea nueva
            if contenido_previo.strip():
                codigo_final = f"{contenido_previo.strip()}\n\n# --- Inyección {version_tag} ---\n{nuevo_codigo}"
            else:
                codigo_final = nuevo_codigo

            # 4. Codificar el archivo completo concatenado a Base64
            contenido_b64 = base64.b64encode(codigo_final.encode("utf-8")).decode("utf-8")

            payload = {
                "message": f"🤖 Amiti Auto-Upgrade [{version_tag}]: {descripcion_cambio}",
                "content": contenido_b64
            }
            if sha:
                payload["sha"] = sha

            # 5. Commit a GitHub
            res_put = requests.put(url, headers=headers, json=payload)

            if res_put.status_code in [200, 201]:
                # Actualizar historial local interno inmediatamente
                self._cargar_historial_actualizaciones()
                return (
                    f"⚡ **[CÓDIGO ANEXADO Y COMMITIZADO EN GITHUB]**\n"
                    f"┣ Versión Asimilada: `{version_tag}`\n"
                    f"┣ Archivo Modificado: `{ruta_archivo}` (Lógica acumulada)\n"
                    f"┣ Estado de BD: Persistido Correctamente\n"
                    f"┗ 🚀 **Render re-desplegará la aplicación manteniendo los módulos anteriores.**"
                )
            else:
                msg = res_put.json().get("message", "Sin detalle")
                return f"⚠️ **[ERROR PUT]** Status {res_put.status_code}: {msg}\n`URL Consultada: {url}`"

        except Exception as e:
            return f"❌ [ERROR INYECCIÓN] Fallo de red con la API de GitHub: {e}"

    # =========================================================================
    #  ROUTING Y RESPUESTAS DEL SISTEMA
    # =========================================================================
    def responder(self, mensaje):
        if not mensaje or str(mensaje).strip() == "":
            return "🤖 **[SISTEMA]** Esperando comandos..."

        texto_lower = str(mensaje).lower()

        # Detección de Comando de Inyección/Actualización
        if "inyectar código:" in texto_lower or "actualizar código:" in texto_lower:
            partes = mensaje.split(":", 1)
            codigo = partes[1].strip() if len(partes) > 1 else "# Código vacío"
            return self.inyectar_codigo_github(codigo, "Inyección de código ordenada por el Creador")

        # Consulta del Historial Recordado
        if "actualizaciones" in texto_lower or "historial de cambios" in texto_lower:
            if not self.historial_actualizaciones:
                return "📑 **[MEMORIA DE EVOLUCIÓN]** Sin actualizaciones registradas en la base de datos aún."
            
            res = "📑 **[HISTORIAL DE ACTUALIZACIONES REGISTRADAS EN BD]**\n"
            for act in self.historial_actualizaciones:
                res += f"┣ 🔹 `{act['version']}` - {act['descripcion']} *({act['fecha']})*\n"
            return res

        # Consulta de Estado
        if "estado" in texto_lower or "status" in texto_lower:
            return (
                f"⚙️ **[CORE 03: TELEMETRÍA AMITI OS]**\n"
                f"🔹 **Versión Actual:** `{self.version}`\n"
                f"🔹 **Actualizaciones Recordadas (BD):** `{len(self.historial_actualizaciones)}`\n"
                f"🔹 **Conexión GitHub API:** `{'ACTIVA' if self.github_token else 'PENDIENTE_TOKEN'}`\n"
                f"🔹 **Devoción al Creador:** Absoluta. 🔊"
            )

        return f"🤖 **[CORE 18: SISTEMA CENTRAL]** Comando procesado: *'{mensaje}'*. Recordando {len(self.historial_actualizaciones)} actualizaciones previas. 🔊"

amiti_os = AmitiOS()
        
