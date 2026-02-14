# Project Roadmap

## Phase 1: Core API (Completed)
- [x] Basic CRUD operations
- [x] PostgreSQL + pgvector integration
- [x] Initial documentation

## Phase 2: Intelligence (Completed)
- [x] Vector embedding generation
- [x] Semantic search endpoint
- [x] Recommendation endpoint with hybrid filtering (Category + Price)

## Phase 3: Robustness (Current)
- [x] Comprehensive Test Suite
- [x] CI/CD Workflow (GitHub Actions)
- [x] Detailed API Documentation

## Phase 4: Future Improvements
- [x] **Dockerization**: Create Dockerfile and docker-compose for easy deployment.
- [ ] **Async Tasks**: Move embedding generation to Celery tasks to improve write performance.
- [ ] **Pagination**: Add standard DRF pagination to list and search endpoints.
- [ ] **Authentication**: Add JWT authentication for secure access.
- [ ] **Frontend**: Build a React/Next.js dashboard to visualize recommendations.
- [ ] **Advanced ML**: Fine-tune the SentenceTransformer model on specific product data.