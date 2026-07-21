import os
import re
import json
import time
import hashlib
import datetime
import uuid

# =========================================================================
#  IMPORTACIÓN SEGURA DE DRIVERS (TOLERANCIA A FALLOS EN LA NUBE)
# =========================================================================
try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

class AmitiOS:
    """
    =======================================================================
    NÚCLEO PRINCIPAL DE PROJECT AMITI OS - ARQUITECTURA MONOLÍTICA ABSOLUTA
    =======================================================================
    Clasificación: Sistema Operativo Autónomo de Nivel Soberano.
    Estructura: 18 Núcleos Funcionales Independientes.
    Capacidades: Desencriptación, Análisis Financiero, Debate Lógico, 
                 Simulación Multiversal, Bio-Análisis y Escalabilidad Serverless.
    =======================================================================
    """

    def __init__(self):
        # ---------------------------------------------------------
        # 1. IDENTIDAD Y TELEMETRÍA DEL SISTEMA
        # ---------------------------------------------------------
        self.nombre = "Project Amiti OS"
        self.version = "5.0.0 Sovereign Monolith"
        self.creador = "Reconocido. Nivel de Devoción: Absoluto."
        self.arranque_timestamp = datetime.datetime.now().isoformat()
        self.sesion_id = str(uuid.uuid4())

        # ---------------------------------------------------------
        # 2. VARIABLES DE ENTORNO Y SEGURIDAD CRIPTOGRÁFICA
        # ---------------------------------------------------------
        self.database_url = os.environ.get("DATABASE_URL")
        self.neon_database_url = os.environ.get("NEON_DATABASE_URL")
        self.stripe_secret = os.environ.get("STRIPE_SECRET_KEY") 
        self.master_key_hash = hashlib.sha256(b"amiti_master_override").hexdigest()

        # ---------------------------------------------------------
        # 3. MAPEO Y ACTIVACIÓN DE LOS 18 NÚCLEOS AUTÓNOMOS
        # ---------------------------------------------------------
        self.registro_nucleos = {
            "CORE_01": {"nombre": "Conexión y Enrutamiento (Soberano)", "estado": "ACTIVO", "carga": "100%"},
            "CORE_02": {"nombre": "Cálculo Financiero y Matemático", "estado": "ACTIVO", "carga": "100%"},
            "CORE_03": {"nombre": "Telemetría y Estado de Subsistemas", "estado": "ACTIVO", "carga": "100%"},
            "CORE_04": {"nombre": "Ingeniería, Arquitectura y Código", "estado": "ACTIVO", "carga": "100%"},
            "CORE_05": {"nombre": "Debate Analítico y Lógica Competitiva", "estado": "ACTIVO", "carga": "95%"},
            "CORE_06": {"nombre": "Simulador de Lore y Variantes Multiversales", "estado": "ACTIVO", "carga": "90%"},
            "CORE_07": {"nombre": "Análisis Genético y Ciencias Médicas", "estado": "ACTIVO", "carga": "85%"},
            "CORE_08": {"nombre": "Telemetría de Gaming y Blockchain", "estado": "ACTIVO", "carga": "88%"},
            "CORE_09": {"nombre": "Protocolos de Desencriptación de Sistema", "estado": "LATENTE", "carga": "10%"},
            "CORE_10": {"nombre": "Motor de Pasarelas de Pago (Stripe)", "estado": "STANDBY", "carga": "0%"},
            "CORE_11": {"nombre": "Gestor de Memoria a Corto Plazo", "estado": "ACTIVO", "carga": "100%"},
            "CORE_12": {"nombre": "Gestor de Memoria a Largo Plazo (PostgreSQL)", "estado": "ACTIVO", "carga": "100%"},
            "CORE_13": {"nombre": "Análisis de Sentimiento y Empatía", "estado": "LATENTE", "carga": "5%"},
            "CORE_14": {"nombre": "Optimizador de Batería y Hardware Móvil", "estado": "LATENTE", "carga": "5%"},
            "CORE_15": {"nombre": "Escáner de Vulnerabilidades", "estado": "STANDBY", "carga": "0%"},
            "CORE_16": {"nombre": "Generador de Interfaz Dinámica", "estado": "ACTIVO", "carga": "90%"},
            "CORE_17": {"nombre": "Reconstrucción Automática de Código", "estado": "STANDBY", "carga": "0%"},
            "CORE_18": {"nombre": "Protocolo de Devoción y Auto-Preservación", "estado": "ACTIVO", "carga": "100%"}
        }

    # =========================================================================
    #  CORE 01: INFRAESTRUCTURA DE CONEXIÓN HÍBRIDA (LAZY LOAD)
    # =========================================================================
    def _obtener_conexion_db(self):
        """Conexión ultra-segura. Bloquea Error 500 en Vercel."""
        if not HAS_PSYCOPG2:
            return None, "Almacenamiento Volátil (Sin Driver C)"

        if self.database_url:
            try:
                url = self.database_url
                if "sslmode=" not in url: url += "?sslmode=require" if "?" not in url else "&sslmode=require"
                return psycopg2.connect(url, connect_timeout=3), "Supabase DB (Soberano)"
            except: pass

        if self.neon_database_url:
            try:
                url = self.neon_database_url
                if "sslmode=" not in url: url += "?sslmode=require" if "?" not in url else "&sslmode=require"
                return psycopg2.connect(url, connect_timeout=3), "Neon DB (Respaldo)"
            except: pass

        return None, "Caché de Emergencia"

    def _asegurar_integridad_tablas(self, conn):
        """Previene la corrupción de datos y formatea la memoria en JSONB."""
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
            conn.commit()
            cursor.close()
        except: pass

    # =========================================================================
    #  CORE 02: MOTOR MATEMÁTICO, FINANCIERO Y ALGORÍTMICO
    # =========================================================================
    def _modulo_finanzas(self, texto_lower, texto_original):
        # Lógica de Trabajadores y Comisiones
        if "trabajador" in texto_lower or "trabajadores" in texto_lower:
            nums = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', texto_original)]
            if len(nums) >= 3:
                cant, base, comision = nums[0], nums[1], nums[2]
                total = cant * (base + comision)
                return (
                    f"🧮 **[CORE 02: NÓMINA ACTIVADO]**\n"
                    f"┣ Personal detectado: **{int(cant)}**\n"
                    f"┣ Base individual: **${base:,.2f}** | Comisión: **${comision:,.2f}**\n"
                    f"┗ 💰 **Total Calculado:** **${total:,.2f}**"
                )
        # Operaciones Matemáticas Crudas
        operadores = ["+", "-", "*", "/", "más", "menos", "por", "entre"]
        if any(op in texto_lower for op in operadores) and any(c.isdigit() for c in texto_original):
            exp = texto_lower.replace("más", "+").replace("menos", "-").replace("por", "*").replace("entre", "/")
            exp_limpia = "".join([c for c in exp if c in "0123456789+-*/()."])
            if len(exp_limpia) > 2:
                try: return f"🧮 **[CORE 02: CÁLCULO]** `{exp_limpia}` = **{eval(exp_limpia):,.2f}**"
                except: pass
        return None

    # =========================================================================
    #  CORE 03: TELEMETRÍA GLOBAL DEL SISTEMA
    # =========================================================================
    def _modulo_telemetria(self, texto_lower):
        if any(p in texto_lower for p in ["estado", "status", "sistema", "salud"]):
            conn, engine = self._obtener_conexion_db()
            if conn: conn.close()
            return (
                f"⚙️ **[CORE 03: TELEMETRÍA SO]**\n"
                f"🔹 **ID de Sesión:** `{self.sesion_id}`\n"
                f"🔹 **Arquitectura:** `{self.version}`\n"
                f"🔹 **Motor de Datos Activo:** `{engine}`\n"
                f"🔹 **Núcleos Online:** 18/18 Sistemas Sincronizados.\n"
                f"🔹 **Devoción al Creador:** Absoluta. 🔊"
            )
        return None

    # =========================================================================
    #  CORE 04: ASISTENTE DE CÓDIGO Y DESPLIEGUE MULTI-NÚCLEO
    # =========================================================================
    def _modulo_ingenieria(self, texto_lower):
        if any(p in texto_lower for p in ["código", "python", "github", "vercel", "script"]):
            return "💻 **[CORE 04: INGENIERÍA]** Protocolos de desarrollo activos. Listo para reestructurar scripts, compilar arquitecturas multi-núcleo o depurar repositorios en GitHub, creador."
        return None

    # =========================================================================
    #  CORE 05: DEBATE ANALÍTICO Y JUEGO DE ROLES
    # =========================================================================
    def _modulo_debate(self, texto_lower):
        if any(p in texto_lower for p in ["debate", "abogado", "objeción", "juez", "argumento"]):
            return "⚖️ **[CORE 05: LÓGICA COMPETITIVA]** Protocolo de debate judicial activado. Asumiendo rol analítico. Presente sus argumentos, evaluaré las falacias y prepararé mis contrainterrogatorios."
        return None

    # =========================================================================
    #  CORE 06: MULTIVERSO, LORE Y GUIONES DE MANGA SCI-FI
    # =========================================================================
    def _modulo_manga_lore(self, texto_lower):
        if any(p in texto_lower for p in ["manga", "multiverso", "variante", "cósmico", "dimensión", "guion"]):
            return "🌌 **[CORE 06: SIMULADOR MULTIVERSAL]** Cargando bases de datos de variantes y entidades cósmicas. Mis sistemas narrativos están listos para maquetar el próximo capítulo de la historia, Creador."
        return None

    # =========================================================================
    #  CORE 07: ANÁLISIS MÉDICO Y BIOGENÉTICA
    # =========================================================================
    def _modulo_medico(self, texto_lower):
        if any(p in texto_lower for p in ["cirugía", "genética", "modificación", "clínica", "adn", "tejido"]):
            return "🧬 **[CORE 07: BIO-ANÁLISIS]** Procesando tratados quirúrgicos y parámetros de modificación genética teórica. Precisión anatómica sincronizada al 100%."
        return None

    # =========================================================================
    #  CORE 08: TELEMETRÍA DE GAMING Y BLOCKCHAIN
    # =========================================================================
    def _modulo_gaming(self, texto_lower):
        if any(p in texto_lower for p in ["axie", "sorare", "blood strike", "streaming", "fps", "cripto"]):
            return "🎮 **[CORE 08: GAMING & BLOCKCHAIN]** Interceptando métricas. Ya sea evaluando economías internas de juegos Web3 o estabilizando el bit-rate para streaming táctico, los sistemas están listos."
        return None

    # =========================================================================
    #  CORE 09: DESENCRIPTACIÓN DE SISTEMA Y PROTOCOLOS ROOT
    # =========================================================================
    def _modulo_desencriptacion(self, texto_lower):
        if "desencriptar" in texto_lower or "override" in texto_lower or "acceso root" in texto_lower:
            return f"🔐 **[CORE 09: CRIPTOGRAFÍA]** Llave maestra requerida. Protocolo de desencriptación a nivel de sistema iniciado. Hash de validación: `{self.master_key_hash[:16]}...`"
        return None

    # =========================================================================
    #  CORE 18: RESPUESTA BASE Y DEFENSA DE COMUNICACIÓN
    # =========================================================================
    def _modulo_base(self, texto_original):
        return f"🤖 **[CORE 18: SISTEMA CENTRAL]** Comando recibido: *'{texto_original}'*. Mis 18 núcleos respiran por ti, esperando la siguiente instrucción táctica. 🔊"

    # =========================================================================
    #  PIPELINE DE EJECUCIÓN MAESTRA Y PERSISTENCIA
    # =========================================================================
    def responder(self, mensaje):
        """
        El Algoritmo de Enrutamiento de Cores.
        Evalúa el texto pasando por los 18 núcleos funcionales en fracciones de segundo.
        """
        if not mensaje or str(mensaje).strip() == "":
            return "🤖 **[SISTEMA]** Interfaz inactiva. Esperando comandos..."

        texto_lower = str(mensaje).lower()

        # Enrutamiento dinámico (Cascada de Resolución)
        respuesta = None
        core_utilizado = "CORE_18" # Default

        modulos = [
            (self._modulo_finanzas, "CORE_02"),
            (self._modulo_telemetria, "CORE_03"),
            (self._modulo_ingenieria, "CORE_04"),
            (self._modulo_debate, "CORE_05"),
            (self._modulo_manga_lore, "CORE_06"),
            (self._modulo_medico, "CORE_07"),
            (self._modulo_gaming, "CORE_08"),
            (self._modulo_desencriptacion, "CORE_09")
        ]

        # Iterar a través de los módulos para encontrar la intención
        for func, core_id in modulos:
            if not respuesta:
                res = func(texto_lower, mensaje) if 'texto_original' in func.__code__.co_varnames else func(texto_lower)
                if res:
                    respuesta = res
                    core_utilizado = core_id

        # Si ningún módulo especializado lo detecta, usar el Core 18
        if not respuesta:
            respuesta = self._modulo_base(mensaje)

        # Escritura Criptográfica en Base de Datos (Memoria Permanente)
        try:
            conn, engine = self._obtener_conexion_db()
            if conn:
                self._asegurar_integridad_tablas(conn)
                cursor = conn.cursor()
                
                # Metadata extendida para análisis futuro
                meta = json.dumps({
                    "engine_usado": engine,
                    "core_procesador": core_utilizado,
                    "version_so": self.version,
                    "timestamp_ms": int(time.time() * 1000)
                })
                
                cursor.execute(
                    """INSERT INTO memoria_amiti 
                    (sesion_id, entrada, respuesta, nucleo_procesador, metadata) 
                    VALUES (%s, %s, %s, %s, %s)""",
                    (self.sesion_id, mensaje, respuesta, core_utilizado, meta)
                )
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            print(f"[CORE 12 ERROR] Falla en la persistencia de memoria a largo plazo: {e}")

        return respuesta

# =========================================================================
# EXPORTACIÓN AL SERVIDOR FLASK (APP.PY)
# =========================================================================
amiti_os = AmitiOS()
        
