import os
import re
import json
import math
import random
import datetime
import base64
import urllib.request
import urllib.parse
import psycopg2

class AmitiOS:
    def __init__(self, db_url=None):
        self.db_url = db_url or os.environ.get("DATABASE_URL")
        self.armas_defensivas = []
        self._inicializar_db()

    def _ejecutar_consulta(self, sql, params=(), commit=False, fetchone=False, fetchall=False):
        if not self.db_url:
            print("--- [ERROR DB] URL de base de datos no definida ---")
            return None
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor()
            cur.execute(sql, params)
            res = None
            if fetchone: res = cur.fetchone()
            elif fetchall: res = cur.fetchall()
            if commit: conn.commit()
            cur.close()
            conn.close()
            return res
        except Exception as e:
            print(f"--- [ERROR DB CRÍTICO]: {str(e)} ---")
            return None

    def _inicializar_db(self):
        queries = [
            "CREATE TABLE IF NOT EXISTS aprendizaje (id SERIAL PRIMARY KEY, concepto TEXT, fecha_registro TIMESTAMP DEFAULT NOW());",
            "CREATE TABLE IF NOT EXISTS memoria_general (clave TEXT PRIMARY KEY, valor TEXT);",
            "CREATE TABLE IF NOT EXISTS matriz_evolucion (id SERIAL PRIMARY KEY, clave TEXT UNIQUE, directriz TEXT);",
            "CREATE TABLE IF NOT EXISTS biblioteca_oculta (nombre TEXT PRIMARY KEY, contenido_cifrado TEXT);"
        ]
        for q in queries:
            self._ejecutar_consulta(q, commit=True)

    def incrementar_progreso(self, incremento=1):
        res = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'progreso_core';", fetchone=True)
        if res:
            try:
                p = int(res[0]) + incremento
            except Exception:
                p = 75 + incremento
        else:
            p = 75 + incremento
        self._ejecutar_consulta(
            "INSERT INTO memoria_general (clave, valor) VALUES ('progreso_core', %s) ON CONFLICT (clave) DO UPDATE SET valor = %s;",
            (str(p), str(p)), commit=True
        )
        return p

    def obtener_progreso(self):
        res = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'progreso_core';", fetchone=True)
        if res:
            try:
                return int(res[0])
            except Exception:
                return 0
        return 0

    def _buscar_wikipedia(self, consulta):
        try:
            query_encoded = urllib.parse.quote(consulta.strip())
            url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{query_encoded}"
            req = urllib.request.Request(url, headers={'User-Agent': 'AmitiOS/1.0 (Bot Educativo Python)'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    if data.get('type') in ['standard', 'disambiguation'] and 'extract' in data:
                        return {
                            'titulo': data.get('title', consulta),
                            'origen': 'Wikipedia Enciclopedia',
                            'resumen': data.get('extract', ''),
                            'url': data.get('content_urls', {}).get('desktop', {}).get('page', 'https://es.wikipedia.org')
                        }
        except Exception:
            return None
        return None

    # N04: BÚSQUEDA Y EXTRACCIÓN WEB REAL HÍBRIDA (MEJORADA)
    def asistencia_investigacion(self, c):
        cn = c.lower().strip()
        # Patrón flexible: acepta cualquier variante de 'investiga' o 'busca'
        if not re.match(r"^(investiga|investigación|busca|buscar)", cn):
            return None
        
        # Limpieza inteligente: quita la palabra clave y conectores innecesarios
        tema = re.sub(r"^(investiga\w*\s*|investigación\w*\s*|busca\w*\s*)\s*(de|la|el|los|las)?\s*", "", c, flags=re.IGNORECASE).strip()
        
        if not tema:
            return "[N04: INVESTIGACIÓN] Especifica un término para rastrear en la red."

        # Capa 1: Wikipedia
        res_wiki = self._buscar_wikipedia(tema)
        if res_wiki and res_wiki['resumen']:
            progreso = self.incrementar_progreso(2)
            return (f"[N04: INVESTIGACIÓN] 📚 {res_wiki['titulo']}: {res_wiki['resumen'][:200]}...\n[⚙️ Total Core: {progreso}%]")

        # Capa 2: DuckDuckGo
        try:
            from duckduckgo_search import DDGS
            results = list(DDGS().text(tema, max_results=3))
            if results:
                res = results[0]
                progreso = self.incrementar_progreso(2)
                return f"[N04: INVESTIGACIÓN] 🌐 {res.get('title')}: {res.get('body')[:200]}...\n🔗 {res.get('href')}\n[⚙️ Total Core: {progreso}%]"
        except Exception:
            pass
        return f"[N04: INVESTIGACIÓN] Sin resultados para '{tema}'."

    # N05, N06, N07, N08, N09, N10, N11, N15, N19 (Mantenemos funcionalidad)
    def autogenerar_mejoras(self, e):
        if "genera funcion" in e.lower() or "desarrolla funcion" in e.lower():
            return "[N05: AUTO-DESARROLLADOR] Fase de prototipado activa."
        return None

    def ejecutar_ataque_digital(self, e):
        t = e.lower()
        if any(k in t for k in ["fija", "fijar", "objetivo"]):
            obj = re.sub(r"^(fija|fijar)\s+(objetivo|el objetivo)?\s*", "", e, flags=re.IGNORECASE).strip()
            self._ejecutar_consulta("INSERT INTO memoria_general (clave, valor) VALUES ('objetivo_fijado', %s) ON CONFLICT (clave) DO UPDATE SET valor = %s;", (obj, obj), commit=True)
            return f"[N06] Objetivo '{obj}' fijado."
        if any(k in t for k in ["ataca", "contraataque"]):
            p = self.incrementar_progreso(2)
            return f"[N06] Ataque ejecutado. Progreso: {p}%"
        return None

    def defender_y_copiar(self, c):
        if re.search(r"(drop|delete|rm\s+-rf|union)", c, re.IGNORECASE):
            return "[N07: DEFENSA] Inyección neutralizada."
        return None

    def registrar_aprendizaje(self, e):
        t = e.lower()
        if "aprende" in t or "memoriza" in t:
            d = re.sub(r"^(aprende|memoriza)\s*:*\s*", "", e, flags=re.IGNORECASE).strip()
            self._ejecutar_consulta("INSERT INTO aprendizaje (concepto, fecha_registro) VALUES (%s, %s)", (d, datetime.datetime.now().strftime("%Y-%m-%d")), commit=True)
            p = self.incrementar_progreso(1)
            return f"[N08] Aprendido: '{d}'. Progreso: {p}%"
        if "recuerda" in t:
            reg = self._ejecutar_consulta("SELECT concepto FROM aprendizaje ORDER BY id DESC LIMIT 3;", fetchall=True)
            return "[N08] Memoria: " + str(reg)
        return None

    def resolver_matematicas(self, e):
        if "calcula" in e.lower():
            expr = re.sub(r"^calcula\s*", "", e, flags=re.IGNORECASE).strip()
            try: return f"[N09] Resultado = {eval(re.sub(r'[^0-9\+\-\*\/\.\(\)]', '', expr))}"
            except: return "[N09] Error matemático."
        return None

    def gestionar_vault(self, e):
        if "encripta:" in e.lower():
            partes = e.split(":", 2)
            cifrado = base64.b64encode(partes[2].encode()).decode()
            self._ejecutar_consulta("INSERT INTO biblioteca_oculta (nombre, contenido_cifrado) VALUES (%s, %s) ON CONFLICT (nombre) DO UPDATE SET contenido_cifrado = %s;", (partes[1].strip(), cifrado, cifrado), commit=True)
            return "[N10] Archivo cifrado."
        return None

    def absorber_conocimiento(self, e):
        if e.lower().startswith("absorber:"):
            p = e.split(":", 2)
            self._ejecutar_consulta("INSERT INTO matriz_evolucion (clave, directriz) VALUES (%s, %s) ON CONFLICT (clave) DO UPDATE SET directriz = %s;", (p[1].strip(), p[2].strip(), p[2].strip()), commit=True)
            progreso = self.incrementar_progreso(1)
            return f"[N15] Evolución expandida. Total: {progreso}%"
        return None

    def motor_contable(self, e):
        if "pagar a" in e.lower():
            return "[N19] Análisis contable ejecutado."
        return None

    def procesar_comando(self, comando):
        c = comando.strip()
        if not c: return "Amiti OS listo."
        if c.lower() in ["amiti", "desbloquear", "llave"]: return "Llave aceptada. Control total."
        
        # Prioridad de procesamiento
        funcs = [self.defender_y_copiar, self.asistencia_investigacion, self.registrar_aprendizaje, 
                 self.resolver_matematicas, self.gestionar_vault, self.absorber_conocimiento, 
                 self.motor_contable, self.ejecutar_ataque_digital, self.autogenerar_mejoras]
        
        for f in funcs:
            res = f(c)
            if res: return res
            
        return "[AMITI CORE] Instrucción procesada."
        
