# =========================
# Stage 1: Builder
# =========================
FROM python:3.11-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# (Optional but recommended if you have packages like pycryptodome that need compiling)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency file
COPY requirements.txt .

# Install dependencies into /install (will be copied to runtime image)
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt
    # If you still get index issues, you can try:
    # pip install --prefix=/install --no-cache-dir -r requirements.txt -i https://pypi.org/simple

# =========================
# Stage 2: Runtime
# =========================
FROM python:3.11-slim

ENV TZ=UTC
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies (only what you need at runtime)
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    rm -rf /var/lib/apt/lists/*

# Configure timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo "$TZ" > /etc/timezone

# Copy Python dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .
COPY cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron


# Create volume mount points
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Expose port
EXPOSE 8080

# Start cron and application
# Start cron in foreground and FastAPI on port 8080
RUN touch /var/log/cron.log

CMD ["sh", "-c", "cron -f & exec uvicorn app.main:app --host 0.0.0.0 --port 8080"]
