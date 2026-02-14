# Changelog

All notable changes to this project will be documented in this file.

## [1.3.0] - 2023-10-27
### Added
- Comprehensive Test Suite (`products/tests.py`) covering CRUD and AI endpoints.
- GitHub Actions workflow for automated testing.
- Detailed `README.md`, `API_DOCS.md`, and `ROADMAP.md`.
- `ProductDetailView` for Retrieve, Update, and Delete operations.
- Improved Recommendation Algorithm: Now filters by Category and Price range before vector search.

## [1.2.0] - 2023-10-15
### Added
- `ProductRecommendationView` using Cosine Distance.
- `ProductSemanticSearchView` for natural language queries.
- `pgvector` integration.