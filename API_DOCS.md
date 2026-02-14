# API Documentation

## Base URL
`http://localhost:8000/api/products/`

## Error Handling
Standard HTTP status codes are used:
- `200 OK`: Request succeeded.
- `201 Created`: Resource created successfully.
- `204 No Content`: Resource deleted successfully.
- `400 Bad Request`: Invalid input data.
- `404 Not Found`: Resource does not exist.

---

## Endpoints

### 1. List Products
- **URL**: `/`
- **Method**: `GET`
- **Response**: Array of product objects.

### 2. Create Product
- **URL**: `/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "asin": "B08X",
    "title": "Wireless Headphones",
    "description": "Noise cancelling...",
    "category": "Electronics",
    "price": 199.99
  }
  ```

### 3. Get Product Detail
- **URL**: `/{id}/`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "id": 1,
    "asin": "B08X",
    "title": "Wireless Headphones",
    "description": "Noise cancelling...",
    "category": "Electronics",
    "brand": "Sony",
    "price": 199.99,
    "created_at": "2023-10-27T10:00:00Z"
  }
  ```
  *Note: The `embedding` field is excluded from responses for performance.*

### 4. Update Product
- **URL**: `/{id}/`
- **Method**: `PATCH`
- **Body**: (Partial fields allowed)
  ```json
  {
    "price": 179.99
  }
  ```

### 5. Delete Product
- **URL**: `/{id}/`
- **Method**: `DELETE`
- **Response**: `204 No Content`

### 6. Get Recommendations
- **URL**: `/{id}/recommendations/`
- **Method**: `GET`
- **Description**: Returns a list of up to 5 products similar to the target ID.
- **Logic**:
  - Filters by same **Category**.
  - Filters by **Price** (within 50% range).
  - Sorts by **Vector Similarity** (Cosine Distance).

### 7. Semantic Search
- **URL**: `/search/?q=query_string`
- **Method**: `GET`
- **Query Params**: `q` (string) - The natural language search query.
- **Response**:
  ```json
  {
    "has_exact_matches": true,
    "results": [
      {
        "id": 5,
        "title": "Bluetooth Earbuds",
        ...
      }
    ]
  }
  ```

## Data Model

| Field | Type | Description |
|-------|------|-------------|
| `asin` | String | Unique Product Identifier |
| `title` | String | Product Name |
| `category` | String | Product Category (used for filtering) |
| `price` | Float | Price in USD |
| `embedding` | Vector(384) | AI-generated vector representation |