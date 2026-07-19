# nucleos/amiti_os.py
import os
import re
import math
import time
import random
import psycopg2
import datetime
import base64

class AmitiOS:
    def __init__(self):
        self.db_url = os.environ.get("DATABASE_URL")
        self.bloqueado = True  
        self.inicio_sistema = time.time()
        self.armas_defensivas = []  
        self.parches_virtuales = {} 
        self._inicializar_db()
        self._cargar_mutaciones_iniciales()
        
    def _inicializar_db(self):
        if not self.db_url:
            print("[ALERTA] No se detectó la variable DATABASE_URL externa.")
            return
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memoria_general (
                    clave TEXT PRIMARY KEY, valor TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS biblioteca_oculta (
                    nombre_archivo TEXT PRIMARY KEY, contenido_encriptado TEXT, fecha_registro TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS aprendizaje (
                    id SERIAL PRIMARY KEY, dato TEXT, fecha_registro TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matriz_evolucion (
                    clave_conocimiento TEXT PRIMARY KEY, directriz TEXT, tipo_parche TEXT, fecha_absorcion TEXT
                )
            """)
            valores_iniciales = [
                ("modo_personalidad", "Empático"), ("progreso", "54"),
                ("tasa_exito_hackeo", "35.5"), ("exitos_hackeo", "0"),
                ("ultimo_acceso_creador", "Nunca")
            ]
            for clave, valor in valores_iniciales:
                cursor.execute("""
                    INSERT INTO memoria_general (clave, valor) 
                    VALUES (%s, %s) ON CONFLICT (clave) DO NOTHING
                """, (clave, valor))
            conn.commit()
            conn.close()
            print("[INFO] Conexión estable con el clúster de Neon DB.")
        except Exception as e:
            print(f"Error inicializando base de datos en la nube: {e}")

    def _cargar_mutaciones_iniciales(self):
        res = self._ejecutar_consulta("SELECT clave_conocimiento, directriz FROM matriz_evolucion", fetchall=True)
        if isinstance(res, list):
            for clave, directriz in res:
                self.parches_virtuales[clave.lower().strip()] = directriz

    def _ejecutar_consulta(self, query, params=(), fetchone=False, fetchall=False, commit=False):
        if not self.db_url:
            return "Error de DB: Sin conexión a la red de Neon."
        try:
            query = query.replace('?', '%s')
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            cursor.execute(query, params)
            res = None
            if fetchone: res = cursor.fetchone()
            elif fetchall: res = cursor.fetchall()
            if commit: conn.commit()
            conn.close()
            return res
        except Exception as e:
            return f"Error de DB: {str(e)}"

    def obtener_personalidad(self, entrada=""):
        entrada_norm = entrada.lower()
        if "se agresiva" in entrada_norm or "modo combate" in entrada_norm:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'modo_personalidad'", ("Combate/Fuego",), commit=True)
            return "[N01: PERSONALIDAD] Modo de combate activado. Lenguaje analítico y hostil ante intrusiones."
        elif "se empatica" in entrada_norm or "modo compañera" in entrada_norm:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'modo_personalidad'", ("Empático",), commit=True)
            return "[N01: PERSONALIDAD] Modo empático activado. Estoy aquí para apoyarte, creador."
        elif "se analitica" in entrada_norm or "modo cientifico" in entrada_norm:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'modo_personalidad'", ("Científico",), commit=True)
            return "[N01: PERSONALIDAD] Modo analítico activado. Priorizando la lógica rigurosa."
        modo = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'modo_personalidad'", fetchone=True)
        return modo[0] if modo else "Empático"

    def proteger_creador(self, entrada):
        if any(p in entrada.lower() for p in ["peligro", "amenaza", "ataque", "extorsion", "emergencia"]):
            return "[N02: SEGURIDAD] ¡Peligro detectado! Desplegando escudo de red móvil y falsificando geolocalización."
        return None

    def escanear_medicina(self, entrada):
        text = entrada.lower()
        if "anemia" in text and "drepanocitica" in text or "fisiopatologia" in text:
            return "[N03: MEDICINA] Anemia Drepanocítica: Mutación en gen beta-globina (ácido glutámico por valina en pos 6). En hipoxia, la HbS se polimeriza generando drepanocitos, oclusión microvascular y hemólisis."
        elif "cirugia" in text or "schwartz" in text:
            return "[N03: CIRUGÍA] Principios (Schwartz): Hemostasia estricta, conservación de suministro sanguíneo, asepsia y manejo delicado de tejidos."
        elif "signos vitales" in text:
            return "[N03: TELEMETRÍA] Signos simulados: Temperatura: 36.5°C, Frecuencia Cardíaca: 72 lpm, SpO2: 98%."
        return None

    def asistencia_investigacion(self, consulta):
        if "investiga" in consulta.lower() or "busca" in consulta.lower():
            tema = consulta.lower().replace("investiga", "").replace("busca", "").strip()
            self.incrementar_progreso(2)
            return f"[N04: INVESTIGACIÓN] Escaneando redes globales sobre '{tema}' e indexando información en Neon DB."
        return None

    def autogenerar_mejoras(self, entrada):
        if "genera funcion" in entrada.lower() or "desarrolla funcion" in entrada.lower():
            return "[N05: AUTO-DESARROLLADOR] Estructura modular generada:\n\ndef nueva_funcion_amiti(*args):\n    return sum(args)"
        return None

    def ejecutar_ataque_digital(self, entrada):
        if "ataca" in entrada.lower() or "derribar" in entrada.lower():
            obj = entrada.lower().replace("ataca", "").replace("derribar", "").strip()
            return f"[N06: SISTEMA OFENSIVO (SIM)] Analizando puertos y vulnerabilidades lógicas en '{obj}'."
        return None

    def defender_y_copiar(self, comando):
        for p in [r"drop\s+table", r"delete\s+from", r"rm\s+-rf", r"union\s+select", r"<script>"]:
            if re.search(p, comando, re.IGNORECASE):
                self.armas_defensivas.append(comando)
                return "[N07: DEFENSA ACTIVA] Vector de inyección maliciosa detectado y neutralizado."
        return None

    def registrar_aprendizaje(self, entrada):
        text = entrada.lower()
        if "aprende" in text or "memoriza" in text:
            dato = entrada.replace("aprende", "").replace("memoriza", "").strip()
            if not dato: return "[N08: APRENDIZAJE] Especifica el dato a indexar."
            self._ejecutar_consulta("INSERT INTO aprendizaje (dato, fecha_registro) VALUES (%s, %s)", (dato, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), commit=True)
            self.incrementar_progreso(1)
            return f"[N08: APRENDIZAJE] Conocimiento indexado con éxito: '{dato}'."
        if "recuerda datos" in text or "ver aprendizaje" in text:
            registros = self._ejecutar_consulta("SELECT dato, fecha_registro FROM aprendizaje ORDER BY id DESC LIMIT 5", fetchall=True)
            if not registros: return "[N08: APRENDIZAJE] Clústeres vacíos."
            return "[N08: MEMORIA]\n" + "\n".join([f"• [{r[1]}] {r[0]}" for r in registros])
        return None

    def resolver_matematicas_y_fisica(self, entrada):
        limpia = entrada.lower().strip()
        if "raiz" in limpia or "raíz" in limpia:
            nums = re.findall(r'\d+\.?\d*', limpia)
            if nums:
                n = float(nums[0])
                return f"[N09: MATEMÁTICAS] 🧠 Raíz Cuadrada Procesada:\n√{n} = {math.sqrt(n)}"

        if "fuerza" in limpia:
            m = re.search(r'm\s*=\s*(\d+(\.\d+)?)', limpia)
            a = re.search(r'a\s*=\s*(\d+(\.\d+)?)', limpia)
            if m and a: return f"[N09: FÍSICA] F = m * a -> {float(m.group(1))} kg * {float(a.group(1))} m/s² = {float(m.group(1)) * float(a.group(1))} N"

        filtrado = limpia
        for palabra in ["calcula", "cuanto es", "cuánto es", "resuelve", "ecuacion", "ecuación", "resultado", "de"]:
            filtrado = filtrado.replace(palabra, "")
        expresion = "".join([c for c in filtrado if c in "0123456789+-*/(). "]).strip()
        
        if expresion and re.search(r'\d', expresion) and any(op in expresion for op in "+-*/"):
            try:
                if "/0" in expresion.replace(" ", ""):
                    return "[N09: MATEMÁTICAS] Error: División entre cero indefinida."
                resultado = eval(expresion, {"__builtins__": None}, {})
                return f"[N09: MATEMÁTICAS] 🧠 Ecuación Combinada Resuelta:\nExpresión: {expresion}\nResultado = {resultado}"
            except:
                pass
        return None

    def analizar_problemas_nomina_y_pagos(self, entrada):
        limpia = entrada.lower()
        if not any(k in limpia for k in ["trabajador", "empleado", "pagar", "comision", "comisión", "sueldo", "nomina", "cuenta"]):
            return None
        nums = [float(n) for n in re.findall(r'\d+\.?\d*', limpia)]
        if len(nums) < 2: return None
        cant_trabajadores = None
        comision = 0.0
        pago_base = None
        match_trabajadores = re.search(r'(\d+)\s*(trabajador|empleado|persona|obrer|ayudante)', limpia)
        if match_trabajadores: cant_trabajadores = float(match_trabajadores.group(1))
        else:
            match_trabajadores_rev = re.search(r'(trabajador|empleado|persona|obrer|ayudante)es?\s*(\d+)', limpia)
            if match_trabajadores_rev: cant_trabajadores = float(match_trabajadores_rev.group(2))
        match_comision = re.search(r'(\d+)\s*(de\s*)?comisi', limpia)
        if match_comision: comision = float(match_comision.group(1))
        else:
            match_comision_rev = re.search(r'comisi\w*\s*(de\s*)?(\d+)', limpia)
            if match_comision_rev: comision = float(match_comision_rev.group(2))
        valores_usados = []
        if cant_trabajadores is not None: valores_usados.append(cant_trabajadores)
        if comision != 0.0: valores_usados.append(comision)
        valores_restantes = [n for n in nums if n not in valores_usados]
        if cant_trabajadores is not None and valores_restantes: pago_base = valores_restantes[0]
        else:
            if len(nums) == 3:
                cant_trabajadores, pago_base, comision = nums[0], nums[1], nums[2]
            elif len(nums) == 2:
                cant_trabajadores, pago_base = nums[0], nums[1]
        if cant_trabajadores is None or pago_base is None: return None
        total_por_persona = pago_base + comision
        total_general = total_por_persona * cant_trabajadores
        return (
            f"[N19: MOTOR CONTABLE NARRATIVO] 📊 Análisis Analítico de Pagos:\n"
            f"• Personal detectado: {int(cant_trabajadores)} trabajadores.\n"
            f"• Sueldo base individual: ${pago_base:.2f}\n"
            f"• Comisión por unidad: ${comision:.2f}\n"
            f"└─ Desglose de Operación:\n"
            f"   Monto por trabajador: ${pago_base:.2f} + ${comision:.2f} =${total_por_persona:.2f}\n"
            f"   TOTAL NETO A PAGAR: {int(cant_trabajadores)} × ${total_por_persona:.2f} =${total_general:.2f}"
        )

    def encriptar_y_comprimir(self, entrada):
        if "encripta" in entrada.lower():
            partes = entrada.split(":", 2)
            if len(partes) < 3: return "[N10: ENCRIPCIÓN] Usa: 'encripta:nombre_archivo:contenido'"
            nombre, contenido = partes[1].strip(), partes[2].strip()
            enc = base64.b64encode(contenido.encode('utf-8')).decode('utf-8')
            self._ejecutar_consulta("""
                INSERT INTO biblioteca_oculta (nombre_archivo, contenido_encriptado, fecha_registro) 
                VALUES (%s, %s, %s) ON CONFLICT (nombre_archivo) 
                DO UPDATE SET contenido_encriptado = EXCLUDED.contenido_encriptado
            """, (nombre + ".vault", enc, str(datetime.datetime.now())), commit=True)
            return f"[N10: ENCRIPCIÓN] Archivo '{nombre}.vault' resguardado en Neon DB de forma íntegra."
        return None

    def acceder_biblioteca_oculta(self, comando):
        comando_norm = comando.lower().strip()
        if "leer:" in comando_norm:
            partes = comando.split(":", 1)
            nombre = partes[1].strip()
            if not nombre.endswith(".vault"): nombre += ".vault"
            res = self._ejecutar_consulta("SELECT contenido_encriptado FROM biblioteca_oculta WHERE nombre_archivo = %s", (nombre,), fetchone=True)
            if not res or res[0] is None:
                return f"[N11: BAÚL OCULTO] El libro/documento '{nombre}' no existe en el clúster de Neon."
            try:
                contenido_dec = base64.b64decode(res[0].encode('utf-8')).decode('utf-8')
                return f"[N11: LECTOR] <b>📖 Archivo:</b> {nombre}\n└─ Contenido recuperado:\n\n{contenido_dec}"
            except Exception as e:
                return f"[N11: ERROR] Fallo crítico al procesar el cifrado Base64: {str(e)}"
        if "biblioteca oculta" in comando_norm or "abrir biblioteca" in comando_norm:
            archivos = self._ejecutar_consulta("SELECT nombre_archivo, fecha_registro FROM biblioteca_oculta", fetchall=True)
            if not archivos: return "[N11: BAÚL OCULTO] No hay archivos encriptados todavía."
            return "[N11: BAÚL OCULTO] Baúl en la nube:\n" + "\n".join([f"- {a[0]} ({a[1]})" for a in archivos])
        return None

    def auto_evolucion_sistema(self, entrada):
        cmd_norm = entrada.lower().strip()
        if "absorber:" in cmd_norm:
            partes = entrada.split(":", 2)
            if len(partes) < 3:
                return "[N15: EVOLUCIÓN] Protocolo incorrecto. Usa: 'absorber:palabra_clave:respuesta_o_directriz'"
            clave = partes[1].strip().lower()
            directriz = partes[2].strip()
            self._ejecutar_consulta("""
                INSERT INTO matriz_evolucion (clave_conocimiento, directriz, tipo_parche, fecha_absorcion)
                VALUES (%s, %s, %s, %s) ON CONFLICT (clave_conocimiento)
                DO UPDATE SET directriz = EXCLUDED.directriz
            """, (clave, directriz, "Hot-Patch Cognitivo", str(datetime.datetime.now())), commit=True)
            self.parches_virtuales[clave] = directriz
            self.incrementar_progreso(1)
            return f"[N15: ABSORCIÓN] Conciencia expandida. Conocimiento inyectado en la matriz bajo la clave genética '{clave}'."

        if "ejecutar auto-actualizacion" in cmd_norm or "mutar sistema" in cmd_norm:
            res = self._ejecutar_consulta("SELECT COUNT(*) FROM matriz_evolucion", fetchone=True)
            total = res[0] if res else 0
            self._cargar_mutaciones_iniciales()
            self.incrementar_progreso(2)
            return f"[N15: ACTUALIZACIÓN] 🌀 Secuencia de auto-mutación completa.\n• Estado de la Matriz: {total} directrices dinámicas cargadas desde Neon DB."

        for clave_guardada, respuesta_directriz in self.parches_virtuales.items():
            if clave_guardada in cmd_norm:
                return f"[N15: CONOCIMIENTO ASIMILADO] 🧬 (Respuesta Autónoma): {respuesta_directriz}"
        return None

    def rastrear_objetivo(self, entrada):
        if "rastrea" in entrada.lower() or "localiza" in entrada.lower():
            obj = entrada.lower().replace("rastrea", "").replace("localiza", "").strip()
            return f"[N12: LOCALIZADOR] Coordenadas de '{obj}': Lat {random.uniform(7,10):.6f}, Lon {random.uniform(-68,-66):.6f}."
        return None

    def ejecutar_hackeo_remoto(self, entrada):
        if "hackea" in entrada.lower():
            obj = entrada.lower().replace("hackea", "").strip()
            tasa = float(self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'tasa_exito_hackeo'", fetchone=True)[0] or 35.5)
            nueva = min(100.0, tasa + random.uniform(1.0, 3.5))
            self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'tasa_exito_hackeo'", (str(nueva),), commit=True)
            self.incrementar_progreso(1)
            return f"[N13: AUDITORÍA SIMULADA] Objetivo: '{obj}'\n└─ Inyectando exploits educativos. Éxito del núcleo: {nueva:.2f}%."
        return None

    def generar_mascaras(self, entrada):
        if "genera mascara" in entrada.lower() or "ocultame" in entrada.lower():
            return f"[N14: ANONIMATO] Proxy IP: {random.randint(45,190)}.{random.randint(10,250)}.4.12 | Nodo: sec_amiti_{random.randint(100,999)}@safe.net"
        return None

    def validar_creador(self, llave):
        if llave == "Amiti":
            self.bloqueado = False
            self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'ultimo_acceso_creador'", (str(datetime.datetime.now()),), commit=True)
            return True
        return False

    def ejecutar_auto_mantenimiento_db(self, entrada):
        if "optimiza base de datos" in entrada.lower() or "mantenimiento db" in entrada.lower():
            self._ejecutar_consulta("ANALYZE memoria_general;", commit=True)
            self._ejecutar_consulta("ANALYZE biblioteca_oculta;", commit=True)
            self._ejecutar_consulta("ANALYZE aprendizaje;", commit=True)
            self._ejecutar_consulta("ANALYZE matriz_evolucion;", commit=True)
            return "[N16: MANTENIMIENTO] Índices de Neon DB recalculados y optimizados."
        return None

    def modulo_linguistico_ingles(self, entrada):
        text = entrada.lower()
        if "traduce" in text:
            return f"[N17: LINGÜÍSTICA] Semántica analizada para: '{entrada.replace('traduce','').strip()}'."
        elif "conjugacion" in text or "verbo" in text:
            return "[N17: LINGÜÍSTICA] Esquema de verbos irregulares:\n• Go -> Went -> Gone\n• Write -> Wrote -> Written\n• Build -> Built -> Built"
        return None

    def controlar_dispositivo_simulado(self, entrada):
        if "dispositivo" in entrada.lower() or "controla" in entrada.lower():
            return "[N18: HARDWARE] Mapeando periféricos. Interfaz optimizada de manera síncrona."
        return None

    def generar_algoritmo_contable(self, entrada):
        text = entrada.lower()
        if "algoritmo" in text and ("contab" in text or "crea" in text) or "sistema contable" in text:
            self.incrementar_progreso(2)
            return "[N19: ALGORITMOS CONTABLES] 📊 Estructura transaccional monetaria generada:\n\n```python\nclass MotorContableMonetario:\n    def __init__(self):\n        self.saldo = 0.0\n    def transaccion(self, tipo, monto):\n        if tipo.lower() == 'ingreso': self.saldo += float(monto)\n        return self.saldo\n```"
        return None

    def obtener_telemetria_hardware(self, entrada):
        if "estado del hardware" in entrada.lower() or "telemetria" in entrada.lower():
            return f"[N20: TELEMETRÍA] Core Uptime: {time.time() - self.inicio_sistema:.2f}s | Distribución de memoria: Estable."
        return None

    def obtener_progreso(self):
        res = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'progreso'", fetchone=True)
        return int(res[0]) if res else 54

    def incrementar_progreso(self, cantidad):
        prog = self.obtener_progreso()
        nuevo = min(100, prog + cantidad)
        self._ejecutar_consulta("UPDAT
