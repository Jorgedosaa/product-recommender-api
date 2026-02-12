# AI-Powered Product Recommender API 🚀

**A High-Performance Semantic Search Engine & Recommendation System**

A professional-grade API built with **Django REST Framework** and **PostgreSQL (pgvector)** that leverages Machine Learning to understand user intent beyond simple keyword matching.

---

## 🌟 Key Features

- **🧠 Semantic Vector Search**: Utilizes `sentence-transformers` to convert natural language queries into vector embeddings, enabling the system to "understand" context (e.g., finding "ergonomic seating" when searching for "office chair").
- **⚡ CPU-Optimized ML Inference**: The AI pipeline is strictly optimized for CPU environments using the `all-MiniLM-L6-v2` model, ensuring low latency without requiring expensive GPUs.
- **🎯 Smart Match Quality**: Implements a **Quality Filter** (threshold `0.7`) to programmatically distinguish between high-confidence exact matches and "closest alternative" suggestions.
- **🔍 Real-Time Recommendations**: Calculates **Cosine Distance** directly within the database layer for efficient similarity ranking.

## 🏗️ Technical Architecture

| Component | Technology |
|-----------|------------|
| **Backend** | Django REST Framework (Python 3.10) |
| **Database** | PostgreSQL + `pgvector` extension |
| **AI/ML** | HuggingFace Transformers, PyTorch (CPU build) |
| **Infrastructure** | Docker & Docker Compose |
| **Frontend** | Vanilla JS + Tailwind CSS |

## ⚙️ How It Works

1. **Vector Embeddings**: When a product is imported, its description is passed through a Transformer model to generate a 384-dimensional vector representation.
2. **Semantic Querying**: When a user searches, their text input is converted into a vector in real-time.
3. **Cosine Similarity**: The database calculates the angular distance between the query vector and stored product vectors.
   - **Closer to 0**: Higher similarity.
   - **Closer to 1**: Lower similarity.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed.

### 1. Clone & Build
```bash
git clone https://github.com/Jorgedosaa/product-recommender-api.git
cd product-recommender-api
docker compose up -d --build
```

### 2. Initialize Database & Data
Run the custom management commands to populate the database and generate vector embeddings:

```bash
# Apply database migrations
docker compose exec api python manage.py migrate

# Import sample dataset (Amazon Products)
docker compose exec api python manage.py import_amazon_data

# Generate vector embeddings for semantic search
docker compose exec api python manage.py generate_embeddings
```

### 3. Access the Application
- **Frontend UI**: Open `http://localhost:8000` in your browser.
- **API Endpoint**: `http://localhost:8000/products/search/?q=laptop`

## 💡 Technical Challenges Solved

### 1. CPU-Only Inference Optimization
Deploying ML models often requires heavy GPU resources. I optimized the build process by explicitly targeting the CPU-only wheels for PyTorch (`--extra-index-url https://download.pytorch.org/whl/cpu`), significantly reducing the Docker image size and runtime resource consumption.

### 2. Handling Non-Exact Matches
A common issue in vector search is returning results even when they are irrelevant. I implemented a **dynamic thresholding logic** in the view layer:
- Calculates distance scores.
- Flags results as `is_high_confidence` if the distance is `< 0.7`.
- Allows the frontend to warn users if results are merely "best guesses" rather than exact matches.

### 3. CORS & Frontend Integration
To enable a seamless decoupled architecture between the static frontend and the API, I configured `django-cors-headers` to handle Cross-Origin Resource Sharing securely, allowing the Vanilla JS client to consume the API directly.



## 🛠️ Quick Start (Server Setup)

1. **Clone and Run:**
   ```bash
   git clone [https://github.com/Jorgedosaa/product-recommender-api.git](https://github.com/Jorgedosaa/product-recommender-api.git)
   cd product-recommender-api
   docker compose up -d --build