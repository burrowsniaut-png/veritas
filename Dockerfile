FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN if [ -f templates.zip ]; then apt-get update && apt-get install -y unzip && unzip templates.zip && rm templates.zip; fi

EXPOSE 5000

CMD python veritas_web_app.py
