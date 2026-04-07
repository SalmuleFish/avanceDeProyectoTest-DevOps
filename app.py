from flask import Flask, send_file
import calculos
import os

app = Flask(__name__)

@app.route('/')
def descargar_reporte():
    # Usamos /tmp para guardar el archivo temporalmente en el contenedor
    archivo_generado = calculos.generar_reporte_csv('/tmp')
    return send_file(archivo_generado, as_attachment=True, download_name='reporte_matematico.csv')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)