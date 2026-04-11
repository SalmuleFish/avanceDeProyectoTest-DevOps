# --- Construccion ---
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
# Dependencias en una carpeta local
RUN pip install --user -r requirements.txt

# --- Produccion ---
FROM python:3.10-slim
WORKDIR /app
# Copiamos dependencias instaladas
COPY --from=builder /root/.local /root/.local
COPY . .

# Ruta al PATH
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000

CMD ["python", "app.py"]