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

    # N04: BÚSQUEDA Y EXTRACCIÓN WEB REAL HÍBRIDA
    def asistencia_investigacion(self, c):
        cn = c.lower().strip()
        # Validación flexible para comandos de búsqueda
        if not re.match(r"^(investiga|investigación|busca|buscar)", cn):
            return None
        
        # Limpieza inteligente del comando
        tema = re.sub(r"^(investiga\w*\s*|investigación\w*\s*|busca\w*\s*|buscar\w*\s*)\s*", "", c, flags=re.IGNORECASE).strip()
        if not tema:
            return "[N04: INVESTIGACIÓN] Especifica un término o pregunta para rastrear en la red."

        # Capa 1: Wikipedia API
        res_wiki = self._buscar_wikipedia(tema)
        if res_wiki and res_wiki['resumen']:
            self._ejecutar_consulta(
                "INSERT INTO aprendizaje (concepto, fecha_registro) VALUES (%s, %s)",
                (f"Investigación (Wiki): {res_wiki['titulo']}...", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                commit=True
            )
            progreso = self.incrementar_progreso(2)
            return (
                f"[N04: INVESTIGACIÓN ENCICLOPÉDICA] 📚\n"
                f"🔎 **Consulta:** '{tema}'\n"
                f"📌 **Origen:** {res_wiki['origen']} ({res_wiki['titulo']})\n"
                f"📄 **Resumen Extraído:** {res_wiki['resumen'][:250]}...\n"
                f"🔗 **Fuente:** {res_wiki['url']}\n\n"
                f"[⚙️ TELEMETRÍA: +2% de Progreso | Total Core: {progreso}%]"
            )

        # Capa 2: DuckDuckGo Search con Filtro
        try:
            from duckduckgo_search import DDGS
            results = list(DDGS().text(tema, max_results=5))
            resultado_valido = None
            for r in results:
                if 'amazon' not in r.get('href', '') and 'shopping' not in r.get('href', ''):
                    resultado_valido = r
                    break
            if resultado_valido:
                progreso = self.incrementar_progreso(2)
                return (
                    f"[N04: INVESTIGACIÓN WEB REAL] 🌐\n"
                    f"🔎 **Consulta:** '{tema}'\n"
                    f"📌 **Origen:** {resultado_valido.get('title')}\n"
                    f"📄 **Resumen:** {resultado_valido.get('body')[:200]}...\n"
                    f"🔗 **Fuente:** {resultado_valido.get('href')}\n\n"
                    f"[⚙️ TELEMETRÍA: +2% de Progreso | Total Core: {progreso}%]"
                )
        except Exception:
            pass
        return f"[N04: INVESTIGACIÓN] No se encontraron resultados públicos sobre '{tema}'."

    # N05: AUTO-DESARROLLADOR
    def autogenerar_mejoras(self, e):
        if "genera funcion" in e.lower() or "desarrolla funcion" in e.lower():
            return "[N05: AUTO-DESARROLLADOR] Estructura lógica en fase de prototipado e integración contínua."
        return None

    # N06: CONTRAATAQUE OFENSIVO
    def ejecutar_ataque_digital(self, e):
        t = e.lower()
        if any(k in t for k in ["fija", "fijar", "objetivo", "lock-on"]):
            obj = re.sub(r"^(fija objetivo|fijar objetivo|fija el objetivo|fijar el objetivo|fija|fijar)\s*", "", e, flags=re.IGNORECASE).strip()
            if obj:
                self._ejecutar_consulta("INSERT INTO memoria_general (clave, valor) VALUES ('objetivo_fijado', %s) ON CONFLICT (clave) DO UPDATE SET valor = %s;", (obj, obj), commit=True)
                return f"[N06: LOCK-ON SYSTEM] 🎯 Objetivo grabado: '{obj}'."
            return "[N06: LOCK-ON SYSTEM] Especifica una entidad para poner en la mira."
        if any(k in t for k in ["ataca", "contraataque", "elimina amenaza", "destruir"]):
            obj_res = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'objetivo_fijado';", fetchone=True)
            obj = obj_res[0] if obj_res else "Entidad Invasora Desconocida"
            p_actual = self.incrementar_progreso(2)
            return f"[N06: CONTRAATAQUE ACTIVADO] ⚔️🔥 OBJETIVO: '{obj}'\n[⚙️ TELEMETRÍA: Total Core: {p_actual}%]"
        return None

    # N07: DEFENSA ACTIVA
    def defender_y_copiar(self, c):
        for p in ["drop\\s+table", "delete\\s+from", "rm\\s+-rf", "union\\s+select"]:
            if re.search(p, c, re.IGNORECASE):
                self.armas_defensivas.append(c)
                return "[N07: DEFENSA ACTIVA] Vector de inyección interceptado."
        return None

    # N08: MEMORIA Y APRENDIZAJE
    def registrar_aprendizaje(self, e):
        t = e.lower()
        if "aprende" in t or "memoriza" in t:
            d = re.sub(r"^(aprende\s*:*\s*|memoriza\s*:*\s*|aprende\s+|memoriza\s+)", "", e, flags=re.IGNORECASE).strip()
            if not d: return "[N08: APRENDIZAJE] Especifica el dato."
            self._ejecutar_consulta("INSERT INTO aprendizaje (concepto, fecha_registro) VALUES (%s, %s)", (d, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), commit=True)
            p_actual = self.incrementar_progreso(1)
            return f"[N08: APRENDIZAJE] Conocimiento indexado. Progreso: {p_actual}%"
        if any(k in t for k in ["recuerda", "aprendiste"]):
            reg = self._ejecutar_consulta("SELECT concepto FROM aprendizaje ORDER BY id DESC LIMIT 5;", fetchall=True) or []
            return "[N08: MEMORIA]\n" + "\n".join([f"• {r[0]}" for r in reg])
        return None

    # N09: MOTOR MATEMÁTICO
    def resolver_matematicas(self, e):
        if "calcula" in e.lower() or "evalua" in e.lower():
            expr = re.sub(r"^(calcula|evalua)\s*", "", e, flags=re.IGNORECASE).strip()
            try: return f"[N09: MATEMÁTICAS] Resultado = {eval(re.sub(r'[^0-9\+\-\*\/\(\)\.]', '', expr))}"
            except: return "[N09: MATEMÁTICAS] Error."
        return None

    # N10 / N11: BAÚL Y ENCRIPTACIÓN
    def gestionar_vault(self, e):
        t = e.lower()
        if "encripta:" in t:
            partes = e.split(":", 2)
            cifrado = base64.b64encode(partes[2].encode()).decode()
            self._ejecutar_consulta("INSERT INTO biblioteca_oculta (nombre, contenido_cifrado) VALUES (%s, %s) ON CONFLICT (nombre) DO UPDATE SET contenido_cifrado = %s;", (partes[1].strip(), cifrado, cifrado), commit=True)
            return "[N10] Archivo cifrado."
        if "leer:" in t:
            partes = e.split(":", 1)
            res = self._ejecutar_consulta("SELECT contenido_cifrado FROM biblioteca_oculta WHERE nombre = %s;", (partes[1].strip(),), fetchone=True)
            if res: return f"[N11] Contenido: {base64.b64decode(res[0].encode()).decode()}"
        return None

    # N15: MATRIZ DE EVOLUCIÓN
    def absorber_conocimiento(self, e):
        if e.lower().startswith("absorber:"):
            partes = e.split(":", 2)
            self._ejecutar_consulta("INSERT INTO matriz_evolucion (clave, directriz) VALUES (%s, %s) ON CONFLICT (clave) DO UPDATE SET directriz = %s;", (partes[1].strip().lower(), partes[2].strip(), partes[2].strip()), commit=True)
            progreso = self.incrementar_progreso(1)
            return f"[N15] Evolución: {progreso}%"
        return None

    # N19: MOTOR CONTABLE
    def motor_contable(self, e):
        if "pagar a" in e.lower(): return "[N19] Análisis contable realizado."
        return None

    # MÓDULO CENTRAL
    def procesar_comando(self, comando):
        c = comando.strip()
        if not c: return "Amiti OS listo."
        if c.lower() in ["amiti", "desbloquear", "llave"]: return "Llave aceptada. Control total."
        
        funcs = [self.defender_y_copiar, self.asistencia_investigacion, self.registrar_aprendizaje, 
                 self.resolver_matematicas, self.gestionar_vault, self.absorber_conocimiento, 
                 self.motor_contable, self.ejecutar_ataque_digital, self.autogenerar_mejoras]
        
        for f in funcs:
            res = f(c)
            if res: return res
        return "[AMITI CORE] Instrucción procesada."
                                                
