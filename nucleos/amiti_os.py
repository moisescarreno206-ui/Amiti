import os
import re

# Intentar importar psycopg2 de forma segura para Vercel
try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

class AmitiOS:
    def __init__(self):
        self.database_url = os.environ.get("DATABASE_URL")
        self.neon_database_url = os.environ.get("NEON_DATABASE_URL")
        try:
            self.inicializar_bbdd()
        except Exception as e:
            print(f"[ERROR] Inicialización diferida de BBDD: {e}")

    def get_db_connection(self):
        """Conecta a Supabase o Neon DB aplicando SSL automático para Vercel."""
        if not HAS_PSYCOPG2:
            return None, "Almacenamiento Volátil (Sin driver)"

        # 1. Intentar Supabase (Base Principal)
        if self.database_url:
            try:
                url = self.database_url
                if "sslmode=" not in url:
                    url += "?sslmode=require" if "?" not in url else "&sslmode=require"
                conn = psycopg2.connect(url, connect_timeout=4)
                return conn, "Supabase DB (Soberano)"
            except Exception as e:
                print(f"[WARN] Supabase temporalmente no disponible: {e}")

        # 2. Intentar Neon DB (Respaldo)
        if self.neon_database_url:
            try:
                url = self.neon_database_url
                if "sslmode=" not in url:
                    url += "?sslmode=require" if "?" not in url else "&sslmode=require"
                conn = psycopg2.connect(url, connect_timeout=4)
                return conn, "Neon DB (Respaldo)"
            except Exception as e:
                print(f"[WARN] Neon DB temporalmente no disponible: {e}")

        return None, "Almacenamiento Volátil en Memoria"

    def inicializar_bbdd(self):
        """Crea la estructura de tablas de forma segura."""
        try:
            conn, engine = self.get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS memoria_amiti (
                        id SERIAL PRIMARY KEY,
                        entrada TEXT NOT NULL,
                        respuesta TEXT NOT NULL,
                        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
                cursor.close()
                conn.close()
                print(f"✅ BBDD sincronizada en {engine}")
        except Exception as e:
            print(f"❌ Error al inicializar tablas: {e}")

    def procesar_calculo(self, texto):
        """Analiza intenciones matemáticas y financieras."""
        try:
            texto_lower = str(texto).lower()
            if any(k in texto_lower for k in ["trabajadores", "pagar", "comisión", "cuanto", "cuánto", "+", "*", "/", "-"]):
                numeros = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', texto)]
                
                if "trabajadores" in texto_lower and len(numeros) >= 3:
                    cant_trabajadores = numeros[0]
                    sueldo_base = numeros[1]
                    comision = numeros[2]
                    
                    pago_por_persona = sueldo_base + comision
                    total_global = cant_trabajadores * pago_por_persona
                    
                    return (
                        f"🧮 **Desglose Financiero Calculado:**\n"
                        f"* Pago base por trabajador: ${sueldo_base:.2f}\n"
                        f"* Comisión por trabajador: ${comision:.2f}\n"
                        f"* Total por trabajador: **${pago_por_persona:.2f}**\n\n"
                        f"💵 **Monto Total a Pagar ({int(cant_trabajadores)} trabajadores):** **${total_global:.2f}**"
                    )
                
                expresion = texto_lower.replace("más", "+").replace("mas", "+").replace("menos", "-").replace("por", "*")
                expresion_limpia = "".join([c for c in expresion if c in "0123456789+-*/()."])
                if expresion_limpia:
                    resultado = eval(expresion_limpia)
                    return f"🧮 **Resultado Matemático:** {expresion_limpia} = **{resultado}**"
        except Exception as e:
            print(f"Error procesando cálculo: {e}")

        return None

    def responder(self, mensaje):
        """Genera respuesta y guarda en memoria."""
        try:
            calculo = self.procesar_calculo(mensaje)
            if calculo:
                respuesta = calculo
            else:
                respuesta = f"🤖 [NÚCLEO ACTIVO] Comando procesado: '{mensaje}'. Todos mis sistemas están sincronizados y listos para ejecutar lo que pidas, creador. 🔊"

            try:
                conn, _ = self.get_db_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO memoria_amiti (entrada, respuesta) VALUES (%s, %s)", (mensaje, respuesta))
                    conn.commit()
                    cursor.close()
                    conn.close()
            except Exception as e:
                print(f"Error guardando memoria: {e}")

            return respuesta
        except Exception as e:
            return f"🤖 [NÚCLEO ACTIVO] Mensaje recibido: '{mensaje}'."

# Instancia para exportación
amiti_os = AmitiOS()
