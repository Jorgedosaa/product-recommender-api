from django.urls import path

from .views import (
    ProductListCreateView,
    ProductRecommendationView,
    ProductSemanticSearchView,
)

urlpatterns = [
    path("", ProductListCreateView.as_view(), name="product-list"),
    path(
        "<int:pk>/similar/",
        ProductRecommendationView.as_view(),
        name="product-recommendations",
    ),
    path(
        "search/", ProductSemanticSearchView.as_view(), name="product-semantic-search"
    ),
]
