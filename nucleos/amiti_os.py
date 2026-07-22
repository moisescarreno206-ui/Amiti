import os
import re
import json
import time
import hashlib
import datetime
import uuid
import base64
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
    Versión: 6.0.0 Self-Evolving Engine
    Capacidades: Persistencia en BD, Auto-Commit en GitHub API,
                 Recuperación de Historial al Inicio.
    =======================================================================
    """

    def __init__(self):
        # 1. Identidad y Estado
        self.nombre = "Project Amiti OS"
        self.version = "6.0.0 Self-Evolving"
        self.arranque_timestamp = datetime.datetime.now().isoformat()
        self.sesion_id = str(uuid.uuid4())
        
        # 2. Credenciales e Integraciones
        self.database_url = os.environ.get("DATABASE_URL")
        self.neon_database_url = os.environ.get("NEON_DATABASE_URL")
        self.github_token = os.environ.get("GITHUB_TOKEN")      # Token de acceso de GitHub
        self.github_repo = os.environ.get("GITHUB_REPO")        # Formato: "usuario/nombre-repo"
        
        # 3. Cargar Memoria Histórica de Actualizaciones desde BD
        self.historial_actualizaciones = []
        self._inicializar_base_datos()
        self._cargar_historial_actualizaciones()

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
                # Tabla de Actualizaciones de Código (Inyecciones)
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

    # =========================================================================
    #  CORE 17: MOTOR DE INYECCIÓN DE CÓDIGO Y AUTO-COMMIT EN GITHUB
    # =========================================================================
    def inyectar_codigo_github(self, nuevo_codigo, descripcion_cambio, ruta_archivo="nucleos/modulos_dinamicos.py"):
        """
        Guarda la actualización en la BD y realiza un Commit real en GitHub via API.
        """
        # 1. Guardar en Base de Datos
        conn, _ = self._obtener_conexion_db()
        version_tag = f"v6.{len(self.historial_actualizaciones) + 1}.0"
        
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO actualizaciones_amiti (version, codigo_inyectado, descripcion) VALUES (%s, %s, %s)",
                    (version_tag, nuevo_codigo, descripcion_cambio)
                )
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                return f"❌ [ERROR BD] No se pudo registrar la actualización en la BD: {e}"

        # 2. Si las llaves de GitHub no están configuradas, solo guarda en BD
        if not self.github_token or not self.github_repo:
            return (
                f"💾 **[ACTUALIZACIÓN GUARDADA EN BD]**\n"
                f"┣ Versión: `{version_tag}`\n"
                f"┣ Nota: Para enviar el commit automático a GitHub, agrega `GITHUB_TOKEN` y `GITHUB_REPO` en las Variables de Entorno de Render."
            )

        # 3. Commit automático a la API REST de GitHub
        url = f"https://api.github.com/repos/{self.github_repo}/contents/{ruta_archivo}"
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            # Obtener SHA del archivo si ya existe
            res_get = requests.get(url, headers=headers)
            sha = res_get.json().get("sha") if res_get.status_code == 200 else None

            # Codificar contenido a Base64
            contenido_b64 = base64.b64encode(nuevo_codigo.encode("utf-8")).decode("utf-8")

            payload = {
                "message": f"🤖 Amiti Auto-Upgrade [{version_tag}]: {descripcion_cambio}",
                "content": contenido_b64,
                "branch": "main"
            }
            if sha:
                payload["sha"] = sha

            res_put = requests.put(url, headers=headers, json=payload)

            if res_put.status_code in [200, 201]:
                return (
                    f"⚡ **[CÓDIGO INYECTADO Y COMMITEADO EN GITHUB]**\n"
                    f"┣ Versión Asimilada: `{version_tag}`\n"
                    f"┣ Archivo Modificado: `{ruta_archivo}`\n"
                    f"┣ Estado de BD: Persistido Correctamente\n"
                    f"┗ 🚀 **Render detectará el commit en GitHub y desplegará la actualización automáticamente.**"
                )
            else:
                return f"⚠️ **[ERROR GITHUB API]** Status {res_put.status_code}: {res_put.json().get('message')}"

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
