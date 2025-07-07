FROM python:3.10-slim AS base
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* \
    && GRPCURL_VERSION=1.8.7 \
    && curl -sSL https://github.com/fullstorydev/grpcurl/releases/download/v${GRPCURL_VERSION}/grpcurl_${GRPCURL_VERSION}_linux_arm64.tar.gz -o grpcurl.tar.gz \
    && tar -xzf grpcurl.tar.gz -C /usr/local/bin grpcurl \
    && rm grpcurl.tar.gz

# Copy and install Python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

FROM base AS development
# Create non-root user
RUN addgroup --system app && adduser --system --ingroup app app

# Copy health check script
COPY scripts/health-check.sh /usr/local/bin/health-check
RUN chmod +x /usr/local/bin/health-check

# Copy application code
COPY . .

# Set permissions
RUN chown -R app:app /app
USER app

# Set environment variables
ENV FLASK_ENV=development
ENV TRANSLATION_SERVICE_PORT=50051
ENV LOG_LEVEL=DEBUG

# Expose port
EXPOSE 50051

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD health-check || exit 1

# Start application
CMD ["python", "src/app.py"]

FROM base AS production
# Create non-root user
RUN addgroup --system app && adduser --system --ingroup app app

# Copy health check script
COPY scripts/health-check.sh /usr/local/bin/health-check
RUN chmod +x /usr/local/bin/health-check

# Copy application code
COPY . .

# Set permissions
RUN chown -R app:app /app
USER app

# Set environment variables
ENV FLASK_ENV=production
ENV TRANSLATION_SERVICE_PORT=50051
ENV LOG_LEVEL=INFO

# Expose port
EXPOSE 50051

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD health-check || exit 1

# Start application
CMD ["python", "src/app.py"]
