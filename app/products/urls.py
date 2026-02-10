from django.urls import path
from .views import ProductListCreateView, ProductRecommendationView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list'),
    path('<int:pk>/similar/', ProductRecommendationView.as_view(), name='product-recommendations'),
]