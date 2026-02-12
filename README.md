# AI-Powered Product Recommender API 🚀

A high-performance **Semantic Search Engine** and **Recommendation System** built with Django, PostgreSQL, and Machine Learning.

## 🌟 Key Features
- **Semantic Vector Search:** Uses `sentence-transformers` to understand user intent beyond keywords.
- **Smart Recommendations:** Real-time product similarity using **Cosine Distance** on a `pgvector` database.
- **CPU-Optimized Deployment:** Specifically tailored for low-resource environments (optimized Docker builds).
- **Modern Web Interface:** A responsive client-side dashboard built with **Tailwind CSS**.

## 🏗️ Technical Architecture
- **Backend:** Django Rest Framework (DRF)
- **Vector Database:** PostgreSQL + `pgvector`
- **NLP Model:** `all-MiniLM-L6-v2` (Running on CPU)
- **Containerization:** Docker & Docker Compose
- **Frontend:** HTML5, JavaScript (Fetch API), Tailwind CSS


## 🛠️ Quick Start (Server Setup)

1. **Clone and Run:**
   ```bash
   git clone [https://github.com/Jorgedosaa/product-recommender-api.git](https://github.com/Jorgedosaa/product-recommender-api.git)
   cd product-recommender-api
   docker compose up -d --build