import os
import re
import psycopg2

class AmitiOS:
    def __init__(self):
        self.database_url = os.environ.get("DATABASE_URL")
        self.neon_database_url = os.environ.get("NEON_DATABASE_URL")
        self.inicializar_bbdd()

    def get_db_connection(self):
        """Conecta a Supabase (principal) o Neon DB (respaldo)."""
        if self.database_url:
            try:
                conn = psycopg2.connect(self.database_url, connect_timeout=5)
                return conn, "Supabase DB (Soberano)"
            except Exception as e:
                print(f"[WARN] Error conectando a Supabase: {e}")

        if self.neon_database_url:
            try:
                conn = psycopg2.connect(self.neon_database_url, connect_timeout=5)
                return conn, "Neon DB (Respaldo)"
            except Exception as e:
                print(f"[WARN] Error conectando a Neon DB: {e}")

        return None, "Almacenamiento Volátil en Memoria"

    def inicializar_bbdd(self):
        """Crea las tablas automáticamente al arrancar."""
        conn, engine = self.get_db_connection()
        if conn:
            try:
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
                print(f"✅ BBDD conectada correctamente en {engine}")
            except Exception as e:
                print(f"❌ Error inicializando BBDD: {e}")

    def procesar_calculo(self, texto):
        """Procesa operaciones matemáticas e intenciones financieras."""
        texto_lower = texto.lower()
        if any(k in texto_lower for k in ["trabajadores", "pagar", "comisión", "cuanto", "cuánto", "+", "*", "/", "-"]):
            numeros = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', texto)]
            
            # Cálculo de trabajadores + pago + comisión
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
            
            # Evaluación matemática general
            try:
                expresion = texto_lower.replace("más", "+").replace("mas", "+").replace("menos", "-").replace("por", "*")
                expresion_limpia = "".join([c for c in expresion if c in "0123456789+-*/()."])
                if expresion_limpia:
                    resultado = eval(expresion_limpia)
                    return f"🧮 **Resultado Matemático:** {expresion_limpia} = **{resultado}**"
            except:
                pass

        return None

    def responder(self, mensaje):
        """Genera la respuesta y registra el aprendizaje en la base de datos."""
        calculo = self.procesar_calculo(mensaje)
        if calculo:
            respuesta = calculo
        else:
            respuesta = f"🤖 [NÚCLEO ACTIVO] Comando procesado: '{mensaje}'. Todos mis sistemas están sincronizados y listos para ejecutar lo que pidas, creador. 🔊"

        # Guardar en base de datos
        conn, _ = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO memoria_amiti (entrada, respuesta) VALUES (%s, %s)", (mensaje, respuesta))
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error guardando memoria: {e}")

        return respuesta

# Instancia global por si app.py la importa directamente como objeto
amiti_os = AmitiOS()

