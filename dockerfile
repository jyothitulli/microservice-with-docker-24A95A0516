# =========================
# Stage 1: Build Python dependencies
# =========================
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies into /install (global, no --user)
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# =========================
# Stage 2: Final image
# =========================
FROM python:3.11-slim

# Set environment variables
ENV TZ=UTC
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install cron & tzdata
RUN apt-get update && \
    apt-get install -y cron tzdata && \
    rm -rf /var/lib/apt/lists/*

# Set timezone
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

# Copy Python dependencies from builder
COPY --from=builder /install /usr/local

# Copy project files
COPY . .

# Setup cron job
COPY cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron

# Create volumes
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Expose port
EXPOSE 8080

# Start cron in background, then start uvicorn
CMD ["sh", "-c", "cron && exec uvicorn app.main:app --host 0.]()
