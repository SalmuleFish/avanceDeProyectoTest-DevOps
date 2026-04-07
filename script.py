"""
Script de cálculos matemáticos y estadísticos.
Genera un archivo CSV con los resultados para pruebas.
"""

import csv
import math
import os
import statistics
from datetime import datetime


def calcular_estadisticas(datos: list[float]) -> dict:
    """Calcula estadísticas descriptivas de una lista de números."""
    return {
        "n": len(datos),
        "suma": sum(datos),
        "media": statistics.mean(datos),
        "mediana": statistics.median(datos),
        "desviacion_estandar": round(statistics.stdev(datos), 4),
        "varianza": round(statistics.variance(datos), 4),
        "minimo": min(datos),
        "maximo": max(datos),
        "rango": max(datos) - min(datos),
    }


def calcular_operaciones(a: float, b: float) -> dict:
    """Realiza operaciones aritméticas entre dos números."""
    resultado = {
        "a": a,
        "b": b,
        "suma": a + b,
        "resta": a - b,
        "multiplicacion": a * b,
        "potencia": a ** b,
    }
    if b != 0:
        resultado["division"] = round(a / b, 4)
        resultado["modulo"] = a % b
    else:
        resultado["division"] = "indefinido"
        resultado["modulo"] = "indefinido"
    return resultado


def calcular_trigonometria(angulos_grados: list[float]) -> list[dict]:
    """Calcula seno, coseno y tangente para una lista de ángulos en grados."""
    resultados = []
    for grado in angulos_grados:
        rad = math.radians(grado)
        resultados.append({
            "angulo_grados": grado,
            "angulo_radianes": round(rad, 4),
            "seno": round(math.sin(rad), 4),
            "coseno": round(math.cos(rad), 4),
            "tangente": round(math.tan(rad), 4) if grado % 180 != 90 else "indefinido",
        })
    return resultados


def calcular_fibonacci(n: int) -> list[int]:
    """Genera los primeros n números de la serie de Fibonacci."""
    if n <= 0:
        return []
    serie = [0, 1]
    while len(serie) < n:
        serie.append(serie[-1] + serie[-2])
    return serie[:n]


def calcular_factoriales(n: int) -> list[dict]:
    """Calcula los factoriales del 1 al n."""
    return [{"numero": i, "factorial": math.factorial(i)} for i in range(1, n + 1)]


def generar_reporte_csv(ruta_salida: str) -> str:
    """Genera un archivo CSV con todos los resultados de los cálculos."""

    # --- Datos de entrada ---
    datos_muestra = [23, 45, 12, 67, 34, 89, 56, 78, 11, 99, 42, 55, 37, 61, 73]
    pares_operaciones = [(10, 3), (25, 5), (100, 7), (50, 0), (8, 2)]
    angulos = [0, 30, 45, 60, 90, 120, 135, 150, 180, 270, 360]
    cantidad_fibonacci = 20
    cantidad_factoriales = 12

    ruta_completa = os.path.join(ruta_salida, "resultados.csv")

    with open(ruta_completa, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)

        # Encabezado general
        writer.writerow(["=== REPORTE DE CÁLCULOS ==="])
        writer.writerow(["Fecha de generación", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow([])

        # --- Sección 1: Estadísticas ---
        writer.writerow(["--- ESTADÍSTICAS DESCRIPTIVAS ---"])
        stats = calcular_estadisticas(datos_muestra)
        writer.writerow(["Datos de entrada"] + datos_muestra)
        writer.writerow([])
        writer.writerow(["Métrica", "Valor"])
        for clave, valor in stats.items():
            writer.writerow([clave, valor])
        writer.writerow([])

        # --- Sección 2: Operaciones aritméticas ---
        writer.writerow(["--- OPERACIONES ARITMÉTICAS ---"])
        writer.writerow(["a", "b", "suma", "resta", "multiplicación", "división", "módulo", "potencia"])
        for a, b in pares_operaciones:
            ops = calcular_operaciones(a, b)
            writer.writerow([
                ops["a"], ops["b"], ops["suma"], ops["resta"],
                ops["multiplicacion"], ops["division"], ops["modulo"], ops["potencia"],
            ])
        writer.writerow([])

        # --- Sección 3: Trigonometría ---
        writer.writerow(["--- TRIGONOMETRÍA ---"])
        writer.writerow(["Ángulo (°)", "Ángulo (rad)", "Seno", "Coseno", "Tangente"])
        for fila in calcular_trigonometria(angulos):
            writer.writerow([
                fila["angulo_grados"], fila["angulo_radianes"],
                fila["seno"], fila["coseno"], fila["tangente"],
            ])
        writer.writerow([])

        # --- Sección 4: Fibonacci ---
        writer.writerow(["--- SERIE DE FIBONACCI ---"])
        serie = calcular_fibonacci(cantidad_fibonacci)
        writer.writerow(["Índice", "Valor"])
        for i, valor in enumerate(serie):
            writer.writerow([i, valor])
        writer.writerow([])

        # --- Sección 5: Factoriales ---
        writer.writerow(["--- FACTORIALES ---"])
        writer.writerow(["Número", "Factorial"])
        for fila in calcular_factoriales(cantidad_factoriales):
            writer.writerow([fila["numero"], fila["factorial"]])

    return ruta_completa


# --- Punto de entrada ---
if __name__ == "__main__":
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_generado = generar_reporte_csv(directorio_actual)
    print(f"✅ Reporte generado exitosamente: {archivo_generado}")
