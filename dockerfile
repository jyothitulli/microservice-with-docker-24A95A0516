FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --prefix=/install --no-cache-dir -r requirements.txt


FROM python:3.11-slim

ENV TZ=UTC

WORKDIR /app

# Install cron and tzdata
RUN apt-get update && \
    apt-get install -y cron tzdata && \
    rm -rf /var/lib/apt/lists/*

RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

# Copy app and dependencies
COPY --from=builder /install /usr/local
COPY . .

# Copy cron job file
COPY cron/cron.sh /cron/cron.sh
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Set permissions
RUN chmod +x /cron/cron.sh
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron

# Create folders for data/logs
RUN mkdir -p /data /logs /cron && chmod 755 /data /logs /cron

EXPOSE 8080

# Start cron and FastAPI
CMD service cron start && uvicorn app.main:app --host 0.0.0.0 --port 8080
