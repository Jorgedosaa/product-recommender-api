from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from pgvector.django import CosineDistance
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRecommendationView(generics.ListAPIView):
    """
    API View to retrieve similar products based on vector embeddings.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('pk')
        # Fetch the reference product
        target_product = get_object_or_404(Product, pk=product_id)
        
        # Ensure the product has an embedding before calculating distance
        if target_product.embedding is None:
            return Product.objects.none()

        # Query similar products excluding the target itself
        # Using the <=> operator via CosineDistance
        return Product.objects.exclude(id=product_id).annotate(
            distance=CosineDistance('embedding', target_product.embedding)
        ).order_by('distance')[:5]

