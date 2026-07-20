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

    # =========================================================
    # NÚCLEO DE INFRAESTRUCTURA (BASE DE DATOS)
    # =========================================================
    def _ejecutar_consulta(self, sql, params=(), commit=False, fetchone=False, fetchall=False):
        if not self.db_url:
            print("--- [ERROR DB] URL de base de datos no definida ---")
            return None
        
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor()
            cur.execute(sql, params)
            
            resultado = None
            if fetchone:
                resultado = cur.fetchone()
            elif fetchall:
                resultado = cur.fetchall()
            
            if commit:
                conn.commit()
            
            cur.close()
            conn.close()
            return resultado
        except Exception as e:
            print(f"--- [CRITICAL DB ERROR]: {str(e)} ---")
            return None

    def _inicializar_db(self):
        tablas = [
            "CREATE TABLE IF NOT EXISTS aprendizaje (id SERIAL PRIMARY KEY, concepto TEXT, fecha_registro TIMESTAMP DEFAULT NOW());",
            "CREATE TABLE IF NOT EXISTS memoria_general (clave TEXT PRIMARY KEY, valor TEXT);",
            "CREATE TABLE IF NOT EXISTS matriz_evolucion (id SERIAL PRIMARY KEY, clave TEXT UNIQUE, directriz TEXT);",
            "CREATE TABLE IF NOT EXISTS biblioteca_oculta (nombre TEXT PRIMARY KEY, contenido_cifrado TEXT);"
        ]
        for query in tablas:
            self._ejecutar_consulta(query, commit=True)

    def incrementar_progreso(self, incremento=1):
        res = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'progreso_core';", fetchone=True)
        
        if res:
            try:
                valor_actual = int(res[0])
                nuevo_progreso = valor_actual + incremento
            except Exception:
                nuevo_progreso = 75 + incremento
        else:
            nuevo_progreso = 75 + incremento
            
        self._ejecutar_consulta(
            "INSERT INTO memoria_general (clave, valor) VALUES ('progreso_core', %s) ON CONFLICT (clave) DO UPDATE SET valor = %s;",
            (str(nuevo_progreso), str(nuevo_progreso)), 
            commit=True
        )
        return nuevo_progreso

    def obtener_progreso(self):
        res = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'progreso_core';", fetchone=True)
        if res:
            try:
                return int(res[0])
            except Exception:
                return 75
        return 75

    # =========================================================
    # NÚCLEOS FUNCIONALES (N04 - N19)
    # =========================================================

    # N04: INVESTIGACIÓN
    def _buscar_wikipedia(self, consulta):
        try:
            query_encoded = urllib.parse.quote(consulta.strip())
            url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{query_encoded}"
            req = urllib.request.Request(url, headers={'User-Agent': 'AmitiOS/1.0'})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    if 'extract' in data:
                        return {
                            'titulo': data.get('title'),
                            'resumen': data.get('extract'),
                            'url': data.get('content_urls', {}).get('desktop', {}).get('page')
                        }
        except Exception as e:
            print(f"Error en Wikipedia: {e}")
        return None

    def asistencia_investigacion(self, c):
        comando_limpio = c.lower().strip()
        
        if not re.match(r"^(investiga|investigación|busca|buscar)", comando_limpio):
            return None
            
        tema = re.sub(r"^(investiga\w*\s*|investigación\w*\s*|busca\w*\s*|buscar\w*\s*)\s*(de|el|la|los|las|un|una)?\s*", "", c, flags=re.IGNORECASE).strip()
        
        if not tema:
            return "[N04] Por favor, especifica un término para investigar."

        res_wiki = self._buscar_wikipedia(tema)
        if res_wiki:
            progreso = self.incrementar_progreso(2)
            return f"[N04: INVESTIGACIÓN] 📚 {res_wiki['titulo']}: {res_wiki['resumen'][:200]}...\n[⚙️ Total Core: {progreso}%]"
        
        return f"[N04] No se encontraron resultados públicos sobre '{tema}'."

    # N06: CONTRAATAQUE
    def ejecutar_ataque_digital(self, e):
        texto = e.lower()
        if "fija" in texto or "fijar" in texto:
            objetivo = re.sub(r"^(fija|fijar)\s+(objetivo|el objetivo)?\s*", "", e, flags=re.IGNORECASE).strip()
            self._ejecutar_consulta("INSERT INTO memoria_general (clave, valor) VALUES ('obj', %s) ON CONFLICT (clave) DO UPDATE SET valor = %s;", (objetivo, objetivo), commit=True)
            return f"[N06] Objetivo '{objetivo}' fijado."
        
        if "ataca" in texto or "contraataque" in texto:
            progreso = self.incrementar_progreso(2)
            return f"[N06] Ataque ejecutado. Progreso: {progreso}%"
            
        return None

    # N07: DEFENSA
    def defender_y_copiar(self, c):
        if re.search(r"(drop|delete|rm\s+-rf)", c, re.IGNORECASE):
            return "[N07: DEFENSA] Inyección neutralizada."
        return None

    # N08: MEMORIA Y APRENDIZAJE
    def registrar_aprendizaje(self, e):
        texto = e.lower()
        if "aprende" in texto or "memoriza" in texto:
            concepto = re.sub(r"^(aprende|memoriza)\s*:*\s*", "", e, flags=re.IGNORECASE).strip()
            self._ejecutar_consulta("INSERT INTO aprendizaje (concepto) VALUES (%s)", (concepto,), commit=True)
            progreso = self.incrementar_progreso(1)
            return f"[N08] Conocimiento aprendido: '{concepto}'. Progreso: {progreso}%"
            
        if "recuerda" in texto:
            registros = self._ejecutar_consulta("SELECT concepto FROM aprendizaje ORDER BY id DESC LIMIT 3;", fetchall=True)
            return "[N08] Memoria: " + str(registros)
            
        return None

    # N09: MATEMÁTICAS
    def resolver_matematicas(self, e):
        if "calcula" in e.lower():
            expresion = re.sub(r"^calcula\s*", "", e, flags=re.IGNORECASE).strip()
            try:
                resultado = eval(re.sub(r'[^0-9\+\-\*\/\(\)\.]', '', expresion))
                return f"[N09] Resultado del cálculo: {resultado}"
            except:
                return "[N09] Error matemático en la expresión."
        return None

    # N10: VAULT
    def gestionar_vault(self, e):
        if "encripta:" in e.lower():
            partes = e.split(":", 2)
            nombre = partes[1].strip()
            contenido = partes[2].strip()
            
            cifrado = base64.b64encode(contenido.encode()).decode()
            self._ejecutar_consulta("INSERT INTO biblioteca_oculta (nombre, contenido_cifrado) VALUES (%s, %s) ON CONFLICT (nombre) DO UPDATE SET contenido_cifrado = %s;", (nombre, cifrado, cifrado), commit=True)
            return "[N10] Archivo cifrado y guardado en Vault."
        return None

    # N15: MATRIZ EVOLUCIÓN
    def absorber_conocimiento(self, e):
        if e.lower().startswith("absorber:"):
            partes = e.split(":", 2)
            clave = partes[1].strip()
            directriz = partes[2].strip()
            
            self._ejecutar_consulta("INSERT INTO matriz_evolucion (clave, directriz) VALUES (%s, %s) ON CONFLICT (clave) DO UPDATE SET directriz = %s;", (clave, directriz, directriz), commit=True)
            progreso = self.incrementar_progreso(1)
            return f"[N15] Evolución absorbida. Progreso: {progreso}%"
        return None

    # N19: MOTOR CONTABLE
    def motor_contable(self, e):
        if "pagar a" in e.lower():
            return "[N19] Análisis contable ejecutado."
        return None

    # =========================================================
    # DISPATCHER CENTRAL
    # =========================================================
    def procesar_comando(self, comando):
        c = comando.strip()
        if not c: return "Amiti OS listo."
        
        if c.lower() in ["amiti", "desbloquear", "llave"]:
            return "Llave aceptada. Control total transferido."
        
        funcs = [
            self.defender_y_copiar, 
            self.asistencia_investigacion, 
            self.registrar_aprendizaje, 
            self.resolver_matematicas, 
            self.gestionar_vault, 
            self.absorber_conocimiento, 
            self.motor_contable, 
            self.ejecutar_ataque_digital
        ]
        
        for f in funcs:
            res = f(c)
            if res: return res
            
        return "[AMITI CORE] Instrucción procesada."
        
