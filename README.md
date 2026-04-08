# 🧮 Reporte Matemático – Aplicación Web Dockerizada

Proyecto para la materia de **DevOps – Semestre 4**. Es una aplicación web hecha con Flask que genera un reporte CSV con cálculos matemáticos y estadísticos, empaquetada en un contenedor Docker y con infraestructura como código (IaC) para desplegarse en **AWS**.

## 📋 ¿Qué hace?

Al abrir la aplicación en el navegador, se muestra una **interfaz gráfica** con un botón para generar y descargar el reporte. Al hacer clic, se genera al vuelo un archivo `reporte_matematico.csv` con las siguientes secciones:

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
├── templates/
│   └── index.html       # Interfaz gráfica (página principal)
├── requirements.txt     # Dependencias de Python (Flask 3.0.3)
├── Dockerfile           # Imagen Docker con multi-stage build
├── docker-compose.yml   # Orquestación del contenedor (local)
├── infraestructura.yaml # CloudFormation – infraestructura AWS
├── buildspec.yml        # Especificación de build para AWS CodeBuild
├── .gitignore           # Archivos ignorados por Git
└── README.md            # Este archivo
```

### Descripción de archivos clave

- **`app.py`** – Levanta un servidor Flask en el puerto `5000`. Tiene dos rutas:
  - `/` – Muestra la interfaz gráfica (`index.html`).
  - `/descargar` – Ejecuta los cálculos y devuelve el CSV como descarga.
- **`templates/index.html`** – Página HTML con un botón que apunta a `/descargar` para generar y bajar el reporte.
- **`calculos.py`** – Contiene las funciones de cálculo (estadísticas, aritmética, trigonometría, Fibonacci, factoriales) y la función `generar_reporte_csv()` que arma el CSV completo. También se puede ejecutar de forma independiente (`python calculos.py`) para generar el reporte localmente.
- **`Dockerfile`** – Usa un **multi-stage build** con `python:3.10-slim` para mantener la imagen liviana.
- **`docker-compose.yml`** – Define el servicio `web` y mapea el puerto `8080` (host) al `5000` (contenedor), dentro de una red personalizada (`stf-network`).
- **`infraestructura.yaml`** – Template de **AWS CloudFormation** que crea una instancia EC2 (`t2.micro`) con un Security Group que permite SSH (22) y Flask (5000). El `UserData` instala Docker, clona el repo, construye la imagen y levanta el contenedor automáticamente.
- **`buildspec.yml`** – Archivo de configuración para **AWS CodeBuild**. Valida el entorno, construye la imagen Docker y empaqueta todos los archivos como artefactos.

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

La aplicación estará disponible en **http://localhost:8080**. Se mostrará una página con un botón para generar y descargar el archivo `reporte_matematico.csv`.

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

## ☁️ Despliegue en AWS

### Infraestructura (CloudFormation)

El archivo `infraestructura.yaml` define la infraestructura completa en AWS:

| Recurso | Tipo | Detalle |
|---|---|---|
| **MiSecurityGroup** | `AWS::EC2::SecurityGroup` | Abre puertos 22 (SSH) y 5000 (Flask) |
| **InstanciaProyectoSTF** | `AWS::EC2::Instance` | `t2.micro` con Amazon Linux, instala Docker vía `UserData` |

Para desplegar:

```bash
aws cloudformation create-stack --stack-name stf-proyecto --template-body file://infraestructura.yaml
```

El script de `UserData` se ejecuta automáticamente al arrancar la instancia: actualiza el sistema, instala Docker y Git, clona el repositorio, construye la imagen y levanta el contenedor.

### CI/CD (CodeBuild)

El archivo `buildspec.yml` se usa con **AWS CodeBuild** para validar que el proyecto se construye correctamente:

1. **pre_build** – Valida el entorno y lista los archivos.
2. **build** – Construye la imagen Docker (`mi-app-stf:latest`).
3. **post_build** – Confirma que todo está listo.

Los artefactos incluyen todos los archivos del proyecto (`**/*`).

## 🤝 Notas

- La **división entre cero** está manejada: si el divisor es 0, devuelve `"indefinido"`.
- Lo mismo para la **tangente de 90°** y ángulos equivalentes.
- El CSV incluye la fecha y hora de generación.
- El servidor guarda el CSV temporalmente en `/tmp` dentro del contenedor para no escribir en el directorio de la aplicación.

---

Hecho con 💻 para la clase de DevOps.
