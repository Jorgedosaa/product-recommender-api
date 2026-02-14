FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a non-root user for security
RUN useradd -m -r django && \
    chown -R django /app

USER django

EXPOSE 8000

# Use Gunicorn for production instead of runserver
# Ensure 'gunicorn' is in your requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "product_recommender_api.wsgi:application"]
