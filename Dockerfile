# Base Stage
FROM python:3.10-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies globally
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Development Stage
FROM base AS development

# Use a non-root user for security
RUN addgroup --system app && adduser --system --ingroup app app
USER app

# Development environment variables
ENV FLASK_ENV=development
ENV TRANSLATION_SERVICE_PORT=50051

# Expose port
EXPOSE 50051

CMD ["python", "src/app.py"]

# Production Stage
FROM base AS production

# Use a non-root user for production
RUN addgroup --system app && adduser --system --ingroup app app
USER app

# Production environment variables
ENV FLASK_ENV=production
ENV TRANSLATION_SERVICE_PORT=50051

# Expose port
EXPOSE 50051

CMD ["python", "src/app.py"]
