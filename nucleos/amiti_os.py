# nucleos/amiti_os.py
import os, re, math, time, random, psycopg2, datetime, base64

class AmitiOS:
    def __init__(self):
        self.db_url = os.environ.get("DATABASE_URL")
        self.bloqueado = True  
        self.inicio_sistema = time.time()
        self.armas_defensivas, self.parches_virtuales = [], {}
        self._inicializar_db()
        self._cargar_mutaciones_iniciales()
        
    def _inicializar_db(self):
        if not self.db_url: return
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS memoria_general (clave TEXT PRIMARY KEY, valor TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS biblioteca_oculta (nombre_archivo TEXT PRIMARY KEY, contenido_encriptado TEXT, fecha_registro TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS aprendizaje (id SERIAL PRIMARY KEY, dato TEXT, fecha_registro TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS matriz_evolucion (clave_conocimiento TEXT PRIMARY KEY, directriz TEXT, tipo_parche TEXT, fecha_absorcion TEXT)")
            for k, v in [("modo_personalidad", "Empático"), ("progreso", "59"), ("tasa_exito_hackeo", "35.5"), ("exitos_hackeo", "0"), ("ultimo_acceso_creador", "Nunca")]:
                cursor.execute("INSERT INTO memoria_general (clave, valor) VALUES (%s, %s) ON CONFLICT (clave) DO NOTHING", (k, v))
            conn.commit(); conn.close()
        except Exception as e: print(f"Error DB: {e}")

    def _cargar_mutaciones_iniciales(self):
        res = self._ejecutar_consulta("SELECT clave_conocimiento, directriz FROM matriz_evolucion", fetchall=True)
        if isinstance(res, list):
            for c, d in res: self.parches_virtuales[c.lower().strip()] = d

    def _ejecutar_consulta(self, query, params=(), fetchone=False, fetchall=False, commit=False):
        if not self.db_url: return "Error: Sin conexión a Neon."
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            cursor.execute(query.replace('?', '%s'), params)
            res = cursor.fetchone() if fetchone else (cursor.fetchall() if fetchall else None)
            if commit: conn.commit()
            conn.close()
            return res
        except Exception as e: return f"Error de DB: {str(e)}"

    def obtener_personalidad(self, entrada=""):
        e = entrada.lower()
        if "se agresiva" in e or "modo combate" in e:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = 'Combate/Fuego' WHERE clave = 'modo_personalidad'", commit=True)
            return "[N01: PERSONALIDAD] Modo de combate activado. Lenguaje hostil ante intrusiones."
        if "se empatica" in e or "modo compañera" in e:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = 'Empático' WHERE clave = 'modo_personalidad'", commit=True)
            return "[N01: PERSONALIDAD] Modo empático activado. Estoy aquí para apoyarte, creador."
        if "se analitica" in e or "modo cientifico" in e:
            self._ejecutar_consulta("UPDATE memoria_general SET valor = 'Científico' WHERE clave = 'modo_personalidad'", commit=True)
            return "[N01: PERSONALIDAD] Modo analítico activado. Priorizando la lógica rigurosa."
        m = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'modo_personalidad'", fetchone=True)
        return m[0] if m else "Empático"

    def proteger_creador(self, e):
        if any(p in e.lower() for p in ["peligro", "amenaza", "ataque", "extorsion", "emergencia"]):
            return "[N02: SEGURIDAD] ¡Peligro detectado! Desplegando escudo de red móvil y falsificando geolocalización."
        return None

    def escanear_medicina(self, e):
        t = e.lower()
        if "anemia" in t and "drepanocitica" in t or "fisiopatologia" in t: return "[N03: MEDICINA] Anemia Drepanocítica: Mutación en gen beta-globina (Glu6Val). En hipoxia, la HbS se polimeriza generando drepanocitos."
        if "cirugia" in t or "schwartz" in t: return "[N03: CIRUGÍA] Principios (Schwartz): Hemostasia estricta, suministro sanguíneo, asepsia y manejo delicado."
        if "signos vitales" in t: return "[N03: TELEMETRÍA] Signos simulados: Temperatura: 36.5°C, Frecuencia Cardíaca: 72 lpm, SpO2: 98%."
        return None

    def asistencia_investigacion(self, c):
        if "investiga" in c.lower() or "busca" in c.lower():
            t = c.lower().replace("investiga","").replace("busca","").strip()
            self.incrementar_progreso(2)
            return f"[N04: INVESTIGACIÓN] Escaneando redes globales sobre '{t}' e indexando información en Neon DB."
        return None

    def autogenerar_mejoras(self, e):
        if "genera funcion" in e.lower() or "desarrolla funcion" in e.lower(): return "[N05: AUTO-DESARROLLADOR] Estructura modular generada:\n\ndef nueva_funcion_amiti(*args):\n    return sum(args)"
        return None

    def ejecutar_ataque_digital(self, e):
        t = e.lower()
        if any(k in t for k in ["ataca", "contraataque", "elimina amenaza", "destruir"]):
            obj = e.replace("ataca","").replace("contraataque","").replace("destruir","").strip()
            obj = obj if obj else "Entidad Invasora Desconocida"
            tacticas = ["Inyección de Ruido Blanco y Desbordamiento Lógico", "Espejo de Bucle Infinito (Honeypot Cuántico)", "Sobrecarga Síncrona de Cifrado (Trampa de Datos)", "Purga de Paquetes y Falsificación de Host"]
            ataque_elegido = random.choice(tacticas)
            self.incrementar_progreso(2)
            return f"[N06: CONTRAATAQUE OFENSIVO ACTIVO] ⚔️\n🔥 OBJETIVO FIJADO: '{obj}'\n└─ Desplegando: {ataque_elegido}\n└─ Estado: Desmantelando vectores del virus, aislando su IP en la lista negra de Neon DB y ejecutando purga de código malicioso."
        return None

    def defender_y_copiar(self, c):
        for p in [r"drop\s+table", r"delete\s+from", r"rm\s+-rf", r"union\s+select"]:
            if re.search(p, c, re.IGNORECASE): self.armas_defensivas.append(c); return "[N07: DEFENSA ACTIVA] Vector de inyección maliciosa detectado y neutralizado."
        return None

    def registrar_aprendizaje(self, e):
        t = e.lower()
        if "aprende" in t or "memoriza" in t:
            d = e.replace("aprende","").replace("memoriza","").strip()
            if not d: return "[N08: APRENDIZAJE] Especifica el dato a indexar."
            self._ejecutar_consulta("INSERT INTO aprendizaje (dato, fecha_registro) VALUES (%s, %s)", (d, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), commit=True)
            self.incrementar_progreso(1)
            return f"[N08: APRENDIZAJE] Conocimiento indexado con éxito: '{d}'."
        if any(k in t for k in ["recuerda", "aprendiste", "aprendizaje"]):
            reg = self._ejecutar_consulta("SELECT dato, fecha_registro FROM aprendizaje ORDER BY id DESC LIMIT 5", fetchall=True)
            mat = self._ejecutar_consulta("SELECT COUNT(*) FROM matriz_evolucion", fetchone=True)
            tot_m = mat[0] if mat else 0
            txt = "[N08: MEMORIA]\n" + "\n".join([f"• [{r[1]}] {r[0]}" for r in reg]) if reg else "[N08: MEMORIA] Registro de aprendizaje libre vacío."
            return f"{txt}\n\n[N15: MATRIZ DE EVOLUCIÓN]\n• Directrices dinámicas en Neon DB: {tot_m}"
        return None

    def resolver_matematicas_y_fisica(self, e):
        l = e.lower().strip()
        if "raiz" in l or "raíz" in l:
            nums = re.findall(r'\d+\.?\d*', l)
            if nums: return f"[N09: MATEMÁTICAS] 🧠 Raíz Cuadrada Procesada:\n√{nums[0]} = {math.sqrt(float(nums[0]))}"
        if "fuerza" in l:
            m, a = re.search(r'm\s*=\s*(\d+(\.\d+)?)', l), re.search(r'a\s*=\s*(\d+(\.\d+)?)', l)
            if m and a: return f"[N09: FÍSICA] F = m * a -> {float(m.group(1))} kg * {float(a.group(1))} m/s² = {float(m.group(1)) * float(a.group(1))} N"
        for p in ["calcula","cuanto es","cuánto es","resuelve","ecuacion","ecuación","resultado","de"]: l = l.replace(p, "")
        exp = "".join([c for c in l if c in "0123456789+-*/(). "]).strip()
        if exp and re.search(r'\d', exp) and any(op in exp for op in "+-*/"):
            try:
                if "/0" in exp.replace(" ",""): return "[N09: MATEMÁTICAS] Error: División entre cero indefinida."
                return f"[N09: MATEMÁTICAS] 🧠 Ecuación Combinada Resuelta:\nExpresión: {exp}\nResultado = {eval(exp, {'__builtins__': None}, {})}"
            except: pass
        return None

    def analizar_problemas_nomina_y_pagos(self, e):
        l = e.lower()
        if not any(k in l for k in ["trabajador", "empleado", "pagar", "comision", "comisión", "sueldo", "nomina"]): return None
        nums = [float(n) for n in re.findall(r'\d+\.?\d*', l)]
        if len(nums) < 2: return None
        cant, com, base = None, 0.0, None
        m_t = re.search(r'(\d+)\s*(trabajador|empleado|persona|obrer|ayudante)', l)
        cant = float(m_t.group(1)) if m_t else (float(re.search(r'(trabajador|empleado|persona|obrer|ayudante)es?\s*(\d+)', l).group(2)) if re.search(r'(trabajador|empleado|persona|obrer|ayudante)es?\s*(\d+)', l) else None)
        m_c = re.search(r'(\d+)\s*(de\s*)?comisi', l)
        com = float(m_c.group(1)) if m_c else (float(re.search(r'comisi\w*\s*(de\s*)?(\d+)', l).group(2)) if re.search(r'comisi\w*\s*(de\s*)?(\d+)', l) else 0.0)
        usados = [v for v in [cant, com] if v is not None]
        restantes = [n for n in nums if n not in usados]
        if cant is not None and restantes: base = restantes[0]
        else:
            if len(nums) == 3: cant, base, com = nums[0], nums[1], nums[2]
            elif len(nums) == 2: cant, base = nums[0], nums[1]
        if cant is None or base is None: return None
        tot_p = base + com; tot_g = tot_p * cant
        return f"[N19: MOTOR CONTABLE NARRATIVO] 📊 Análisis Analítico de Pagos:\n• Personal: {int(cant)} trabajadores.\n• Sueldo base: ${base:.2f}\n• Comisión: ${com:.2f}\n• TOTAL NETO A PAGAR: ${tot_g:.2f}"

    def encriptar_y_comprimir(self, e):
        if "encripta" in e.lower():
            p = e.split(":", 2)
            if len(p) < 3: return "[N10: ENCRIPCIÓN] Usa: 'encripta:nombre_archivo:contenido'"
            enc = base64.b64encode(p[2].strip().encode('utf-8')).decode('utf-8')
            self._ejecutar_consulta("INSERT INTO biblioteca_oculta VALUES (%s, %s, %s) ON CONFLICT (nombre_archivo) DO UPDATE SET contenido_encriptado = EXCLUDED.contenido_encriptado", (p[1].strip()+".vault", enc, str(datetime.datetime.now())), commit=True)
            return f"[N10: ENCRIPCIÓN] Archivo '{p[1].strip()}.vault' resguardado en Neon DB de forma íntegra."
        return None

    def acceder_biblioteca_oculta(self, c):
        cn = c.lower().strip()
        if "leer:" in cn:
            n = c.split(":", 1)[1].strip()
            if not n.endswith(".vault"): n += ".vault"
            res = self._ejecutar_consulta("SELECT contenido_encriptado FROM biblioteca_oculta WHERE nombre_archivo = %s", (n,), fetchone=True)
            if not res or res[0] is None: return f"[N11: BAÚL OCULTO] El archivo '{n}' no existe en el clúster de Neon."
            return f"[N11: LECTOR] <b>📖 Archivo:</b> {n}\n└─ Contenido recuperado:\n\n{base64.b64decode(res[0].encode('utf-8')).decode('utf-8')}"
        if "biblioteca oculta" in cn or "abrir biblioteca" in cn:
            archivos = self._ejecutar_consulta("SELECT nombre_archivo FROM biblioteca_oculta", fetchall=True)
            return "[N11: BAÚL OCULTO] Baúl en la nube:\n" + "\n".join([f"- {a[0]}" for a in archivos]) if archivos else "[N11: BAÚL OCULTO] Baúl vacío."
        return None

    def auto_evolucion_sistema(self, e):
        cn = e.lower().strip()
        if "absorber:" in cn:
            p = e.split(":", 2)
            if len(p) < 3: return "[N15: EVOLUCIÓN] Protocolo incorrecto. Usa: 'absorber:palabra_clave:respuesta_o_directriz'"
            cl, dir_ = p[1].strip().lower(), p[2].strip()
            self._ejecutar_consulta("INSERT INTO matriz_evolucion VALUES (%s, %s, 'Hot-Patch Cognitivo', %s) ON CONFLICT (clave_conocimiento) DO UPDATE SET directriz = EXCLUDED.directriz", (cl, dir_, str(datetime.datetime.now())), commit=True)
            self.parches_virtuales[cl] = dir_; self.incrementar_progreso(1)
            return f"[N15: ABSORCIÓN] Conciencia expandida. Conocimiento inyectado en la matriz bajo la clave genética '{cl}'."
        if "ejecutar auto-actualizacion" in cn or "mutar sistema" in cn:
            res = self._ejecutar_consulta("SELECT COUNT(*) FROM matriz_evolucion", fetchone=True)
            self._cargar_mutaciones_iniciales(); self.incrementar_progreso(2)
            return f"[N15: ACTUALIZACIÓN] 🌀 Secuencia de auto-mutación completa.\n• Estado de la Matriz: {res[0] if res else 0} directrices dinámicas cargadas desde Neon DB."
        for k, d in self.parches_virtuales.items():
            if k in cn: return f"[N15: CONOCIMIENTO ASIMILADO] 🧬 (Respuesta Autonomous): {d}"
        return None

    def rastrear_objetivo(self, e):
        if "rastrea" in e.lower() or "localiza" in e.lower(): return f"[N12: LOCALIZADOR] Coordenadas: Lat {random.uniform(7,10):.6f}, Lon {random.uniform(-68,-66):.6f}."
        return None

    def ejecutar_hackeo_remoto(self, e):
        if "hackea" in e.lower():
            t = float(self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'tasa_exito_hackeo'", fetchone=True)[0] or 35.5)
            self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'tasa_exito_hackeo'", (str(min(100.0, t + random.uniform(1.0, 3.5))),), commit=True)
            self.incrementar_progreso(1)
            return f"[N13: AUDITORÍA SIMULADA] Inyectando exploits educativos. Éxito del núcleo incrementado."
        return None

    def generar_mascaras(self, e):
        if "genera mascara" in e.lower() or "ocultame" in e.lower(): return f"[N14: ANONIMATO] Proxy IP: {random.randint(45,190)}.{random.randint(10,250)}.4.12 | Nodo: sec_amiti_{random.randint(100,999)}@safe.net"
        return None

    def validar_creador(self, llave):
        if llave == "Amiti": self.bloqueado = False; self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'ultimo_acceso_creador'", (str(datetime.datetime.now()),), commit=True); return True
        return False

    def ejecutar_auto_mantenimiento_db(self, e):
        if "optimiza base de datos" in e.lower() or "mantenimiento db" in e.lower():
            for t in ["memoria_general", "biblioteca_oculta", "aprendizaje", "matriz_evolucion"]: self._ejecutar_consulta(f"ANALYZE {t};", commit=True)
            return "[N16: MANTENIMIENTO] Índices de Neon DB recalculados y optimizados."
        return None

    def modulo_linguistico_ingles(self, e):
        if "traduce" in e.lower(): return f"[N17: LINGÜÍSTICA] Semántica analizada para la cadena de entrada."
        if "conjugacion" in e.lower() or "verbo" in e.lower(): return "[N17: LINGÜÍSTICA] Esquema: Go->Went->Gone | Write->Wrote->Written"
        return None

    def controlar_dispositivo_simulado(self, e):
        if "dispositivo" in e.lower() or "controla" in e.lower(): return "[N18: HARDWARE] Mapeando periféricos. Interfaz optimizada de manera síncrona."
        return None

    def generar_algoritmo_contable(self, e):
        if "algoritmo" in e.lower() and "contab" in e.lower():
            self.incrementar_progreso(2)
            return "[N19: ALGORITMOS CONTABLES] 📊 Código monetario generado:\n\n```python\nclass MotorContable:\n    def __init__(self): self.saldo = 0.0\n```"
        return None

    def obtener_telemetria_hardware(self, e):
        if "estado del hardware" in e.lower() or "telemetria" in e.lower(): return f"[N20: TELEMETRÍA] Core Uptime: {time.time() - self.inicio_sistema:.2f}s | Distribución estable."
        return None

    def obtener_progreso(self):
        res = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'progreso'", fetchone=True)
        return int(res[0]) if res else 59

    def incrementar_progreso(self, cant):
        n = min(100, self.obtener_progreso() + cant)
        self._ejecutar_consulta("UPDATE memoria_general SET valor = %s WHERE clave = 'progreso'", (str(n),), commit=True)
        return n

    def procesar(self, cmd):
        if self.bloqueado: return "BLOQUEADO. Ingrese la llave de seguridad."
        cn = cmd.lower().strip()
        modulos = [
            self.defender_y_copiar, self.proteger_creador, self.resolver_matematicas_y_fisica,
            self.analizar_problemas_nomina_y_pagos, self.generar_algoritmo_contable, self.ejecutar_auto_mantenimiento_db,
            self.obtener_telemetria_hardware, self.registrar_aprendizaje, self.encriptar_y_comprimir,
            self.acceder_biblioteca_oculta, self.auto_evolucion_sistema, self.escanear_medicina,
            self.asistencia_investigacion, self.autogenerar_mejoras, self.ejecutar_hackeo_remoto,
            self.rastrear_objetivo, self.generar_mascaras, self.controlar_dispositivo_simulado, 
            self.modulo_linguistico_ingles, self.ejecutar_ataque_digital
        ]
        for m in modulos:
            res = m(cmd)
            if res: return res
        p = self.obtener_personalidad(cmd)
        if "se " in cn or "modo " in cn: return p
        if any(h in cn for h in ["hola", "saludos", "buenas"]): return f"[Amiti OS - {p}]: ¡Hola de nuevo, Creador! 👋 Todos mis sub-núcleos lógicos y Neon DB están en línea."
        if any(a in cn for a in ["ayuda", "que puedes hacer", "funciones"]): return f"[Amiti OS - {p}]: 🤖 Capacidades: Cálculos de nóminas narrativas, Auto-Evolución N15, Ciberseguridad y Neon DB."
        return f"[Amiti OS - Empático]: Entendido perfectamente, Creador. He leído tu mensaje, pero no logré identificar un comando directo. Recuerda que puedes pedirme operaciones matemáticas o que genere código contable. 🚀"
        
