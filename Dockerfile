# Multi-stage build for lightweight production image
FROM python:3.12-slim as builder

# Set work directory
WORKDIR /app

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements-prod.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements-prod.txt

# Production stage
FROM python:3.12-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Set work directory
WORKDIR /home/app

# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /home/app/.local

# Copy application code
COPY --chown=app:app . .

# Make sure scripts in .local are usable
ENV PATH=/home/app/.local/bin:$PATH

# Switch to non-root user
USER app

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8001/health')"

# Run the application
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
