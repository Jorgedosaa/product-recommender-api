from django.urls import path

from .views import (
    ProductListCreateView,
    ProductDetailView,
    ProductRecommendationView,
    ProductSemanticSearchView,
)

# Using descriptive app_name for reverse URL lookups in your portfolio
app_name = "products"

urlpatterns = [
    # Basic CRUD: List all products or create one
    path("", ProductListCreateView.as_view(), name="product_list"),
    
    # Basic CRUD: Retrieve, Update, Delete specific product
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),

    # Phase 3 & 4: Recommendations based on Vector Similarity (Cosine Distance)
    path(
        "<int:pk>/recommendations/",
        ProductRecommendationView.as_view(),
        name="product_recommendations",
    ),
    
    # Phase 4: Semantic Search using Natural Language Processing
    path(
        "search/", 
        ProductSemanticSearchView.as_view(), 
        name="product_semantic_search"
    ),
]