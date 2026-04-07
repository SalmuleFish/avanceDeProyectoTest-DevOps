# --- Etapa 1: Construcción (Builder) ---
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
# Instalamos dependencias en una carpeta local
RUN pip install --user -r requirements.txt

# --- Etapa 2: Producción ---
FROM python:3.10-slim
WORKDIR /app
# Copiamos solo las dependencias instaladas de la etapa 1
COPY --from=builder /root/.local /root/.local
COPY . .

# Agregamos la ruta al PATH
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000

CMD ["python", "app.py"]