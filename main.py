import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def ver_historial():
    try:
        if os.path.exists("contingencia.log"):
            with open("contingencia.log", "r", encoding="utf-8") as f:
                lineas = f.readlines()
        else:
            lineas = []

        html = """
        <html>
        <head>
            <title>Panel AMITI OS</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 20px; }
                h2 { color: #58a6ff; border-bottom: 2px solid #21262d; padding-bottom: 10px; }
                .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 15px; margin-bottom: 15px; }
                .danger { color: #f85149; font-weight: bold; }
                .geo { color: #56d364; }
                .footer { font-size: 0.8em; color: #8b949e; margin-top: 30px; text-align: center; }
            </style>
        </head>
        <body>
            <h2>🛰️ AMITI IA - HISTORIAL DE ALERTAS NUBE</h2>
        """

        if not lineas:
            html += "<p style='color:#8b949e;'>[SISTEMA LIMPIO] No hay alertas registradas en la base de datos.</p>"
        else:
            for linea in reversed(lineas):
