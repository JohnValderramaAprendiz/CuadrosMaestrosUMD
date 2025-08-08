from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from automatizacion_cm01 import generar_reporte_cm1
from automatizacion_cm09 import generar_reporte_practicas
from automatizacion_cm20 import generar_reporte_final_con_condicional
from automatizacion_cm03 import generar_reporte_profesores
from automatizacion_cm10 import generar_reporte_proyeccion_social

app = Flask(__name__)
CORS(app)

# Ruta base del proyecto (ajusta si es necesario)
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BASE_PATH = os.path.normpath(BASE_PATH)

@app.route('/generar_reporte', methods=['POST'])
def generar_reporte():
    data = request.json
    plantilla = int(data.get('plantilla', 0))
    codigo = int(data.get('codigo', 0))

    if not plantilla or not codigo:
        return jsonify({'error': 'Faltan datos de plantilla o código'}), 400

    if plantilla == 1:
        resultado, error = generar_reporte_cm1(codigo, BASE_PATH)
    elif plantilla == 3:
        resultado, error = generar_reporte_profesores(codigo, BASE_PATH)
    elif plantilla == 9:
        resultado, error = generar_reporte_practicas(codigo, BASE_PATH)
    elif plantilla == 10:
        resultado, error = generar_reporte_proyeccion_social(codigo, BASE_PATH)
    elif plantilla == 20:
        resultado, error = generar_reporte_final_con_condicional(codigo, BASE_PATH)
    else:
        return jsonify({'error': 'Plantilla no soportada'}), 400

    if error:
        return jsonify({'error': error}), 400

    if not os.path.exists(resultado):
        return jsonify({'error': 'No se pudo generar el archivo'}), 500

    # Enviar el archivo generado para descarga
    return send_file(resultado, as_attachment=True)

# Ruta para servir archivos estáticos (HTML)
@app.route('/')
def index():
    try:
        return send_file(os.path.join(BASE_PATH, 'principal.html'))
    except:
        return send_file('principal.html')

@app.route('/plantillas')
def plantillas():
    try:
        return send_file(os.path.join(BASE_PATH, 'plantillas.html'))
    except:
        return send_file('plantillas.html')

@app.route('/instructivo')
def instructivo():
    try:
        return send_file(os.path.join(BASE_PATH, 'instructivo.html'))
    except:
        return send_file('instructivo.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 