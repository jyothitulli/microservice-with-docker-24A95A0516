# =========================
# Stage 1: Builder
# =========================
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies into /install (global)
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# =========================
# Stage 2: Runtime
# =========================
FROM python:3.11-slim

# Set environment variable
ENV TZ=UTC
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y cron tzdata && \
    rm -rf /var/lib/apt/lists/*

# Configure timezone
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

# Copy Python dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Create volume mount points
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Expose port
EXPOSE 8080

# Start cron and application
CMD ["sh", "-c", "cron && exec uvicorn app.main:app --host 0.0.0.0 --port 8080"]
