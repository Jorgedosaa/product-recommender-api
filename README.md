# 🛒 AI Product Recommender API

![Build Status](https://github.com/Jorgedosaa/product-recommender-api/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-5.0-green)
![Postgres](https://img.shields.io/badge/postgres-pgvector-blue)
![Deployment](https://img.shields.io/badge/deploy-railway-purple)
![License](https://img.shields.io/badge/license-MIT-blue)

A production-ready REST API built with Django and Django REST Framework that provides intelligent product recommendations using **Vector Similarity Search (pgvector)** and **Semantic Search (Sentence Transformers)**.

Live Demo: [https://product-recommender-api-production.up.railway.app/products/search/?q=laptop](https://product-recommender-api-production.up.railway.app/products/search/?q=laptop)

---

## 🚀 Features

- **🧠 Vector Similarity Search:** Uses `pgvector` to find products based on semantic meaning, not just keywords.
- **🔍 Semantic Search:** Natural language processing allows users to search "ergonomic device for coding" and find keyboards/mice.
- **⚡ Performance:** Asynchronous embedding generation using **Celery** and **Redis**.
- **🐳 Dockerized:** Fully containerized setup for consistent development and production environments.
- **☁️ Cloud Native:** Deployed on Railway with a microservices architecture (API + Worker + Redis + Postgres).

---

## 🏗 Architecture

The system is built as a set of microservices orchestrated via Docker Compose (Locally) and Railway (Production):

1.  **API Service (Django + Gunicorn):** Handles HTTP requests and business logic.
2.  **Database (PostgreSQL + pgvector):** Stores product data and high-dimensional vectors (384d).
3.  **Queue (Redis):** Manages background tasks.
4.  **Worker (Celery):** Processes embedding generation asynchronously to keep the API fast.



---

## 🛠 Tech Stack

- **Backend:** Python 3.12, Django 5, Django REST Framework
- **Database:** PostgreSQL 16 (using `ankane/pgvector` image)
- **AI/ML:** sentence-transformers (`all-MiniLM-L6-v2`)
- **Infrastructure:** Docker, Docker Compose, Gunicorn, Whitenoise
- **CI/CD:** GitHub Actions

---

## 📦 Local Installation (Docker)

The easiest way to run the project is using Docker.

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Jorgedosaa/product-recommender-api.git](https://github.com/Jorgedosaa/product-recommender-api.git)
    cd product-recommender-api
    ```

2.  **Create .env file**
    ```bash
    cp .env.example .env
    ```

3.  **Build and Run**
    ```bash
    docker-compose up --build
    ```

4.  **Access the API**
    - Search: `http://localhost:8000/products/search/?q=headphones`
    - Admin: `http://localhost:8000/admin/`

---

## ☁️ Deployment (Railway)

This project is deployed on **Railway**.

### Key Configuration Steps:
1.  **Database:** Must use the `ankane/pgvector` image instead of the standard Postgres image to support vector operations.
2.  **Start Command:**
    ```bash
    gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
    ```
3.  **Data Seeding (ETL):**
    Data was injected into the production database using a custom management command:
    ```bash
    python manage.py import_amazon_data
    ```

---

## 🧪 Testing

Run the comprehensive test suite. Si corres las pruebas localmente fuera de Docker, asegúrate de tener Redis disponible o activar el modo síncrono de Celery:

```bash
# Usando Docker 
docker-compose exec api python manage.py test products

# Localmente (Host)
DB_HOST=localhost CELERY_TASK_ALWAYS_EAGER=True python manage.py test products