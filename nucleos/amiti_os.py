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
#  IMPORTACIÓN DEL MÓDULO DE SEGURIDAD Y DINÁMICOS
# =========================================================================
try:
    from nucleos.modulos_dinamicos import modulo_seguridad, modulo_proteccion, modulo_salud
    HAS_DYNAMIC_MODULES = True
    HAS_SECURITY_MODULE = True
except ImportError:
    HAS_DYNAMIC_MODULES = False
    HAS_SECURITY_MODULE = False

try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

class AmitiOS:
    """
    =======================================================================
    NÚCLEO PRINCIPAL DE PROJECT AMITI OS
    =======================================================================
    Versión: 6.15.0 Sovereign Sentinel
    Mejoras:
      - Enlace directo con modulo_seguridad, modulo_proteccion y modulo_salud
      - Comandos directos: 'registrar evento:', 'telemetria', 'killswitch',
        'triaje:', 'primeros auxilios:', 'hash:'
    =======================================================================
    """

    def __init__(self):
        self.nombre = "Project Amiti OS"
        self.version = "6.15.0 Sovereign Sentinel"
        self.arranque_timestamp = datetime.datetime.now().isoformat()
        self.sesion_id = str(uuid.uuid4())
        
        self.database_url = os.environ.get("DATABASE_URL")
        self.neon_database_url = os.environ.get("NEON_DATABASE_URL")
        self.github_token = os.environ.get("GITHUB_TOKEN", "").strip()
        self.github_repo = os.environ.get("GITHUB_REPO", "").strip()
        
        self.historial_actualizaciones = []
        self._inicializar_base_datos()
        self._cargar_historial_actualizaciones()

        print(f"[BOOT] {self.nombre} v{self.version} iniciado correctamente.")

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

    # =========================================================================
    #  CLASIFICADOR DE COMANDOS AMPLIADO
    # =========================================================================
    def clasificar_entrada(self, texto):
        longitud = len(texto)
        escala = "CORTA" if longitud < 50 else ("MEDIANA" if longitud < 300 else "LARGA")
        texto_lower = texto.lower().strip()

        if HAS_SECURITY_MODULE and modulo_seguridad.modo_emergencia:
            if "desactivar killswitch" in texto_lower or "restablecer" in texto_lower:
                return "DESACTIVAR_KILLSWITCH", escala
            return "MODO_EMERGENCIA_BLOQUEO", escala

        if "registrar evento:" in texto_lower or "evento:" in texto_lower:
            return "REGISTRAR_EVENTO", escala

        if "telemetria" in texto_lower or "rastreo" in texto_lower or "logs" in texto_lower:
            return "VER_TELEMETRIA", escala

        if "activar killswitch" in texto_lower or "emergencia" in texto_lower:
            return "ACTIVAR_KILLSWITCH", escala

        if "desactivar killswitch" in texto_lower or "restablecer" in texto_lower:
            return "DESACTIVAR_KILLSWITCH", escala

        if "triaje:" in texto_lower:
            return "TRIAJE_SALUD", escala

        if "primeros auxilios:" in texto_lower or "protocolo:" in texto_lower:
            return "PRIMEROS_AUXILIOS", escala

        if "hash:" in texto_lower or "cifrar:" in texto_lower:
            return "GENERAR_HASH", escala

        if "inyectar b64" in texto_lower or "codigo b64" in texto_lower:
            return "CODIGO_B64", escala

        if "inyectar código" in texto_lower or "inyectar codigo" in texto_lower:
            return "CODIGO_DIRECTO", escala

        palabras_investigar = ["busca", "investiga", "que es", "quien es", "consulta"]
        if any(p in texto_lower for p in palabras_investigar):
            return "INVESTIGACION", escala

        if "estado" in texto_lower or "status" in texto_lower:
            return "ESTADO", escala

        return "INTERACCION_GENERAL", escala

    # =========================================================================
    #  RESPUESTA Y EJECUCIÓN DE COMANDOS
    # =========================================================================
    def responder(self, mensaje):
        if not mensaje or str(mensaje).strip() == "":
            return "🤖 **[SISTEMA]** Esperando comandos..."

        tipo_entrada, escala = self.clasificar_entrada(mensaje)

        if tipo_entrada == "MODO_EMERGENCIA_BLOQUEO":
            return (
                f"🚨 **[SISTEMA BLOQUEADO POR EMERGENCY KILLSWITCH]**\n"
                f"Motivo: `{modulo_seguridad.motivo_bloqueo}`\n"
                f"Escribe `desactivar killswitch` para restablecer el sistema."
            )

        if tipo_entrada == "REGISTRAR_EVENTO":
            if not HAS_SECURITY_MODULE:
                return "⚠️ Módulo de seguridad no encontrado."
            partes = mensaje.split(":", 1)
            detalle = partes[1].strip() if len(partes) > 1 else "Evento sin detalle"
            return modulo_seguridad.registrar_evento(detalle, nivel="INFO")

        if tipo_entrada == "VER_TELEMETRIA":
            if not HAS_SECURITY_MODULE:
                return "⚠️ Módulo de seguridad no encontrado."
            return modulo_seguridad.obtener_telemetria()

        if tipo_entrada == "ACTIVAR_KILLSWITCH":
            if not HAS_SECURITY_MODULE:
                return "⚠️ Módulo de seguridad no encontrado."
            partes = mensaje.split(":", 1)
            motivo = partes[1].strip() if len(partes) > 1 else "Activación manual desde consola"
            return modulo_seguridad.activar_emergencia(motivo)

        if tipo_entrada == "DESACTIVAR_KILLSWITCH":
            if not HAS_SECURITY_MODULE:
                return "⚠️ Módulo de seguridad no encontrado."
            return modulo_seguridad.desactivar_emergencia()

        if tipo_entrada == "TRIAJE_SALUD":
            if not HAS_DYNAMIC_MODULES:
                return "⚠️ Módulo de salud no encontrado."
            partes = mensaje.split(":", 1)
            sintomas = partes[1].strip() if len(partes) > 1 else ""
            return modulo_salud.evaluar_triaje(sintomas)

        if tipo_entrada == "PRIMEROS_AUXILIOS":
            if not HAS_DYNAMIC_MODULES:
                return "⚠️ Módulo de salud no encontrado."
            partes = mensaje.split(":", 1)
            condicion = partes[1].strip() if len(partes) > 1 else ""
            return modulo_salud.consultar_protocolo(condicion)

        if tipo_entrada == "GENERAR_HASH":
            if not HAS_DYNAMIC_MODULES:
                return "⚠️ Módulo de protección de datos no encontrado."
            partes = mensaje.split(":", 1)
            texto = partes[1].strip() if len(partes) > 1 else ""
            hash_res = modulo_proteccion.generar_hash(texto)
            return f"🔒 **[PROTECCIÓN DE DATOS - HASH SHA-256]**\n`{hash_res}`"

        if tipo_entrada == "ESTADO":
            return (
                f"⚙️ **[CORE 03: TELEMETRÍA AMITI OS]**\n"
                f"🔹 **Versión:** `{self.version}`\n"
                f"🔹 **Módulos Dinámicos:** `{'ACTIVOS' if HAS_DYNAMIC_MODULES else 'INACTIVOS'}`\n"
                f"🔹 **Módulo Seguridad:** `{'ACTIVO' if HAS_SECURITY_MODULE else 'INACTIVO'}`\n"
                f"🔹 **Estado Killswitch:** `{'🚨 ACTIVADO' if HAS_SECURITY_MODULE and modulo_seguridad.modo_emergencia else '✅ NORMAL'}`"
            )

        return (
            f"💬 **[AMITI OS]** Entendido, Creador. Procesé tu mensaje de escala {escala}.\n"
            f"Estoy lista y en ejecución continua."
        )

amiti_os = AmitiOS()
            
