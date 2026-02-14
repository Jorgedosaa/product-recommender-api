# Product Recommender API

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-5.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

A production-ready REST API built with Django and Django REST Framework that provides intelligent product recommendations using Vector Similarity Search (pgvector) and Semantic Search (Sentence Transformers).

## 🚀 Features

- **Full CRUD Operations**: Manage products with standard RESTful endpoints.
- **AI-Powered Recommendations**: Finds similar products based on vector embeddings (Cosine Similarity).
- **Semantic Search**: Search for products using natural language queries, not just keyword matching.
- **Hybrid Filtering**: Recommendations are refined by category and price range for better relevance.
- **Performance**: Optimized database queries and vector indexing.

## 🛠 Tech Stack

- **Backend**: Python 3.12, Django 5, Django REST Framework
- **Database**: PostgreSQL with `pgvector` extension
- **AI/ML**: `sentence-transformers` (all-MiniLM-L6-v2)
- **Testing**: Pytest / Django APITestCase

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/product-recommender-api.git
   cd product-recommender-api
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   Ensure you have PostgreSQL installed and the `pgvector` extension enabled.
   ```sql
   CREATE EXTENSION vector;
   ```
   Then run migrations:
   ```bash
   python manage.py migrate
   ```

5. **Run the server**
   ```bash
   python manage.py runserver
   ```

## 🧪 Running Tests

This project uses a comprehensive test suite covering CRUD, edge cases, and AI logic.

```bash
python manage.py test products
```

## 📡 API Endpoints

For detailed documentation, including request/response examples, see [API_DOCS.md](API_DOCS.md).

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| POST | `/api/products/` | Create a new product |
| GET | `/api/products/{id}/` | Retrieve product details |
| PATCH | `/api/products/{id}/` | Update a product |
| DELETE | `/api/products/{id}/` | Delete a product |
| GET | `/api/products/{id}/recommendations/` | Get AI-based recommendations |
| GET | `/api/products/search/?q={query}` | Semantic search |

## 🧠 Recommendation Algorithm

The recommendation engine uses a hybrid approach:
1. **Filtering**: Candidates are filtered by the target product's **Category** and a **Price Range** (+/- 50%).
2. **Vector Search**: Calculates Cosine Distance between the target product's embedding and candidates.
3. **Ranking**: Returns the top 5 closest matches.

## 📂 Project Structure

The project follows a standard Django app structure, with logic separated into `serializers`, `views`, and `models`. Tests are located in `products/tests.py`.