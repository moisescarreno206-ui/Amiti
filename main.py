from flask import Flask, request, render_template_string
import datetime, os

app = Flask(__name__)

RED = {
    "conocimiento": ["AMITI Iniciado"],
    "logs": [{"t": "00:00", "m": "NUCLEO V9 OPERATIVO", "c": "cyan"}]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    modo = request.form.get("canal", "asistencia")
    msg = request.form.get("msg")
    
    if msg:
        if modo == "evolucion":
            RED["conocimiento"].append(msg)
            res = "Dato asimilado. Nivel: " + str(len(RED["conocimiento"]))
        elif modo == "seguridad":
            res = "REPORTANDO: Integridad 100%. Sin peligros detectados."
        else:
            res = "IA AMITI: Procesando comando: " + msg
            
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "NODO: " + msg, "c": "gray"})
        RED["logs"].append({"t": datetime.datetime.now().strftime("%H:%M"), "m": "AMITI: " + res, "c": "white"})
        if len(RED["logs"]) > 10: RED["logs"].pop(0)

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            :root { --border: #00ff41; --text1: #00ff41; }
            body { background: #000; color: var(--text1); font-family: monospace; margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: auto; }
            .panel { border: 2px solid var(--border); padding: 20px; margin-bottom: 15px; border-radius: 10px; }
            h2 { color: var(--border); text-align: center; }
            #logs { height: 300px; overflow-y: auto; }
            select, input, button { width: 100%; padding: 15px; margin: 10px 0; background: #000; color: var(--border); border: 2px solid var(--border); }
            button { background: var(--border); color: #000; font-weight: bold; cursor: pointer; }
