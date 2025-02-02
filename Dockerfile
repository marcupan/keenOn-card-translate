# services/keenOn-card-translate/Dockerfile

FROM python:3.10-slim AS base
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libssl-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Development Stage
FROM base AS development
RUN addgroup --system app && adduser --system --ingroup app app
USER app
ENV FLASK_ENV=development
ENV TRANSLATION_SERVICE_PORT=50051
EXPOSE 50051
CMD ["python", "src/app.py"]

# Production Stage
FROM base AS production
RUN addgroup --system app && adduser --system --ingroup app app
USER app
ENV FLASK_ENV=production
ENV TRANSLATION_SERVICE_PORT=50051
EXPOSE 50051
CMD ["python", "src/app.py"]
