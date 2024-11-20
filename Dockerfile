# Development Stage
FROM python:3.9-slim AS development

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app/src

WORKDIR /app

# Install pip and upgrade to latest version to avoid issues
RUN pip install --upgrade pip

COPY requirements.txt ./

# Install dependencies with increased timeout and alternative mirror for reliability
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

EXPOSE 5000 50051

CMD ["python3", "-u", "src/app.py"]

# Production Stage
FROM python:3.9-slim AS production

ENV FLASK_APP=src/app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app/src

WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

COPY requirements.txt ./

# Install dependencies with increased timeout and alternative mirror for reliability
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

EXPOSE 5000 50051

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.app:app"]
