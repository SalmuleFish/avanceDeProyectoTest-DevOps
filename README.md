# 🧮 Script de Cálculos Matemáticos y Estadísticos

Proyecto para la materia de **DevOps – Semestre 4**. Básicamente es un script en Python que hace un montón de cálculos matemáticos y los exporta a un archivo CSV bien organizado, pensado para que sea fácil de verificar con pruebas automatizadas.

## 📋 ¿Qué hace?

El script (`script.py`) ejecuta varias operaciones matemáticas y guarda todos los resultados en un archivo `resultados.csv`. Las secciones que genera son:

| Sección | Descripción |
|---|---|
| **Estadísticas descriptivas** | Media, mediana, desviación estándar, varianza, mínimo, máximo y rango de un conjunto de datos. |
| **Operaciones aritméticas** | Suma, resta, multiplicación, división, módulo y potencia entre pares de números. |
| **Trigonometría** | Seno, coseno y tangente de varios ángulos (en grados y radianes). |
| **Serie de Fibonacci** | Los primeros 20 números de la serie. |
| **Factoriales** | Factoriales del 1 al 12. |

## 🛠️ Requisitos

- **Python 3.10** o superior (se usan type hints como `list[float]`).
- No se necesitan librerías externas, todo funciona con la librería estándar (`csv`, `math`, `statistics`, `os`, `datetime`).

## 🚀 ¿Cómo se ejecuta?

Simplemente corre el script desde la terminal:

```bash
python script.py
```

Si todo sale bien, vas a ver un mensaje así:

```
✅ Reporte generado exitosamente: /ruta/al/proyecto/resultados.csv
```

El archivo `resultados.csv` se genera en la misma carpeta donde está el script.

## 📁 Estructura del proyecto

```
avance de proyecto/
├── script.py          # Script principal con todos los cálculos
├── resultados.csv     # Archivo generado al ejecutar el script
├── .gitignore         # Archivos ignorados por Git
└── README.md          # Este archivo
```

## 📊 Ejemplo de salida

El CSV generado tiene un formato como este:

```csv
=== REPORTE DE CÁLCULOS ===
Fecha de generación,2026-04-06 17:00:00

--- ESTADÍSTICAS DESCRIPTIVAS ---
Datos de entrada,23,45,12,67,34,89,56,78,11,99,42,55,37,61,73

Métrica,Valor
n,15
suma,782
media,52.133...
...
```

## 🤝 Notas

- El script maneja la **división entre cero** para que no truene: si el divisor es 0, simplemente pone `"indefinido"`.
- Lo mismo pasa con la **tangente de 90°** y ángulos equivalentes.
- El CSV incluye la fecha y hora de generación para saber cuándo se corrió.

---

Hecho con 💻 para la clase de DevOps.
