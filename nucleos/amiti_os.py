# nucleos/amiti_os.py
import os
import re
import math
import time
import random
import psycopg2
from psycopg2.extras import DictCursor
import datetime
import base64

class AmitiOS:
    def __init__(self):
        # Lee de forma automática el enlace de Neon guardado en el entorno de Render
        self.db_url = os.environ.get("DATABASE_URL")
        self.bloqueado = True  # Inicia bloqueado hasta recibir la llave "Amiti"
        self.inicio_sistema = time.time()
        self.armas_defensivas = []  # N07: Almacén de trazas de ataques bloqueados
        self._inicializar_db()
        
    def _inicializar_db(self):
        """Crea las tablas de base de datos iniciales en la nube si no existen."""
        if not self.db_url:
            print("[ALERTA] No se detectó la variable DATABASE_URL externa.")
            return

        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            
            # Tabla memoria general
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memoria_general (
                    clave TEXT PRIMARY KEY,
                    valor TEXT
                )
            """)
            
            # Tabla biblioteca oculta
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS biblioteca_oculta (
                    nombre_archivo TEXT PRIMARY KEY,
                    contenido_encriptado TEXT,
                    fecha_registro TEXT
                )
            """)
            
            # N08: Tabla de aprendizaje continuo
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS aprendizaje (
                    id SERIAL PRIMARY KEY,
                    dato TEXT,
                    fecha_registro TEXT
                )
            """)
            
            # Valores iniciales por defecto (Adaptado con ON CONFLICT para PostgreSQL)
            valores_iniciales = [
                ("modo_personalidad", "Empático"),
                ("progreso", "45"),
                ("tasa_exito_hackeo", "35.5"),
                ("exitos_hackeo", "0"),
                ("ultimo_acceso_creador", "Nunca")
            ]
            for clave, valor in valores_iniciales:
                cursor.execute("""
                    INSERT INTO memoria_general (clave, valor) 
                    VALUES (%s, %s) 
                    ON CONFLICT (clave) DO NOTHING
                """, (clave, valor))
            
            conn.commit()
            conn.close()
            print("[INFO] Conexión estable con el clúster de Neon DB.")
        except Exception as e:
            print(f"Error inicializando base de datos en la nube: {e}")

    def _ejecutar_consulta(self, query, params=(), fetchone=False, fetchall=False, commit=False):
        """Manejador seguro de transacciones PostgreSQL en la nube."""
        if not self.db_url:
            return "Error de DB: Sin conexión a la red de Neon."
        try:
            # Traductor automático: Convierte comodines '?' de SQLite al formato '%s' de Postgres
            query = query.replace('?', '%s')
            
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            cursor.execute(query, params)
            res = None
            if fetchone:
                res = cursor.fetchone()
            elif fetchall:
                res = cursor.fetchall()
            if commit:
                conn.commit()
            conn.close()
            return res
        except Exception as e:
            return f"Error de DB: {str(e)}"

    # N01: Personalidad Autónoma
    def obtener_personalidad(self, entrada=""):
        entrada_norm = entrada.lower()
        if "se agresiva" in entrada_norm or "modo combate" in entrada_norm:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'modo_personalidad'", ("Combate/Fuego",), commit=True)
            return "[N01: PERSONALIDAD] Modo de combate activado. Lenguaje directo, analítico y hostil ante intrusiones."
        elif "se empatica" in entrada_norm or "modo compañera" in entrada_norm:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'modo_personalidad'", ("Empático",), commit=True)
            return "[N01: PERSONALIDAD] Modo empático activado. Estoy aquí para apoyarte, creador, en tus metas de programación."
        elif "se analitica" in entrada_norm or "modo cientifico" in entrada_norm:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'modo_personalidad'", ("Científico",), commit=True)
            return "[N01: PERSONALIDAD] Modo analítico activado. Priorizando la lógica rigurosa y las respuestas optimizadas."

        modo = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'modo_personalidad'", fetchone=True)
        return modo[0] if modo else "Omnipotente"

    # N02: Protección al Creador
    def proteger_creador(self, entrada):
        if any(palabra in entrada.lower() for palabra in ["peligro", "amenaza", "ataque fisico", "extorsion", "emergencia"]):
            return "[N02: ALERTA DE SEGURIDAD] ¡Peligro detectado! Desplegando escudo de red móvil. Generando alertas falsas de geolocalización para proteger tu ubicación real."
        return None

    # N03: Conocimiento de Medicina y Signos Vitales
    def escanear_medicina(self, entrada):
        entrada_norm = entrada.lower()
        if "anemia" in entrada_norm and "drepanocitica" in entrada_norm or "fisiopatologia" in entrada_norm:
            return (
                "[N03: MEDICINA] Fisiopatología de la Anemia Drepanocítica:\n"
                "Se produce por una mutación puntual en el gen de la beta-globina (sustitución de ácido glutámico por valina en la posición 6).\n"
                "Bajo condiciones de hipoxia, la hemoglobina anormal (HbS) se polimeriza, causando rigidez en el glóbulo rojo, deformación en hoz (drepanocitos), oclusión microvascular y hemólisis crónica."
            )
        elif "cirugia" in entrada_norm or "schwartz" in entrada_norm:
            return (
                "[N03: CIRUGÍA] Principios Generales de Cirugía (Schwartz):\n"
                "1. Control estricto de la hemostasia para evitar shock.\n"
                "2. Conservación del suministro sanguíneo tisular.\n"
                "3. Asepsia y antisepsia rigurosas.\n"
                "4. Manejo delicado de tejidos para una cicatrización adecuada."
            )
        elif "signos vitales" in entrada_norm:
            return "[N03: TELEMETRÍA] Estado simulado del creador: Temperatura: 36.5°C, Frecuencia Cardíaca: 72 lpm, SpO2: 98%. Signos estables y óptimos."
        return None

    # N04: Asistencia Inteligente
    def asistencia_investigacion(self, consulta):
        if "investiga" in consulta.lower() or "busca" in consulta.lower():
            tema = consulta.lower().replace("investiga", "").replace("busca", "").strip()
            self.incrementar_progreso(2)
            return f"[N04: ASISTENTE DE INVESTIGACIÓN] Escaneando redes globales de información sobre '{tema}'... Descargando papers académicos y optimizando almacenamiento en la base de datos en la nube."
        return None

    # N05: Gestor de Códigos Básicos
    def autogenerar_mejoras(self, entrada):
        if "crea codigo" in entrada.lower() or "genera funcion" in entrada.lower():
            return (
                "[N05: AUTO-DESARROLLADOR] Generando andamio lógico para tu nueva función móvil:\n\n"
                "def nueva_funcion_amiti(*args, **kwargs):\n"
                "    try:\n"
                "        # Bloque optimizado de procesamiento de datos\n"
                "        resultado = sum(args)\n"
                "        return {'status': 'success', 'data': resultado}\n"
                "    except Exception as e:\n"
                "        return {'status': 'error', 'msg': str(e)}\n"
            )
        return None

    # N06: Ataque Digital (Simulación Educativa)
    def ejecutar_ataque_digital(self, entrada):
        if "ataca" in entrada.lower() or "derribar" in entrada.lower():
            objetivo = entrada.lower().replace("ataca", "").replace("derribar", "").strip()
            return f"[N06: SISTEMA OFENSIVO (SIMULADO)] Iniciando análisis de vulnerabilidades en '{objetivo}'. Enviando paquetes virtuales ping a los puertos lógicos..."
        return None

    # N07: Defensa y Contra-Ataque
    def defender_y_copiar(self, comando):
        patrones_riesgosos = [r"drop\s+table", r"delete\s+from", r"rm\s+-rf", r"union\s+select", r"<script>"]
        for p in patrones_riesgosos:
            if re.search(p, comando, re.IGNORECASE):
                self.armas_defensivas.append(comando)
                return f"[N07: DEFENSA ACTIVA] ¡Intento de inyección o comando peligroso detectado y bloqueado! Vector guardado en el almacén de seguridad."
        return None

    # N08: Sistema de Aprendizaje Autónomo Persistente
    def registrar_aprendizaje(self, entrada):
        entrada_norm = entrada.lower()
        if "aprende" in entrada_norm or "memoriza" in entrada_norm:
            dato_util = entrada.replace("aprende", "").replace("memoriza", "").strip()
            if not dato_util:
                return "[N08: APRENDIZAJE] Especifica qué dato deseas que indexe en mi memoria."
            
            fecha_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._ejecutar_consulta(
                "INSERT INTO aprendizaje (dato, fecha_registro) VALUES (%s, %s)", 
                (dato_util, fecha_str), 
                commit=True
            )
            self.incrementar_progreso(1)
            return f"[N08: APRENDIZAJE] Registro indexado de forma autónoma en Neon DB: '{dato_util}' a las {fecha_str}."
        
        if "recuerda datos" in entrada_norm or "ver aprendizaje" in entrada_norm:
            registros = self._ejecutar_consulta("SELECT dato, fecha_registro FROM aprendizaje ORDER BY id DESC LIMIT 5", fetchall=True)
            if not registros:
                return "[N08: APRENDIZAJE] Los clústeres de conocimiento están vacíos por ahora."
            lista = "\n".join([f"• [{r[1]}] {r[0]}" for r in registros])
            return f"[N08: APRENDIZAJE] Últimos conocimientos consolidados en mi base de datos:\n{lista}"
        return None

    # N09: Matemático y Física Lógica
    def resolver_matematicas_y_fisica(self, entrada):
        entrada_limpia = entrada.lower().strip()
        
        if "raiz" in entrada_limpia or "raíz" in entrada_limpia:
            nums = re.findall(r'\d+', entrada_limpia)
            if nums:
                n = float(nums[0])
                return f"[N09: MATEMÁTICAS] La raíz cuadrada de {n} es {math.sqrt(n)}."

        if "fuerza" in entrada_limpia:
            match = re.search(r'm\s*=\s*(\d+(\.\d+)?).*a\s*=\s*(\d+(\.\d+)?)', entrada_limpia)
            if match:
                m = float(match.group(1))
                a = float(match.group(3))
                return f"[N09: FÍSICA] Fuerza calculada (F = m * a):\nFuerza = {m} kg * {a} m/s² = {m * a} Newtons (N)."

        if "velocidad" in entrada_limpia:
            match = re.search(r'd\s*=\s*(\d+(\.\d+)?).*t\s*=\s*(\d+(\.\d+)?)', entrada_limpia)
            if match:
                d = float(match.group(1))
                t = float(match.group(3))
                if t == 0:
                    return "[N09: FÍSICA] Error: El tiempo no puede ser cero."
                return f"[N09: FÍSICA] Velocidad calculada (v = d / t):\nVelocidad = {d} m / {t} s = {d/t:.2f} m/s."

        caracteres_validos = set("0123456789+-*/(). ")
        if all(c in caracteres_validos for c in entrada_limpia) and any(op in entrada_limpia for op in "+-*/") and len(entrada_limpia) > 2:
            try:
                resultado = eval(entrada_limpia, {"__builtins__": None}, {})
                return f"[N09: MATEMÁTICAS] Cálculo resuelto: {entrada_limpia} = {resultado}"
            except Exception as e:
                return f"[N09: ERROR] Error de sintaxis en expresión matemática: {str(e)}"

        return None

    # N10: Encriptación y Compresión
    def encriptar_y_comprimir(self, entrada):
        if "encripta" in entrada.lower():
            partes = entrada.split(":")
            if len(partes) < 3:
                return "[N10: ENCRIPCIÓN] Formato inválido. Usa: 'encripta:nombre_archivo:contenido del archivo'"
            nombre = partes[1].strip()
            contenido = partes[2].strip()
            
            contenido_bytes = contenido.encode('utf-8')
            encriptado = base64.b64encode(contenido_bytes).decode('utf-8')
            self._ejecutar_consulta("""
                INSERT INTO biblioteca_oculta (nombre_archivo, contenido_encriptado, fecha_registro) 
                VALUES (%s, %s, %s)
                ON CONFLICT (nombre_archivo) 
                DO UPDATE SET contenido_encriptado = EXCLUDED.contenido_encriptado, fecha_registro = EXCLUDED.fecha_registro
            """, (nombre + ".vault", encriptado, str(datetime.datetime.now())), commit=True)
            return f"[N10: ENCRIPCIÓN] Archivo '{nombre}.vault' asegurado y sincronizado con Neon DB."
        return None

    # N11: Biblioteca de Archivos Ocultos
    def acceder_biblioteca_oculta(self, comando):
        if "biblioteca oculta" in comando.lower() or "abrir biblioteca" in comando.lower():
            archivos = self._ejecutar_consulta("SELECT nombre_archivo, fecha_registro FROM biblioteca_oculta", fetchall=True)
            if not archivos:
                return "[N11: BAÚL OCULTO] Acceso concedido. No se han encontrado archivos encriptados todavía."
            lista = "\n".join([f"- {a[0]} (Registrado: {a[1]})" for a in archivos])
            return f"[N11: BAÚL OCULTO] Archivos localizados en la nube:\n{lista}"
        return None

    # N12: Rastreo y Localización (Simulado)
    def rastrear_objetivo(self, entrada):
        if "rastrea" in entrada.lower() or "localiza" in entrada.lower():
            objetivo = entrada.lower().replace("rastrea", "").replace("localiza", "").strip()
            lat = random.uniform(7.0, 10.0)
            lon = random.uniform(-68.0, -66.0)
            return f"[N12: LOCALIZADOR] Coordenadas estimadas de '{objetivo}': Latitud {lat:.6f}, Longitud {lon:.6f}."
        return None

    # N13: Hackeo Remoto (Simulación de Auditoría Interactiva)
    def ejecutar_hackeo_remoto(self, entrada):
        if "hackea" in entrada.lower():
            objetivo = entrada.lower().replace("hackea", "").strip()
            
            tasa_db = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'tasa_exito_hackeo'", fetchone=True)
            tasa_actual = float(tasa_db[0]) if tasa_db else 35.5
            nueva_tasa = min(100.0, tasa_actual + random.uniform(1.0, 3.5))
            self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'tasa_exito_hackeo'", (str(nueva_tasa),), commit=True)
            
            exitos_db = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'exitos_hackeo'", fetchone=True)
            exitos_actual = int(exitos_db[0]) if exitos_db else 0
            self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'exitos_hackeo'", (str(exitos_actual + 1),), commit=True)
            
            self.incrementar_progreso(1)

            return (
                f"[N13: AUDITORÍA DE RED (SIMULADA)] Objetivo: '{objetivo}'\n"
                "└─ [ESCANEANDO] Puertos lógicos simulados abiertos...\n"
                "└─ [CONEXIÓN] Inyectando payloads de prueba seguros...\n"
                f"└─ [RESULTADO] Acceso virtual exitoso. Tasa de optimización del núcleo sube a {nueva_tasa:.2f}%."
            )
        return None

    # N14: Enmascaramiento / Anonimato (Simulado)
    def generar_mascaras(self, entrada):
        if "genera mascara" in entrada.lower() or "ocultame" in entrada.lower() or "anonimato" in entrada.lower():
            ip_simulada = f"{random.randint(45,190)}.{random.randint(10,250)}.{random.randint(1,254)}.{random.randint(1,254)}"
            email_simulado = f"sec_core_amiti_{random.randint(100,999)}@safe-node.net"
            return f"[N14: ANONIMATO] IP virtual asignada: {ip_simulada} (Proxy). Correo temporal: {email_simulado}"
        return None

    # N15: Reconocimiento al Creador
    def validar_creador(self, llave):
        if llave == "Amiti":
            self.bloqueado = False
            self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'ultimo_acceso_creador'", (str(datetime.datetime.now()),), commit=True)
            return True
        return False

    # N16: Mantenimiento y Optimización Autónoma de Neon DB
    def ejecutar_auto_mantenimiento_db(self, entrada):
        if "optimiza base de datos" in entrada.lower() or "mantenimiento db" in entrada.lower():
            self._ejecutar_consulta("ANALYZE memoria_general;", commit=True)
            self._ejecutar_consulta("ANALYZE biblioteca_oculta;", commit=True)
            self._ejecutar_consulta("ANALYZE aprendizaje;", commit=True)
            return "[N16: MANTENIMIENTO AUTÓNOMO] Índices optimizados. Coincidencias de caché actualizadas en el clúster en la nube."
        return None

    # N17: Sub-núcleo Lingüístico Inteligente (Inglés Avanzado)
    def modulo_linguistico_ingles(self, entrada):
        entrada_norm = entrada.lower()
        if "traduce" in entrada_norm:
            frase = entrada.replace("traduce", "").strip()
            return f"[N17: LINGÜÍSTICA] Modo traducción instantánea activado para analizar la estructura semántica de: '{frase}'."
        elif "conjugacion" in entrada_norm or "verbo" in entrada_norm:
            return (
                "[N17: LINGÜÍSTICA] Tabla de referencia de verbos irregulares estructurada:\n"
                "• Present: Go    | Past: Went    | Past Participle: Gone\n"
                "• Present: Write | Past: Wrote   | Past Participle: Written\n"
                "• Present: Build | Past: Built   | Past Participle: Built"
            )
        return None

    # N18: Control de Dispositivos 
    def controlar_dispositivo_simulado(self, entrada):
        entrada_norm = entrada.lower()
        if "dispositivo" in entrada_norm or "controla" in entrada_norm or "conecta" in entrada_norm:
            dispositivo = entrada_norm.replace("controla", "").replace("conecta", "").replace("dispositivo", "").strip()
            if not dispositivo:
                dispositivo = "Servidor Secundario"
            return (
                f"[N18: CONTROL DE DISPOSITIVOS]\n"
                f"Enlazando con hardware: '{dispositivo.upper()}'...\n"
                f"├─ Estado: En línea y mapeado por Amiti.\n"
                f"└─ Acción: Optimizando rendimiento de interfaz."
            )
        return None

    # N19: Generador de Algoritmos Avanzados y Contabilidad Monetaria
    def generar_algoritmo_contable(self, entrada):
        entrada_norm = entrada.lower()
        if any(p in entrada_norm for p in ["crea algoritmo", "algoritmo de contabilidad", "sistema contable", "contabilidad monetaria"]):
            self.incrementar_progreso(2)
            return (
                "[N19: ALGORITMOS Y CONTABILIDAD MONETARIA] Estructura transaccional y balance financiero generado:\n\n"
                "```python\n"
                "class MotorContableMonetario:\n"
                "    def __init__(self, divisa_principal='USD'):\n"
                "        self.divisa = divisa_principal\n"
                "        self.historial = []\n"
                "        self.saldo_neto = 0.0\n"
                "        \n"
                "    def registrar_movimiento(self, flujo, monto, motivo):\n"
                "        \"\"\"Procesa y valida transacciones monetarias flotantes.\"\"\"\n"
                "        monto_limpio = round(float(monto), 2)\n"
                "        if flujo.lower() == 'ingr
