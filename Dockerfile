# Base Stage: Install dependencies shared between dev and prod
FROM python:3.10-slim AS base

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Set Python to unbuffered mode (ensure logs show up in real-time) and set PYTHONPATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Development Stage
FROM base AS development

# Set environment variables for development
ENV TRANSLATION_SERVICE_PORT=50051
ENV FLASK_ENV=development

# Expose the gRPC port for development
EXPOSE 50051

# Command for running the gRPC server in development
CMD ["python", "src/app.py"]

# Production Stage
FROM base AS production

# Set environment variables for production
ENV TRANSLATION_SERVICE_PORT=50051
ENV FLASK_ENV=production

# Expose the gRPC port for production
EXPOSE 50051

# Command for running the gRPC server in production
CMD ["python", "src/app.py"]
