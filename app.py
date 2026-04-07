from flask import Flask, send_file, render_template
import calculos

app = Flask(__name__)

@app.route('/')
def inicio():
    # Muestra la interfaz gráfica
    return render_template('index.html')

@app.route('/descargar')
def descargar_reporte():
    # Hace los cálculos y descarga el archivo
    archivo_generado = calculos.generar_reporte_csv('/tmp')
    return send_file(archivo_generado, as_attachment=True, download_name='reporte_matematico.csv')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)