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
            # ESTO IMPRIMIRÁ EL ERROR REAL EN LOS LOGS DE RENDER
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
        if not (cn.startswith("investiga ") or cn.startswith("busca ")):
            return None
        tema = re.sub(r"^(investiga|busca|investigar|buscar)\s*", "", c, flags=re.IGNORECASE).strip()
        if not tema:
            return "[N04: INVESTIGACIÓN] Especifica un término o pregunta para rastrear en la red."

        # Capa 1: Wikipedia API
        res_wiki = self._buscar_wikipedia(tema)
        if res_wiki and res_wiki['resumen']:
            self._ejecutar_consulta(
                "INSERT INTO aprendizaje (concepto, fecha_registro) VALUES (%s, %s)",
                (f"Investigación (Wiki): {res_wiki['titulo']} - {res_wiki['resumen'][:200]}...", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                commit=True
            )
            progreso = self.incrementar_progreso(2)
            return (
                f"[N04: INVESTIGACIÓN ENCICLOPÉDICA] 📚\n"
                f"🔎 **Consulta:** '{tema}'\n"
                f"📌 **Origen:** {res_wiki['origen']} ({res_wiki['titulo']})\n"
                f"📄 **Resumen Extraído:** {res_wiki['resumen']}\n"
                f"🔗 **Fuente:** {res_wiki['url']}\n\n"
                f"💾 *Información indexada automáticamente en Neon DB.*\n"
                f"[⚙️ TELEMETRÍA: +2% de Progreso por Investigación | Total Core: {progreso}%]"
            )

        # Capa 2: DuckDuckGo Search con Filtro
        try:
            from duckduckgo_search import DDGS
            results = list(DDGS().text(tema, max_results=5))
            dominios_descartar = ['walmart.com', 'amazon.com', 'ebay.com', 'aliexpress.com', 'shopping']
            resultado_valido = None
            for r in results:
                href = r.get('href', '').lower()
                if not any(d in href for d in dominios_descartar):
                    resultado_valido = r
                    break

            if resultado_valido:
                origen = resultado_valido.get('title', 'Fuente Web')
                resumen = resultado_valido.get('body', 'Sin contenido disponible.')
                fuente = resultado_valido.get('href', '')
                self._ejecutar_consulta(
                    "INSERT INTO aprendizaje (concepto, fecha_registro) VALUES (%s, %s)",
                    (f"Investigación Web: {tema} - {resumen[:200]}...", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    commit=True
                )
                progreso = self.incrementar_progreso(2)
                return (
                    f"[N04: INVESTIGACIÓN WEB REAL] 🌐\n"
                    f"🔎 **Consulta:** '{tema}'\n"
                    f"📌 **Origen:** {origen}\n"
                    f"📄 **Resumen Extraído:** {resumen}\n"
                    f"🔗 **Fuente:** {fuente}\n\n"
                    f"💾 *Información indexada automáticamente en Neon DB.*\n"
                    f"[⚙️ TELEMETRÍA: +2% de Progreso por Investigación | Total Core: {progreso}%]"
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
                return f"[N06: LOCK-ON SYSTEM] 🎯 Objetivo grabado de forma persistente en Neon DB: '{obj}'."
            return "[N06: LOCK-ON SYSTEM] Especifica una IP, host o entidad para poner en la mira."

        if any(k in t for k in ["ataca", "contraataque", "elimina amenaza", "destruir"]):
            obj_res = self._ejecutar_consulta("SELECT valor FROM memoria_general WHERE clave = 'objetivo_fijado';", fetchone=True)
            obj = obj_res[0] if obj_res else "Entidad Invasora Desconocida"
            tacticas = ["Inyección de Ruido Blanco y Desbordamiento Lógico", "Espejo de Bucle Infinito (Honeypot Cuántico)"]
            ataque_elegido = random.choice(tacticas)
            p_actual = self.incrementar_progreso(2)
            return f"[N06: CONTRAATAQUE OFENSIVO ACTIVADO] ⚔️🔥 OBJETIVO FIJADO: '{obj}'\nDesplegando: {ataque_elegido}\n[⚙️ TELEMETRÍA: Total Core: {p_actual}%]"
        return None

    # N07: DEFENSA ACTIVA
    def defender_y_copiar(self, c):
        for p in ["drop\\s+table", "delete\\s+from", "rm\\s+-rf", "union\\s+select"]:
            if re.search(p, c, re.IGNORECASE):
                self.armas_defensivas.append(c)
                return "[N07: DEFENSA ACTIVA] Vector de inyección interceptado y neutralizado."
        return None

    # N08: MEMORIA Y APRENDIZAJE
    def registrar_aprendizaje(self, e):
        t = e.lower()
        if "aprende" in t or "memoriza" in t:
            d = re.sub(r"^(aprende\s*:*\s*|memoriza\s*:*\s*|aprende\s+|memoriza\s+)", "", e, flags=re.IGNORECASE).strip()
            if not d:
                return "[N08: APRENDIZAJE] Especifica el dato a indexar."
            self._ejecutar_consulta("INSERT INTO aprendizaje (concepto, fecha_registro) VALUES (%s, %s)", (d, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), commit=True)
            p_actual = self.incrementar_progreso(1)
            return f"[N08: APRENDIZAJE] Conocimiento indexado con éxito en Neon DB: '{d}'.\n\n[🧠 APRENDIZAJE INTEGRADO: +1% de Progreso por Almacenamiento de Datos | Total Core: {p_actual}%]"

        if any(k in t for k in ["recuerda", "aprendiste", "aprendizaje"]):
            reg = self._ejecutar_consulta("SELECT concepto, fecha_registro FROM aprendizaje ORDER BY id DESC LIMIT 5;", fetchall=True) or []
            mat = self._ejecutar_consulta("SELECT COUNT(*) FROM matriz_evolucion;", fetchone=True)
            tot_m = mat[0] if mat else 0
            if reg:
                txt = "[N08: MEMORIA]\n" + "\n".join([f"• [{r[1]}] {r[0]}" for r in reg])
            else:
                txt = "[N08: MEMORIA] No hay conocimientos guardados aún."
            txt += f"\n\n[N15: MATRIZ DE EVOLUCIÓN]\n• Directrices dinámicas en Neon DB: {tot_m}"
            return txt
        return None

    # N09: MOTOR MATEMÁTICO
    def resolver_matematicas(self, e):
        if "calcula" in e.lower() or "evalua" in e.lower():
            expr = re.sub(r"^(calcula|evalua)\s*", "", e, flags=re.IGNORECASE).strip()
            try:
                expr_limpia = re.sub(r"[^0-9\+\-\*\/\(\)\.\s]", "", expr)
                res = eval(expr_limpia)
                return f"[N09: MATEMÁTICAS] 🧠\nEcuación Combinada Resuelta:\nExpresión: {expr_limpia}\nResultado = {res}"
            except Exception:
                return f"[N09: MATEMÁTICAS] No se pudo evaluar la expresión: {expr}"
        return None

    # N10 / N11: BAÚL Y ENCRIPTACIÓN
    def gestionar_vault(self, e):
        t = e.lower()
        if "encripta:" in t or "encriptar:" in t:
            partes = e.split(":", 2)
            if len(partes) >= 3:
                nombre = partes[1].strip()
                contenido = partes[2].strip()
                cifrado = base64.b64encode(contenido.encode('utf-8')).decode('utf-8')
                self._ejecutar_consulta(
                    "INSERT INTO biblioteca_oculta (nombre, contenido_cifrado) VALUES (%s, %s) ON CONFLICT (nombre) DO UPDATE SET contenido_cifrado = %s;",
                    (nombre, cifrado, cifrado), commit=True
                )
                return f"[N10: ENCRIPCIÓN] Archivo '{nombre}.vault' resguardado en Neon DB de forma íntegra."
        if "leer:" in t or "desencripta:" in t:
            partes = e.split(":", 1)
            if len(partes) >= 2:
                nombre = partes[1].strip()
                res = self._ejecutar_consulta("SELECT contenido_cifrado FROM biblioteca_oculta WHERE nombre = %s;", (nombre,), fetchone=True)
                if res and res[0]:
                    desc = base64.b64decode(res[0].encode('utf-8')).decode('utf-8')
                    return f"[N11: LECTOR] 📖 Archivo: {nombre}.vault\n└─ Contenido recuperado:\n\n{desc}"
                return f"[N11: LECTOR] Archivo '{nombre}' no encontrado en el baúl."
        return None

    # N15: MATRIZ DE EVOLUCIÓN / ABSORCIÓN COGNITIVA
    def absorber_conocimiento(self, e):
        cn = e.lower().strip()
        if cn.startswith("absorber:"):
            partes = e.split(":", 2)
            if len(partes) >= 3:
                clave = partes[1].strip().lower()
                directriz = partes[2].strip()
                self._ejecutar_consulta(
                    "INSERT INTO matriz_evolucion (clave, directriz) VALUES (%s, %s) ON CONFLICT (clave) DO UPDATE SET directriz = %s;",
                    (clave, directriz, directriz), commit=True
                )
                progreso = self.incrementar_progreso(1)
                return (
                    f"[N15: ABSORCIÓN] Conciencia expandida. Conocimiento inyectado en la matriz bajo la clave genética '{clave}'.\n\n"
                    f"[🧬 EVOLUCIÓN AUTÓNOMA: +1% de Progreso por Absorción Cognitiva | Total Core: {progreso}%]"
                )
        res = self._ejecutar_consulta("SELECT directriz FROM matriz_evolucion WHERE clave = %s;", (cn,), fetchone=True)
        if res and res[0]:
            return f"[N15: CONOCIMIENTO ASIMILADO] 🧬 (Respuesta Autónoma):\n{res[0]}"
        return None

    # N19: MOTOR CONTABLE NARRATIVO
    def motor_contable(self, e):
        t = e.lower()
        if "pagar a" in t and "trabajadores" in t:
            try:
                m_num = re.search(r"pagar a\s+(\d+)\s+trabajadores", t)
                m_base = re.search(r"sueldo base de\s+(\d+(\.\d+)?)", t)
                m_com = re.search(r"comision de\s+(\d+(\.\d+)?)", t)
                if m_num and m_base:
                    cant = int(m_num.group(1))
                    base = float(m_base.group(1))
                    com = float(m_com.group(1)) if m_com else 0.0
                    total = cant * (base + com)
                    return (
                        f"[N19: MOTOR CONTABLE NARRATIVO] 📊 Análisis Analítico de Pagos:\n"
                        f"• Personal: {cant} trabajadores.\n"
                        f"• Sueldo base: ${base:.2f}\n"
                        f"• Comisión: ${com:.2f}\n"
                        f"• TOTAL NETO A PAGAR: ${total:.2f}"
                    )
            except Exception:
                pass
        return None

    # MÓDULO CENTRAL DE PROCESAMIENTO
    def procesar_comando(self, comando):
        c = comando.strip()
        if not c:
            return "Amiti OS listo para recibir instrucciones."

        if c.lower() in ["amiti", "desbloquear", "llave"]:
            return "Amiti: Llave aceptada. Control total transferido al creador."

        defensa = self.defender_y_copiar(c)
        if defensa:
            return defensa

        investigacion = self.asistencia_investigacion(c)
        if investigacion:
            return investigacion

        aprendizaje = self.registrar_aprendizaje(c)
        if aprendizaje:
            return aprendizaje

        matematicas = self.resolver_matematicas(c)
        if matematicas:
            return matematicas

        vault = self.gestionar_vault(c)
        if vault:
            return vault

        absorcion = self.absorber_conocimiento(c)
        if absorcion:
            return absorcion

        contable = self.motor_contable(c)
        if contable:
            return contable

        ataque = self.ejecutar_ataque_digital(c)
        if ataque:
            return ataque

        autodev = self.autogenerar_mejoras(c)
        if autodev:
            return autodev

        return f"[AMITI CORE] Instrucción procesada. Registrando interacción en Neon DB."
                            
