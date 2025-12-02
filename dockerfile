# ------------------------------------------------------------
# Stage 1: Builder - Install dependencies
# ------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
# RUN pip install --user --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --index-url https://pypi.org/simple -r requirements.txt



# ------------------------------------------------------------
# Stage 2: Runtime
# ------------------------------------------------------------
FROM python:3.11-slim

ENV TZ=UTC

WORKDIR /app

# Install cron + timezone tools
RUN apt-get update && \
    apt-get install -y cron tzdata && \
    rm -rf /var/lib/apt/lists/*

# Configure timezone to UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy project source
COPY . .

# Make required volume directories
RUN mkdir -p /data /cron && chmod -R 755 /data /cron

# Copy cron job to /cron (we will create next step)
# RUN cp cronjob /etc/cron.d/auth-cronjob     # Uncomment later

# Ensure cron has correct permissions
# RUN chmod 0644 /etc/cron.d/auth-cronjob     # Uncomment later
# RUN crontab /etc/cron.d/auth-cronjob        # Uncomment later

EXPOSE 8080

# Start cron in background + start API
CMD cron && uvicorn app.api:app --host 0.0.0.0 --port 8080
