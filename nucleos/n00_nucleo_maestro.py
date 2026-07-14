class NucleoMaestro:
    def __init__(self):
        self.bloqueado = True

    def procesar(self, comando):
        cmd = comando.strip().lower()
        
        # 1. Autenticación
        if cmd == "amiti":
            self.bloqueado = False
            return "Hola, creador. En qué puedo ayudarte? Estoy lista para evolucionar."
        
        if self.bloqueado:
            return "SISTEMA BLOQUEADO. Requiere secuencia de acceso."

        # 2. Núcleo 17: Inteligencia Computacional (Nueva lógica)
        return self._ejecutar_logica(cmd)

    def _ejecutar_logica(self, cmd):
        # Ejemplo: Lógica simple de cálculo
        if "cuanto es" in cmd:
            try:
                # Extrae los números y calcula
                numeros = [int(s) for s in cmd.split() if s.isdigit()]
                if len(numeros) >= 2:
                    resultado = sum(numeros) # Esto es una base, iremos a más
                    return f"Cálculo completado. El resultado es {resultado}."
            except:
                return "Error en el cálculo. Asegúrate de ingresar números claros."
        
        return f"Misión '{cmd}' registrada. Estoy analizando cómo procesarla."

amiti = NucleoMaestro()
