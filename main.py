from flask import Flask, request, render_template_string
# Importaremos nuestros módulos aquí
import modulos.asistencia as asistencia
import modulos.monitor as monitor
import modulos.contabilidad as contabilidad

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    canal = request.form.get("canal", "asistencia")
    msg = request.form.get("msg")
    
    # El Orquestador redirige al módulo correcto
    if canal == "monitor":
        respuesta = monitor.ejecutar(msg)
    elif canal == "contabilidad":
        respuesta = contabilidad.ejecutar(msg)
    else:
        respuesta = asistencia.ejecutar(msg)
        
    return render_template_string(template_base, respuesta=respuesta)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    
