FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TRANSLATION_SERVICE_PORT=50051

CMD ["python", "translation_service.py"]
