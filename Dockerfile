FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . .

CMD gunicorn veritas_web_app:app --bind 0.0.0.0:$PORT

