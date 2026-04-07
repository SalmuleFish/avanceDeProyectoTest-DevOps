# 🧮 Reporte Matemático – Aplicación Web Dockerizada

Proyecto para la materia de **DevOps – Semestre 4**. Es una aplicación web hecha con Flask que genera un reporte CSV con cálculos matemáticos y estadísticos, empaquetada en un contenedor Docker listo para producción.

## 📋 ¿Qué hace?

Al visitar la ruta principal (`/`) del servidor, la aplicación genera al vuelo un archivo `reporte_matematico.csv` y lo descarga automáticamente. El reporte incluye las siguientes secciones:

| Sección | Descripción |
|---|---|
| **Estadísticas descriptivas** | Media, mediana, desviación estándar, varianza, mínimo, máximo y rango de un conjunto de datos. |
| **Operaciones aritméticas** | Suma, resta, multiplicación, división, módulo y potencia entre pares de números. |
| **Trigonometría** | Seno, coseno y tangente de varios ángulos (en grados y radianes). |
| **Serie de Fibonacci** | Los primeros 20 números de la serie. |
| **Factoriales** | Factoriales del 1 al 12. |

## 📁 Estructura del proyecto

```
avanceProyecto/
├── app.py               # Servidor web Flask (punto de entrada)
├── calculos.py          # Módulo con toda la lógica de cálculos y generación del CSV
├── requirements.txt     # Dependencias de Python (Flask 3.0.3)
├── Dockerfile           # Imagen Docker con multi-stage build
├── docker-compose.yml   # Orquestación del contenedor
├── .gitignore           # Archivos ignorados por Git
└── README.md            # Este archivo
```

### Descripción de archivos clave

- **`app.py`** – Levanta un servidor Flask en el puerto `5000`. En la ruta `/` llama a `calculos.generar_reporte_csv()` y devuelve el CSV como descarga.
- **`calculos.py`** – Contiene las funciones de cálculo (estadísticas, aritmética, trigonometría, Fibonacci, factoriales) y la función `generar_reporte_csv()` que arma el CSV completo. También se puede ejecutar de forma independiente (`python calculos.py`) para generar el reporte localmente.
- **`Dockerfile`** – Usa un **multi-stage build** con `python:3.10-slim` para mantener la imagen liviana.
- **`docker-compose.yml`** – Define el servicio `web` y mapea el puerto `8080` (host) al `5000` (contenedor), dentro de una red personalizada (`stf-network`).

## 🛠️ Requisitos

### Ejecución local (sin Docker)
- **Python 3.10** o superior.
- Instalar dependencias:
  ```bash
  pip install -r requirements.txt
  ```

### Ejecución con Docker
- **Docker** y **Docker Compose** instalados.

## 🚀 ¿Cómo se ejecuta?

### Opción 1: Con Docker Compose (recomendado)

```bash
docker-compose up --build
```

La aplicación estará disponible en **http://localhost:8080**. Al abrir esa URL en el navegador, se descargará automáticamente el archivo `reporte_matematico.csv`.

### Opción 2: Solo con Docker

```bash
docker build -t reporte-matematico .
docker run -p 8080:5000 reporte-matematico
```

### Opción 3: Ejecución local (sin Docker)

```bash
pip install -r requirements.txt
python app.py
```

El servidor arrancará en **http://localhost:5000**.

### Opción 4: Generar el CSV directamente (sin servidor)

```bash
python calculos.py
```

Se generará `resultados.csv` en la misma carpeta.

## 🐳 Detalles de Docker

El `Dockerfile` usa **multi-stage build** para optimizar el tamaño de la imagen:

1. **Etapa builder** – Instala las dependencias de Python en una carpeta local.
2. **Etapa producción** – Copia solo las dependencias compiladas y el código fuente, sin herramientas de compilación innecesarias.

```
Puerto expuesto: 5000 (interno)
Puerto mapeado:  8080 (host) → 5000 (contenedor)
Red:             stf-network (bridge)
```

## 📊 Ejemplo de salida (CSV)

```csv
=== REPORTE DE CÁLCULOS ===
Fecha de generación,2026-04-07 17:00:00

--- ESTADÍSTICAS DESCRIPTIVAS ---
Datos de entrada,23,45,12,67,34,89,56,78,11,99,42,55,37,61,73

Métrica,Valor
n,15
suma,782
media,52.133...
...
```

## 🤝 Notas

- La **división entre cero** está manejada: si el divisor es 0, devuelve `"indefinido"`.
- Lo mismo para la **tangente de 90°** y ángulos equivalentes.
- El CSV incluye la fecha y hora de generación.
- El servidor guarda el CSV temporalmente en `/tmp` dentro del contenedor para no escribir en el directorio de la aplicación.

---

Hecho con 💻 para la clase de DevOps.
