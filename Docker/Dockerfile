FROM python:3.11-slim

RUN apt-get update && apt-get install -y sqlite3 nodejs && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4413

# --reload allows auto-reloading when you change Python files in dev.
CMD ["gunicorn", "-k", "gevent", "--worker-connections", "1000", "--bind", "0.0.0.0:4413", "--reload", "app:app"]ROM python:3.11-slim
RUN apt-get update && apt-get install -y sqlite3 nodejs && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4413

CMD ["gunicorn", "-k", "gevent", "--worker-connections", "1000", "--bind", "0.0.0.0:4413", "--reload", "app:app"]
