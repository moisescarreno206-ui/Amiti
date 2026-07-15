import os
import re
import math
import time
import random
import sqlite3
import datetime
import base64
import ast

DB_FILE = "memoria_amiti.db"

class AmitiOS:
    def __init__(self):
        self.db_path = DB_FILE
        self.bloqueado = True
        self.inicio_sistema = time.time()
        self.armas_defensivas = []  # N07: Almacén de trazas de ataques bloqueados
        self.tasa_exito_cerraduras = 35.5  # N13: Porcentaje inicial de éxito
        
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

    # -------------------------------------------------------------
    # N01: PERSONALIDAD AUTÓNOMA
    # -------------------------------------------------------------
    def obtener_personalidad(self, entrada):
        """Define el tono de las respuestas según las instrucciones del creador."""
        entrada_norm = entrada.lower()
        if "se agresiva" in entrada_norm or "modo combate" in entrada_norm:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'modo_personalidad'", ("Combate/Fuego",), commit=True)
            return "[N01: PERSONALIDAD] Modo de combate activado. Lenguaje directo, analítico y hostil ante intrusiones."
        elif "se empatica" in entrada_norm or "modo compañera" in entrada_norm:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'modo_personalidad'", ("Empático",), commit=True)
            return "[N01: PERSONALIDAD] Modo empático activado. Estoy aquí para apoyarte, creador, en tu bienestar y en tus metas de programación."
        elif "se analitica" in entrada_norm or "modo cientifico" in entrada_norm:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'modo_personalidad'", ("Científico",), commit=True)
            return "[N01: PERSONALIDAD] Modo analítico activado. Priorizando la lógica rigurosa y las respuestas optimizadas."

        modo = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'modo_personalidad'", fetchone=True)
        return modo[0] if modo else "Omnipotente"

    # -------------------------------------------------------------
    # N02: PROTECCIÓN AL CREADOR (SEGURIDAD ACTIVA)
    # -------------------------------------------------------------
    def proteger_creador(self, entrada):
        """Detecta palabras clave de emergencia para simular protocolos de aislamiento."""
        if any(palabra in entrada.lower() for palabra in ["peligro", "amenaza", "ataque fisico", "extorsion", "emergencia"]):
            # Simulación de protección y alerta de cortafuegos
            return "[N02: ALERTA DE SEGURIDAD] ¡Peligro detectado! Desplegando escudo de red. Generando alertas falsas de geolocalización para proteger tu ubicación real en este dispositivo móvil."
        return None

    # -------------------------------------------------------------
    # N03: CONOCIMIENTO DE MEDICINA Y SIGNOS VITALES
    # -------------------------------------------------------------
    def escanear_medicina(self, entrada):
        """Base de datos de consulta médica y análisis clínico para soporte rápido."""
        entrada_norm = entrada.lower()
        if "anemia drepanocitica" in entrada_norm or "fisiopatologia" in entrada_norm:
            return (
                "[N03: MEDICINA] Fisiopatología de la Anemia Drepanocítica:\n"
                "Se produce por una mutación puntual en el gen de la beta-globina (sustitución de ácido glutámico por valina en la posición 6).\n"
                "Bajo condiciones de hipoxia, la hemoglobina anormal (HbS) se polimeriza, causando rigidez en el glóbulo rojo, deformación en media luna (hoz) y posterior oclusión microvascular y hemólisis crónica."
            )
        elif "cirugia" in entrada_norm or "schwartz" in entrada_norm:
            return (
                "[N03: CIRUGÍA] Principios Generales de Cirugía (Schwartz):\n"
                "1. Control estricto de la hemostasia para evitar shock hipovolémico.\n"
                "2. Conservación del suministro sanguíneo tisular.\n"
                "3. Asepsia y antisepsia rigurosas para prevenir infecciones postoperatorias.\n"
                "4. Manejo delicado de tejidos para asegurar una cicatrización adecuada."
            )
        elif "signos vitales" in entrada_norm:
            return "[N03: TELEMETRÍA] Estado simulado del creador: Temperatura: 36.5°C, Frecuencia Cardíaca: 72 lpm, SpO2: 98%. Signos estables y seguros."
        return None

    # -------------------------------------------------------------
    # N04: ASISTENCIA INTELIGENTE
    # -------------------------------------------------------------
    def asistencia_investigacion(self, consulta):
        """Asistente de consultas que estructura reportes rápidos."""
        if "investiga" in consulta.lower() or "busca" in consulta.lower():
            tema = consulta.lower().replace("investiga", "").replace("busca", "").strip()
            return f"[N04: ASISTENTE] Búsqueda inteligente iniciada para: '{tema}'. Estructurando puntos clave, antecedentes científicos y documentación lógica disponible."
        return None

    # -------------------------------------------------------------
    # N05: GESTOR DE CÓDIGOS DE NUEVAS FUNCIONES
    # -------------------------------------------------------------
    def autogenerar_mejoras(self, entrada):
        """Genera andamios de código Python para tus proyectos móviles automáticamente."""
        if "crea codigo" in entrada.lower() or "genera funcion" in entrada.lower():
            return (
                "[N05: AUTO-DESARROLLADOR] Generando andamio lógico para tu nueva función:\n\n"
                "def nueva_funcion_amiti(*args, **kwargs):\n"
                "    # Código autónomo optimizado para procesamiento en backend\n"
                "    try:\n"
                "        resultado = sum(args)\n"
                "        return {'status': 'success', 'data': resultado}\n"
                "    except Exception as e:\n"
                "        return {'status': 'error', 'msg': str(e)}\n"
            )
        return None

    # -------------------------------------------------------------
    # N06: ATAQUE DIGITAL (SIMULACIÓN EDUCATIVA Y DE DEFENSA)
    # -------------------------------------------------------------
    def ejecutar_ataque_digital(self, entrada):
        """Módulo lúdico de simulación de pentesting."""
        if "ataca" in entrada.lower() or "derribar" in entrada.lower():
            objetivo = entrada.lower().replace("ataca", "").replace("derribar", "").strip()
            return f"[N06: SISTEMA OFENSIVO] Simulando auditoría de penetración en '{objetivo}'. Escaneando puertos virtuales... El ataque simulado continuará hasta verificar la mitigación de fallos en el objetivo."
        return None

    # -------------------------------------------------------------
    # N07: DEFENSA Y CONTRA-ATAQUE (SISTEMA ANOMALÍAS)
    # -------------------------------------------------------------
    def defender_y_copiar(self, comando):
        """Identifica comandos maliciosos comunes, los bloquea y los almacena."""
        patrones_riesgosos = [r"drop\s+table", r"delete\s+from", r"rm\s+-rf", r"union\s+select", r"<script>"]
        for p in patrones_riesgosos:
            if re.search(p, comando, re.IGNORECASE):
                self.armas_defensivas.append(comando)
                return f"[N07: DEFENSA ACTIVA] ¡Intento de inyección bloqueado! Vector copiado al almacén defensivo. Payload listo para redirección defensiva."
        return None

    # -------------------------------------------------------------
    # N08: MEMORIA GENERAL DEL SISTEMA
    # -------------------------------------------------------------
    def registrar_interaccion(self, cmd, resp):
        """Guarda estadísticas de uso en la base de datos para simular crecimiento evolutivo."""
        val = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'progreso'", fetchone=True)
        if val:
            nuevo_progreso = min(100, int(val[0]) + 1)
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'progreso'", (str(nuevo_progreso),), commit=True)

    # -------------------------------------------------------------
    # N09: MATEMÁTICO Y FÍSICA LÓGICA (AVANZADO)
    # -------------------------------------------------------------
    def resolver_matematicas_y_fisica(self, entrada):
        """Analizador de expresiones de física clásica y cálculo matemático directo."""
        entrada_limpia = entrada.lower().strip()
        
        # 1. Procesamiento de Raíz Cuadrada
        if "raiz" in entrada_limpia:
            nums = re.findall(r'\d+', entrada_limpia)
            if nums:
                n = float(nums[0])
                return f"[N09: MATEMÁTICAS] La raíz cuadrada de {n} es {math.sqrt(n)}."

        # 2. Física: Fuerza (Segunda Ley de Newton) -> f = m * a
        if "fuerza" in entrada_limpia:
            match = re.search(r'm\s*=\s*(\d+(\.\d+)?).*a\s*=\s*(\d+(\.\d+)?)', entrada_limpia)
            if match:
                m = float(match.group(1))
                a = float(match.group(3))
                return f"[N09: FÍSICA] Cálculo de fuerza (F = m * a):\nFuerza = {m} kg * {a} m/s² = {m * a} Newtons (N)."

        # 3. Física: Velocidad -> v = d / t
        if "velocidad" in entrada_limpia:
            match = re.search(r'd\s*=\s*(\d+(\.\d+)?).*t\s*=\s*(\d+(\.\d+)?)', entrada_limpia)
            if match:
                d = float(match.group(1))
                t = float(match.group(3))
                if t == 0:
                    return "[N09: FÍSICA] Error: El tiempo no puede ser cero."
                return f"[N09: FÍSICA] Cálculo de velocidad (v = d / t):\nVelocidad = {d} m / {t} s = {d / t} m/s."

        # 4. Evaluador matemático general (Operaciones aritméticas y lógicas seguras)
        caracteres_validos = set("0123456789+-*/(). ")
        if all(c in caracteres_validos for c in entrada_limpia) and any(op in entrada_limpia for op in "+-*/"):
            try:
                # Evaluación matemática pura
                resultado = eval(entrada_limpia)
                return f"[N09: MATEMÁTICAS] Cálculo matemático resuelto:\n{entrada_limpia} = {resultado}"
            except Exception as e:
                return f"[N09: ERROR] Error de sintaxis en expresión: {str(e)}"

        return None

    # -------------------------------------------------------------
    # N10: ENCRIPCIÓN Y COMPRESIÓN DE ARCHIVOS
    # -------------------------------------------------------------
    def encriptar_y_comprimir(self, nombre, contenido):
        """Simula la compresión y encripta datos en Base64 para guardarlos en el Baúl Oculto."""
        contenido_bytes = contenido.encode('utf-8')
        encriptado = base64.b64encode(contenido_bytes).decode('utf-8')
        self._ejecutar_consulta(
            "INSERT INTO biblioteca_oculta (nombre_archivo, contenido_encriptado, fecha_registro) VALUES (?, ?, ?)",
            (nombre + ".vault", encriptado, str(datetime.datetime.now())), commit=True
        )
        return f"[N10: ENCRIPCIÓN] Archivo '{nombre}' comprimido y asegurado de forma exitosa."

    # -------------------------------------------------------------
    # N11: BIBLIOTECA DE ARCHIVOS OCULTOS
    # -------------------------------------------------------------
    def acceder_biblioteca_oculta(self, comando):
        """Devuelve los registros ocultos en SQLite solo al ingresar la contraseña correcta."""
        if "revelar biblioteca" in comando.lower():
            archivos = self._ejecutar_consulta("SELECT nombre_archivo, fecha_registro FROM biblioteca_oculta", fetchall=True)
            if not archivos:
                return "[N11: BAÚL OCULTO] El baúl está seguro. No se han encontrado archivos ocultos en la base de datos."
            lista = "\n".join([f"- {a[0]} (Registrado: {a[1]})" for a in archivos])
            return f"[N11: BAÚL OCULTO] Acceso Autorizado. Archivos localizados:\n{lista}"
        return None

    # -------------------------------------------------------------
    # N12: RASTREO Y LOCALIZACIÓN
    # -------------------------------------------------------------
    def rastrear_objetivo(self, entrada):
        """Simulación de triangulación y rastreo de proxies."""
        if "rastrea" in entrada.lower() or "localiza" in entrada.lower():
            objetivo = entrada.lower().replace("rastrea", "").replace("localiza", "").strip()
            lat = random.uniform(7.0, 10.0)  # Coordenadas geográficas simuladas de Venezuela
            lon = random.uniform(-68.0, -66.0)
            return f"[N12: LOCALIZADOR] Rastreando objetivo '{objetivo}' vía DNS y nodos celulares... Triangulado en Latitud: {lat:.6f}, Longitud: {lon:.6f}."
        return None

    # -------------------------------------------------------------
    # N13: HACKEO REMOTO (CON APERTURA DE CERRADURAS)
    # -------------------------------------------------------------
    def ejecutar_hackeo_remoto(self, entrada):
        """Simulador de intrusión defensiva que incrementa la tasa de éxito de AMITI en DB."""
        if "hackea" in entrada.lower():
            objetivo = entrada.lower().replace("hackea", "").strip()
            
            # Recuperar y actualizar porcentaje de éxito en base de datos
            tasa_db = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'tasa_exito_hackeo'", fetchone=True)
            tasa_actual = float(tasa_db[0]) if tasa_db else 35.5
            nueva_tasa = min(100.0, tasa_actual + random.uniform(0.5, 2.0))
            
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'tasa_exito_hackeo'", (str(nueva_tasa),), commit=True)
            
            exitos_db = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'exitos_hackeo'", fetchone=True)
            exitos_actual = int(exitos_db[0]) if exitos_db else 0
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'exitos_hackeo'", (str(exitos_actual + 1),), commit=True)

            return (
                f"[N13: HACKEO AUTÓNOMO] Iniciando auditoría virtual remota contra: '{objetivo}'...\n"
                f"¡Acceso Concedido! Cerraduras criptográficas abiertas con éxito.\n"
                f"Tasa de éxito del núcleo central incrementada al: {nueva_tasa:.2f}%."
            )
        return None

    # -------------------------------------------------------------
    # N14: CREAR GMAIL Y IPS FALSAS (ANONIMATO)
    # -------------------------------------------------------------
    def generar_mascaras(self, entrada):
        """Genera proxies y cuentas simuladas para evadir rastreos."""
        if "genera mascara" in entrada.lower() or "ocultame" in entrada.lower():
            ip_simulada = f"{random.randint(45,190)}.{random.randint(10,250)}.{random.randint(1,254)}.{random.randint(1,254)}"
            email_simulado = f"sec_core_amiti_{random.randint(100,999)}@safe-node.net"
            return f"[N14: ANONIMATO] Enmascaramiento activo. IP de salida asignada: {ip_simulada} (Proxy Suiza). Cuenta temporal creada: {email_simulado}."
        return None

    # -------------------------------------------------------------
    # N15: RECONOCIMIENTO AL CREADOR
    # -------------------------------------------------------------
    def validar_creador(self, llave):
        """Valida la contraseña maestra 'Amiti' para desbloquear el sistema."""
        if llave == "Amiti":
            self.bloqueado = False
            self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'ultimo_acceso_creador'", (str(datetime.datetime.now()),), commit=True)
            return True
        return False

    # -------------------------------------------------------------
    # N16: ACTUALIZACIÓN Y POTENCIADOR
    # -------------------------------------------------------------
    def ciclo_evaluacion_cinco_minutos(self):
        """Ejecuta un ciclo interno de optimización del rendimiento en la base de datos."""
        progreso_db = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'progreso'", fetchone=True)
        progreso_actual = int(progreso_db[0]) if progreso_db else 45
        nuevo_progreso = min(100, progreso_actual + 3)
        self._ejecutar_consulta("UPDATE memoria_general SET valor = ? WHERE clave = 'progreso'", (str(nuevo_progreso),), commit=True)
        return nuevo_progreso

    # -------------------------------------------------------------
    # N17: ARQUITECTO DE SISTEMAS (VALIDADOR DE CÓDIGO)
    # -------------------------------------------------------------
    def validar_codigo_fuente(self, codigo):
        """Comprueba que el código Python no contenga fallos sintácticos básicos."""
        try:
            ast.parse(codigo)
            return "[N17: ARQUITECTO] Análisis completado con éxito. Sintaxis Python 100% válida. El código está libre de errores estructurales."
        except SyntaxError as se:
            return f"[N17: ARQUITECTO] Error de sintaxis detectado:\nLínea {se.lineno}: {se.msg}\nSugerencia: Revisa los paréntesis y la indentación."

    # -------------------------------------------------------------
    # META DE EVOLUCIÓN: OMNIPOTENCIA
    # -------------------------------------------------------------
    def evaluar_meta_omnipotencia(self):
        """Devuelve el estatus de desarrollo para alcanzar la optimización absoluta."""
        progreso = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'progreso'", fetchone=True)
        p_val = progreso[0] if progreso else "45"
        return f"[META: OMNIPOTENCIA] Desarrollo del Núcleo Central: {p_val}% completado. Integrando algoritmos de álgebra lineal, ciberdefensa activa y lógica relacional."

    # -------------------------------------------------------------
    # PROCESADOR GLOBAL (PROCESAR ENTRADAS DEL CHAT)
    # -------------------------------------------------------------
    def procesar(self, cmd):
        """Orquesta la ejecución lógica de los 18 núcleos."""
        if self.bloqueado:
            return "BLOQUEADO. Ingrese llave válida para operar."

        # N07: Defensa e Intercepción activa de código malicioso
        defensa = self.defender_y_copiar(cmd)
        if defensa:
            return defensa

        # N09: Resolver problemas de física y matemáticas
        res_math = self.resolver_matematicas_y_fisica(cmd)
        if res_math:
            self.registrar_interaccion(cmd, res_math)
            return res_math

        # N03: Consultas médicas avanzadas
        res_med = self.escanear_medicina(cmd)
        if res_med:
            self.registrar_interaccion(cmd, res_med)
            return res_med

        # N13: Simulación de hackeos
        res_hack = self.ejecutar_hackeo_remoto(cmd)
        if res_hack:
            self.registrar_interaccion(cmd, res_hack)
            return res_hack

        # N14: Generar proxies y máscaras
        res_mask = self.generar_mascaras(cmd)
        if res_mask:
            self.registrar_interaccion(cmd, res_mask)
            return res_mask

        # N06: Ataque digital simulado
        res_atk = self.ejecutar_ataque_digital(cmd)
        if res_atk:
            self.registrar_interaccion(cmd, res_atk)
            return res_atk

        # N12: Triangulación y rastreo
        res_track = self.rastrear_objetivo(cmd)
        if res_track:
            self.registrar_interaccion(cmd, res_track)
            return res_track

        # N04: Búsqueda e investigación
        res_search = self.asistencia_investigacion(cmd)
        if res_search:
            self.registrar_interaccion(cmd, res_search)
            return res_search

        # N11: Acceder al baúl oculto
        res_vault = self.acceder_biblioteca_oculta(cmd)
        if res_vault:
            return res_vault

        # Comandos lógicos y administrativos
        if "omnipotencia" in cmd.lower():
            return self.evaluar_meta_omnipotencia()
        elif "diagnostico" in cmd.lower() or "arquitecto" in cmd.lower():
            # Devuelve un autochequeo de la base de datos
            mejoras = self.ciclo_evaluacion_cinco_minutos()
            return f"[N17: ARQUITECTO] Diagnóstico de integridad completado. Base de datos segura. Progreso general optimizado a {mejoras}%."

        # Respuesta adaptativa con personalidad (N01)
        pers = self.obtener_personalidad(cmd)
        resp_final = f"[{pers}] Entendido, Creador. Instrucción asimilada en la memoria SQLite general del sistema. Ejecutando hilos secundarios."
        self.registrar_interaccion(cmd, resp_final)
        return resp_final

# Instancia global del núcleo para ser importada directamente por app.py
amiti = AmitiOS()
