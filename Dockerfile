FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y nginx sqlite3 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 4413


# Start Nginx and Flask (using --debug for auto-reload)
CMD nginx && python app.py --debug
