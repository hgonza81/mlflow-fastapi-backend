# Use Python 3.11 slim Debian image
FROM python:3.11-slim

# Set working directory.
WORKDIR /app

# Set environment variables, disable .pyc, log buffer and add /app to the path.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies, -y yes to all, and don't install recommended packages, only the required ones.
# build-essentials is required to compile dependencies with C code, and curl is a practical tool for health checks.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies. Upgrade pip and install libraries in requiremetns.txt (-r)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code, it keeps the access modes (rwx) but the owner is the root user for now.
COPY app/ ./app/
COPY .env .env
COPY entrypoint.sh ./entrypoint.sh

# Make entrypoint executable and create a non-root user "appuser" and makes him the owner of the app.
RUN chmod +x ./entrypoint.sh \
    && adduser --disabled-password --gecos '' --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8001

# Health check: Marks the container as healty or unhealthy
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${API_PORT:-8001}/health || exit 1

# Use entrypoint script for flexible configuration
ENTRYPOINT ["./entrypoint.sh"]