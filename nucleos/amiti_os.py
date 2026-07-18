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
        self._inicializar_db()
        
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
            valores_iniciales = [
                ("modo_personalidad", "Empático"), ("progreso", "45"),
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
        return modo[0] if modo else "Omnipotente"

    def proteger_creador(self, entrada):
        if any(p in entrada.lower() for p in ["peligro", "amenaza", "ataque", "extorsion", "emergencia"]):
            return "[N02: SEGURIDAD] ¡Peligro detectado! Desplegando escudo de red móvil y falsificando geolocalización."
        return None

    def escanear_medicina(self, entrada):
        entrada_norm = entrada.lower()
        if "anemia" in entrada_norm and "drepanocitica" in entrada_norm or "fisiopatologia" in entrada_norm:
            return "[N03: MEDICINA] Anemia Drepanocítica: Mutación en gen beta-globina (ácido glutámico por valina en pos 6). En hipoxia, la HbS se polimeriza generando drepanocitos, oclusión microvascular y hemólisis."
        elif "cirugia" in entrada_norm or "schwartz" in entrada_norm:
            return "[N03: CIRUGÍA] Principios (Schwartz): Hemostasia estricta, conservación de suministro sanguíneo, asepsia y manejo delicado de tejidos."
        elif "signos vitales" in entrada_norm:
            return "[N03: TELEMETRÍA] Signos simulados: Temperatura: 36.5°C, Frecuencia Cardíaca: 72 lpm, SpO2: 98%."
        return None

    def asistencia_investigacion(self, consulta):
        if "investiga" in consulta.lower() or "busca" in consulta.lower():
            tema = consulta.lower().replace("investiga", "").replace("busca", "").strip()
            self.incrementar_progreso(2)
            return f"[N04: INVESTIGACIÓN] Escaneando redes globales sobre '{tema}' e indexando información en Neon DB."
        return None

    def autogenerar_mejoras(self, entrada):
        if "crea codigo" in entrada.lower() or "genera funcion" in entrada.lower():
            return "[N05: AUTO-DESARROLLADOR] Estructura:\n\ndef nueva_funcion_amiti(*args):\n    return sum(args)"
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
        entrada_norm = entrada.lower()
        if "aprende" in entrada_norm or "memoriza" in entrada_norm:
            dato = entrada.replace("aprende", "").replace("memoriza", "").strip()
            if not dato: return "[N08: APRENDIZAJE] Especifica el dato a indexar."
            self._ejecutar_consulta("INSERT INTO aprendizaje (dato, fecha_registro) VALUES (%s, %s)", (dato, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), commit=True)
            self.incrementar_progreso(1)
            return f"[N08: APRENDIZAJE] Conocimiento indexado con éxito: '{dato}'."
        if "recuerda datos" in entrada_norm or "ver aprendizaje" in entrada_norm:
            registros = self._ejecutar_consulta("SELECT dato, fecha_registro FROM aprendizaje ORDER BY id DESC LIMIT 5", fetchall=True)
            if not registros: return "[N08: APRENDIZAJE] Clústeres vacíos."
            return "[N08: MEMORIA]\n" + "\n".join([f"• [{r[1]}] {r[0]}" for r in registros])
        return None

    def resolver_matematicas_y_fisica(self, entrada):
        limpia = entrada.lower().strip()
        if "raiz" in limpia or "raíz" in limpia:
            nums = re.findall(r'\d+', limpia)
            if nums: return f"[N09: MATEMÁTICAS] Raíz cuadrada de {nums[0]} = {math.sqrt(float(nums[0]))}"
        if "fuerza" in limpia:
            m = re.search(r'm\s*=\s*(\d+(\.\d+)?)', limpia)
            a = re.search(r'a\s*=\s*(\d+(\.\d+)?)', limpia)
            if m and a: return f"[N09: FÍSICA] F = m * a -> {float(m.group(1))} kg * {float(a.group(1))} m/s² = {float(m.group(1)) * float(a.group(1))} N"
        caracteres = set("0123456789+-*/(). ")
        if all(c in caracteres for c in limpia) and any(op in limpia for op in "+-*/") and len(limpia) > 2:
            try: return f"[N09: MATEMÁTICAS] Resultado: {limpia} = {eval(limpia, {'__builtins__': None}, {})}"
            except: pass
        return None

    def encriptar_y_comprimir(self, entrada):
        if "encripta" in entrada.lower():
            partes = entrada.split(":")
            if len(partes) < 3: return "[N10: ENCRIPCIÓN] Usa: 'encripta:nombre_archivo:contenido'"
            nombre, contenido = partes[1].strip(), partes[2].strip()
            enc = base64.b64encode(contenido.encode('utf-8')).decode('utf-8')
            self._ejecutar_consulta("""
                INSERT INTO biblioteca_oculta (nombre_archivo, contenido_encriptado, fecha_registro) 
                VALUES (%s, %s, %s) ON CONFLICT (nombre_archivo) 
                DO UPDATE SET contenido_encriptado = EXCLUDED.contenido_encriptado
            """, (nombre + ".vault", enc, str(datetime.datetime.now())), commit=True)
            return f"[N10: ENCRIPCIÓN] Archivo '{nombre}.vault' resguardado en Neon DB."
        return None

    def acceder_biblioteca_oculta(self, comando):
        if "biblioteca oculta" in comando.lower() or "abrir biblioteca" in comando.lower():
            archivos = self._ejecutar_consulta("SELECT nombre_archivo, fecha_registro FROM biblioteca_oculta", fetchall=True)
            if not archivos: return "[N11: BAÚL OCULTO] No hay archivos encriptados todavía."
            return "[N11: BAÚL OCULTO] Baúl en la nube:\n" + "\n".join([f"- {a[0]} ({a[1]})" for a in archivos])
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
            return "[N16: MANTENIMIENTO] Índices de Neon DB recalculados y optimizados."
        return None

    def modulo_linguistico_ingles(self, entrada):
        entrada_norm = entrada.lower()
        if "traduce" in entrada_norm:
            return f"[N17: LINGÜÍSTICA] Semántica analizada para: '{entrada.replace('traduce','').strip()}'."
        elif "conjugacion" in entrada_norm or "verbo" in entrada_norm:
            return "[N17: LINGÜÍSTICA] Esquema de verbos irregulares:\n• Go -> Went -> Gone\n• Write -> Wrote -> Written\n• Build -> Built -> Built"
        return None

    def controlar_dispositivo_simulado(self, entrada):
        if "dispositivo" in entrada.lower() or "controla" in entrada.lower():
            return "[N18: HARDWARE] Mapeando periféricos. Interfaz optimizada de manera síncrona."
        return None

    def generar_algoritmo_contable(self, entrada):
        if any(p in entrada.lower() for p in ["crea algoritmo", "sistema contable", "contabilidad monetaria"]):
            self.incrementar_progreso(2)
            return (
                "[N19: ALGORITMOS CONTABLES] Estructura transaccional monetaria:\n\n"
                "```python\n"
                "class MotorContableMonetario:\n"
                "    def __init__(self):\n"
                "        self.saldo = 0.0\n"
                "    def transaccion(self, tipo, monto):\n"
                "        if tipo.lower() == 'ingreso': self.saldo += float(monto)\n"
                "        return self.saldo\n"
                "```"
            )
        return None

    def obtener_telemetria_hardware(self, entrada):
        if "estado del hardware" in entrada.lower() or "telemetria" in entrada.lower():
            return f"[N20: TELEMETRÍA] Core Uptime: {time.time() - self.inicio_sistema:.2f}s | Distribución de memoria: Estable."
        return None

    def obtener_progreso(self):
        res = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'progreso'", fetchone=True)
        return int(res[0]) if res else 45

    def incrementar_progreso(self, cantidad):
        prog = self.obtener_progreso()
        nuevo = min(100, prog + cantidad)
        self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'progreso'", (str(nuevo),), commit=True)
        return nuevo

    def procesar(self, cmd):
        if self.bloqueado: return "BLOQUEADO. Ingrese la llave de seguridad."
        
        # Orquestación automática de sub-núcleos estructurados
        modulos = [
            self.defender_y_copiar, self.proteger_creador, self.resolver_matematicas_y_fisica,
            self.generar_algoritmo_contable, self.ejecutar_auto_mantenimiento_db, self.obtener_telemetria_hardware,
            self.registrar_aprendizaje, self.encriptar_y_comprimir, self.acceder_biblioteca_oculta,
            self.escanear_medicina, self.asistencia_investigacion, self.autogenerar_mejoras,
            self.ejecutar_hackeo_remoto, self.rastrear_objetivo, self.generar_mascaras,
            self.controlar_dispositivo_simulado, self.modulo_linguistico_ingles
        ]
        
        for modulo in modulos:
            resultado = modulo(cmd)
            if resultado: return resultado

        p = self.obtener_personalidad(cmd)
        if "se " in cmd.lower() or "modo " in cmd.lower(): return p
        return f"[Amiti OS - {p}]: Escucha activa establecida, Creador. Clúster Neon DB listo para comandos macro."
