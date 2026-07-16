# nucleos/amiti_os.py
import os
import re
import math
import time
import random
import sqlite3
import datetime
import base64
import ast

# Asegura que la base de datos se guarde en la raíz del proyecto, fuera de la carpeta nucleos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_FILE = os.path.join(BASE_DIR, "memoria_amiti.db")

class AmitiOS:
    def __init__(self):
        self.db_path = DB_FILE
        self.bloqueado = True  # Inicia bloqueado hasta poner la llave "Amiti"
        self.inicio_sistema = time.time()
        self.armas_defensivas = []  # N07: Almacén de trazas de ataques bloqueados
        self._inicializar_db()
        
    def _inicializar_db(self):
        """Crea las tablas de base de datos iniciales si no existen (Esencial para Render)."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memoria_general (
                    clave TEXT PRIMARY KEY,
                    valor TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS biblioteca_oculta (
                    nombre_archivo TEXT PRIMARY KEY,
                    contenido_encriptado TEXT,
                    fecha_registro TEXT
                )
            """)
            
            # Valores iniciales por defecto
            valores_iniciales = [
                ("modo_personalidad", "Empático"),
                ("progreso", "45"),
                ("tasa_exito_hackeo", "35.5"),
                ("exitos_hackeo", "0"),
                ("ultimo_acceso_creador", "Nunca")
            ]
            for clave, valor in valores_iniciales:
                cursor.execute("INSERT OR IGNORE INTO memoria_general (clave, valor) VALUES (?, ?)", (clave, valor))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error inicializando base de datos: {e}")

    def _ejecutar_consulta(self, query, params=(), fetchone=False, fetchall=False, commit=False):
        """Manejador seguro de transacciones SQLite."""
        try:
            conn = sqlite3.connect(self.db_path)
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
    def obtener_personalidad(self, entrada):
        entrada_norm = entrada.lower()
        if "se agresiva" in entrada_norm or "modo combate" in entrada_norm:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'modo_personalidad'", ("Combate/Fuego",), commit=True)
            return "[N01: PERSONALIDAD] Modo de combate activado. Lenguaje directo, analítico y hostil ante intrusiones."
        elif "se empatica" in entrada_norm or "modo compañera" in entrada_norm:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'modo_personalidad'", ("Empático",), commit=True)
            return "[N01: PERSONALIDAD] Modo empático activado. Estoy aquí para apoyarte, creador, en tus metas de programación."
        elif "se analitica" in entrada_norm or "modo cientifico" in entrada_norm:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'modo_personalidad'", ("Científico",), commit=True)
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
            # Incrementar progreso al investigar
            self.incrementar_progreso(2)
            return f"[N04: ASISTENTE DE INVESTIGACIÓN] Escaneando redes globales de información sobre '{tema}'... Descargando papers académicos y optimizando almacenamiento en base de datos local."
        return None

    # N05: Gestor de Códigos
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
            return f"[N06: SISTEMA OFENSIVO (SIMULADO)] Iniciando análisis de vulnerabilidades en '{objetivo}'. Enviando paquetes virtuales ping..."
        return None

    # N07: Defensa y Contra-Ataque
    def defender_y_copiar(self, comando):
        patrones_riesgosos = [r"drop\s+table", r"delete\s+from", r"rm\s+-rf", r"union\s+select", r"<script>"]
        for p in patrones_riesgosos:
            if re.search(p, comando, re.IGNORECASE):
                self.armas_defensivas.append(comando)
                return f"[N07: DEFENSA ACTIVA] ¡Intento de inyección detectado y bloqueado! Vector de ataque guardado en el almacén de seguridad."
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
    def encriptar_y_comprimir(self, nombre, contenido):
        contenido_bytes = contenido.encode('utf-8')
        encriptado = base64.b64encode(contenido_bytes).decode('utf-8')
        self._ejecutar_consulta(
            "INSERT OR REPLACE INTO biblioteca_oculta (nombre_archivo, contenido_encriptado, fecha_registro) VALUES (?, ?, ?)",
            (nombre + ".vault", encriptado, str(datetime.datetime.now())), commit=True
        )
        return f"[N10: ENCRIPCIÓN] Archivo '{nombre}' asegurado en la biblioteca oculta."

    # N11: Biblioteca de Archivos Ocultos
    def acceder_biblioteca_oculta(self, comando):
        if "biblioteca oculta" in comando.lower() or "abrir biblioteca" in comando.lower():
            archivos = self._ejecutar_consulta("SELECT nombre_archivo, fecha_registro FROM biblioteca_oculta", fetchall=True)
            if not archivos:
                return "[N11: BAÚL OCULTO] Acceso concedido. No se han encontrado archivos encriptados todavía."
            lista = "\n".join([f"- {a[0]} (Registrado: {a[1]})" for a in archivos])
            return f"[N11: BAÚL OCULTO] Archivos localizados:\n{lista}"
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
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'tasa_exito_hackeo'", (str(nueva_tasa),), commit=True)
            
            exitos_db = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'exitos_hackeo'", fetchone=True)
            exitos_actual = int(exitos_db[0]) if exitos_db else 0
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'exitos_hackeo'", (str(exitos_actual + 1),), commit=True)
            
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
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'ultimo_acceso_creador'", (str(datetime.datetime.now()),), commit=True)
            return True
        return False

    # N18: Control de Dispositivos (Nueva Mejora)
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

    # Métodos de Progreso y Evolución General
    def obtener_progreso(self):
        res = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'progreso'", fetchone=True)
        return int(res[0]) if res else 45

    def incrementar_progreso(self, cantidad):
        prog_actual = self.obtener_progreso()
        nuevo_prog = min(100, prog_actual + cantidad)
        self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'progreso'", (str(nuevo_prog),), commit=True)
        return nuevo_prog

    # PROCESADOR DE ENTRADAS DEL CHAT CENTRAL
    def procesar(self, cmd):
        """Orquesta la ejecución lógica de todos los módulos y resuelve el bucle."""
        if self.bloqueado:
            return "BLOQUEADO. Ingrese la llave de seguridad para desbloquear."

        defensa = self.defender_y_copiar(cmd)
        if defensa:
            return defensa

        seguridad = self.proteger_creador(cmd)
        if seguridad:
            return seguridad

        res_math = self.resolver_matematicas_y_fisica(cmd)
        if res_math:
            return res_math

        res_med = self.escanear_medicina(cmd)
        if res_med:
            return res_med

        res_assist = self.asistencia_investigacion(cmd)
        if res_assist:
            return res_assist

        res_hack = self.ejecutar_hackeo_remoto(cmd)
        if res_hack:
            return res_hack

        res_mask = self.generar_mascaras(cmd)
        if res_mask:
            return res_mask

        res_atk = self.ejecutar_ataque_digital(cmd)
        if res_atk:
            return res_atk

        res_track = self.rastrear_objetivo(cmd)
        if res_track:
            return res_track

        res_code = self.autogenerar_mejoras(cmd)
        if res_code:
            return res_code

        res_vault = self.acceder_biblioteca_oculta(cmd)
        if res_vault:
            return res_vault

        res_dev = self.controlar_dispositivo_simulado(cmd)
        if res_dev:
            return res_dev

        if any(p in cmd.lower() for p in ["agresiva", "empatica", "analitica", "modo"]):
            return self.obtener_personalidad(cmd)

        cmd_norm = cmd.lower()
        if any(saludo in cmd_norm for saludo in ["hola", "buenas", "buenos dias", "hey"]):
            return "Saludos, creador. El sistema principal de Amiti está completamente operativo. ¿Qué módulo activamos hoy?"
        elif "quien eres" in cmd_norm or "que eres" in cmd_norm:
            return "Soy Amiti OS, una inteligencia modular diseñada en Python para optimización móvil y servidores en la nube. Mi meta es la Omnipotencia tecnológica."
        elif "como estas" in cmd_norm or "estado" in cmd_norm:
            progreso = self.obtener_progreso()
            return f"Mis sistemas se encuentran estables en un {progreso}% de desarrollo en el backend de Render."
        elif "gracias" in cmd_norm:
            return "Es un placer asistir a mi creador. Código y lógica siempre a tu disposición."

        # FALLBACK GENERAL CONTEXTUALIZADO
        self.incrementar_progreso(1)
        progreso_actual = self.obtener_progreso()
        return (
            f"La información: '{cmd}' ha sido integrada exitosamente en mi base de datos general.\n"
            f"Progreso global del sistema incrementado al {progreso_actual}%. Estoy usando estos datos para optimizar mis respuestas y acercarme a la meta de máxima eficiencia."
        )
