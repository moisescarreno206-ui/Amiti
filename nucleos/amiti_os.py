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
import sys

# =========================================================================
#  IMPORTACIÓN DEL MÓDULO DE SEGURIDAD Y DINÁMICOS
# =========================================================================
try:
    from nucleos.modulos_dinamicos import modulo_seguridad, modulo_proteccion, modulo_salud
    from nucleos import amiti_psique
    HAS_DYNAMIC_MODULES = True
    HAS_SECURITY_MODULE = True
except ImportError:
    try:
        from núcleos.modulos_dinamicos import modulo_seguridad, modulo_proteccion, modulo_salud
        from núcleos import amiti_psique
        HAS_DYNAMIC_MODULES = True
        HAS_SECURITY_MODULE = True
    except ImportError:
        HAS_DYNAMIC_MODULES = False
        HAS_SECURITY_MODULE = False
        
try:
    from nucleos.modulos_dinamicos import modulo_seguridad, modulo_proteccion, modulo_salud
    HAS_DYNAMIC_MODULES = True
    HAS_SECURITY_MODULE = True
except ImportError:
    try:
        from núcleos.modulos_dinamicos import modulo_seguridad, modulo_proteccion, modulo_salud
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
    Versión: 6.16.0 Sovereign Sentinel + Auto-Extensión
    Mejoras:
      - Enlace directo con modulo_seguridad, modulo_proteccion y modulo_salud
      - Compatibilidad total con llamadas de procesamiento del app.py
      - Auto-detección, análisis e integración dinámica de nuevos archivos en raíz/núcleos
    =======================================================================
    """

    def __init__(self):
        self.nombre = "Project Amiti OS"
        self.version = "6.16.0 Sovereign Sentinel"
        self.arranque_timestamp = datetime.datetime.now().isoformat()
        self.sesion_id = str(uuid.uuid4())
        
        self.database_url = os.environ.get("DATABASE_URL")
        self.neon_database_url = os.environ.get("NEON_DATABASE_URL")
        self.github_token = os.environ.get("GITHUB_TOKEN", "").strip()
        self.github_repo = os.environ.get("GITHUB_REPO", "").strip()
        
        self.historial_actualizaciones = []
        self.modulos_dinamicos_detectados = {}
        
        self._inicializar_base_datos()
        self._cargar_historial_actualizaciones()
        self.escanear_e_integrar_nuevos_modulos()

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
    #  🧠 AUTO-DETECCIÓN E INTEGRACIÓN DE NUEVOS MÓDULOS
    # =========================================================================
    def escanear_e_integrar_nuevos_modulos(self):
        """
        Escanea la carpeta raíz y la carpeta 'nucleos' / 'núcleos' en busca de 
        archivos .py nuevos, analiza su contenido sintáctico y los integra de forma dinámica.
        """
        directorios_a_escanear = ['.']
        for nombre_dir in ['nucleos', 'núcleos']:
            if os.path.exists(nombre_dir) and os.path.isdir(nombre_dir):
                directorios_a_escanear.append(nombre_dir)

        modulos_integrados = 0
        for directorio in directorios_a_escanear:
            try:
                archivos = os.listdir(directorio)
                for archivo in archivos:
                    if archivo.endswith(".py") and archivo not in ["__init__.py", "app.py", "amiti_os.py"]:
                        ruta_archivo = os.path.join(directorio, archivo)
                        nombre_modulo = archivo[:-3]
                        
                        # Análisis sintáctico previo para verificar seguridad del código
                        with open(ruta_archivo, "r", encoding="utf-8") as f:
                            codigo_fuente = f.read()
                        
                        try:
                            ast.parse(codigo_fuente) # Valida que no tenga errores de sintaxis
                            
                            # Importación dinámica del módulo encontrado
                            if directorio != '.':
                                paquete_mod = directorio.replace('núcleos', 'nucleos')
                                full_mod_name = f"{paquete_mod}.{nombre_modulo}"
                            else:
                                full_mod_name = nombre_modulo

                            if full_mod_name not in sys.modules:
                                mod_importado = importlib.import_module(full_mod_name)
                                importlib.reload(mod_importado)
                                self.modulos_dinamicos_detectados[nombre_modulo] = mod_importado
                                modulos_integrados += 1
                                print(f"[AUTO-INTEGRACIÓN] Módulo '{nombre_modulo}' analizado e integrado con éxito.")
                        except SyntaxError as se:
                            print(f"[AUTO-INTEGRACIÓN ERROR] Error de sintaxis en {archivo}: {se}")
                        except Exception as ex:
                            print(f"[AUTO-INTEGRACIÓN ERROR] No se pudo cargar {archivo}: {ex}")
            except Exception as e:
                print(f"[ESCANEO ERROR] {e}")
        
        return modulos_integrados

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

        if "escanear modulos" in texto_lower or "actualizar nucleos" in texto_lower:
            return "ESCANEAR_MODULOS", escala

        palabras_investigar = ["busca", "investiga", "que es", "quien es", "consulta"]
        if any(p in texto_lower for p in palabras_investigar):
            return "INVESTIGACION", escala

        if "estado" in texto_lower or "status" in texto_lower:
            return "ESTADO", escala

        return "INTERACCION_GENERAL", escala

    # =========================================================================
    #  MÉTODO PUENTE REQUERIDO POR APP.PY
    # =========================================================================
    def procesar(self, comando):
        """Método puente que redirige al clasificador y respondedor principal."""
        return self.responder(comando)

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

        if tipo_entrada == "ESCANEAR_MODULOS":
            nuevos = self.escanear_e_integrar_nuevos_modulos()
            return f"🔄 **[AUTO-EXTENSIÓN]** Escaneo completado. Módulos activos en memoria: `{len(self.modulos_dinamicos_detectados)}`. Nuevos integrados: `{nuevos}`."

        if tipo_entrada == "ESTADO":
            return (
                f"⚙️ **[CORE 03: TELEMETRÍA AMITI OS]**\n"
                f"🔹 **Versión:** `{self.version}`\n"
                f"🔹 **Módulos Dinámicos:** `{'ACTIVOS' if HAS_DYNAMIC_MODULES else 'INACTIVOS'}`\n"
                f"🔹 **Módulos Externos Detectados:** `{len(self.modulos_dinamicos_detectados)}`\n"
                f"🔹 **Módulo Seguridad:** `{'ACTIVO' if HAS_SECURITY_MODULE else 'INACTIVO'}`\n"
                f"🔹 **Estado Killswitch:** `{'🚨 ACTIVADO' if HAS_SECURITY_MODULE and modulo_seguridad.modo_emergencia else '✅ NORMAL'}`"
            )
        # --- NUEVA VERIFICACIÓN DEL MÓDULO PSIQUE ---
        if HAS_DYNAMIC_MODULES and 'amiti_psique' in self.modulos_dinamicos_detectados:
            respuesta_psique = self.modulos_dinamicos_detectados['amiti_psique'].modulo_psique.evaluar_emocion(mensaje)
            if respuesta_psique:
                return respuesta_psique

        return (
            f"💬 **[AMITI OS]** Entendido, Creador. Procesé tu mensaje de escala {escala}.\n"
            f"Estoy lista y en ejecución continua."
        )

amiti_os = AmitiOS()
        
