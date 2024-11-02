FROM python:3.9-slim AS development

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/usr/src/app

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50051

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=50051"]

FROM python:3.9-slim AS production

ENV FLASK_APP=src/app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app/src

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50051

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:50051", "src.app:app"]
