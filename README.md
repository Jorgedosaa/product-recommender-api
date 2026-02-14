# 🛒 Product Recommender API

![Build Status](https://github.com/Jorgedosaa/product-recommender-api/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-5.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

A production-ready REST API built with Django and Django REST Framework that provides intelligent product recommendations using **Vector Similarity Search (pgvector)** and **Semantic Search (Sentence Transformers)**.

---

## 🚀 Features

- **Full CRUD Operations**  
  Manage products with standard RESTful endpoints.

- **AI-Powered Recommendations**  
  Finds similar products based on vector embeddings using Cosine Similarity.

- **Semantic Search**  
  Search for products using natural language queries, not just keyword matching.

- **Hybrid Filtering**  
  Recommendations refined by category and price range for better relevance.

- **Performance Optimized**  
  Efficient database queries and vector indexing.

- **CI/CD Pipeline**  
  ![Tests](https://github.com/Jorgedosaa/product-recommender-api/actions/workflows/tests.yml/badge.svg)

---

## 🛠 Tech Stack

- **Backend:** Python 3.12, Django 5, Django REST Framework  
- **Database:** PostgreSQL + pgvector extension  
- **AI/ML:** sentence-transformers (`all-MiniLM-L6-v2`)  
- **Testing:** Pytest / Django APITestCase  

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Jorgedosaa/product-recommender-api.git
cd product-recommender-api
