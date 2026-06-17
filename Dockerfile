FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir bottle

COPY models/ ./models/
COPY controllers/ ./controllers/
COPY views/ ./views/
COPY static/ ./static/
COPY route.py .

RUN mkdir -p data

EXPOSE 8080

CMD ["python", "route.py"]

