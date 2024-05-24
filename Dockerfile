FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/.env

EXPOSE 80

ENV NAME OPENAI-SUITE

CMD ["python", "app.py"]
