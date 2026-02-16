# 📚 API Documentation

## Base URLs

| Environment | URL |
| :--- | :--- |
| **Production (Live)** | `https://product-recommender-api-production.up.railway.app/products/` |
| **Local Development** | `http://localhost:8000/products/` |

---

## 🔐 Authentication
- **Read Operations (GET):** Publicly accessible (Search, Recommendations, List).
- **Write Operations (POST, PATCH, DELETE):** Require valid authentication (or Admin access locally).

---

## 📡 Endpoints

### 1. 🔍 Semantic Search (AI Powered)
Searches for products using natural language queries. It converts the user's query into a vector and finds the nearest semantic matches in the database.

- **URL**: `/search/?q={query}`
- **Method**: `GET`
- **Query Params**:
  - `q` (string): The search term (e.g., "device for coding", "noise cancelling").
- **Response**:
  ```json
  {
    "count": 5,
    "has_exact_matches": false,
    "results": [
      {
        "id": 2,
        "title": "Keychron K2 Mechanical Keyboard",
        "category": "Electronics",
        "price": 99.0,
        "description": "Wireless mechanical keyboard...",
        "match_score": "High Confidence"
      }
    ]
  }