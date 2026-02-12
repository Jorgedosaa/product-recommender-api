from django.shortcuts import get_object_or_404
from pgvector.django import CosineDistance
from rest_framework import generics
from sentence_transformers import SentenceTransformer

from .models import Product
from .serializers import ProductSerializer

# Initialize model outside the view for better performance (cached in memory)
# Using CPU-only as per requirements
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")


class ProductListCreateView(generics.ListCreateAPIView):
    """
    Standard view to list all products or create new ones.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRecommendationView(generics.ListAPIView):
    """
    Phase 3: Provides product recommendations based on a specific product ID.
    """

    serializer_class = ProductSerializer

    def get_queryset(self):
        product_id = self.kwargs.get("pk")
        target_product = get_object_or_404(Product, pk=product_id)

        # Ensure the product has an embedding processed
        if target_product.embedding is None:
            return Product.objects.none()

        # Search for similar items excluding the reference product itself
        return (
            Product.objects.exclude(id=product_id)
            .annotate(distance=CosineDistance("embedding", target_product.embedding))
            .order_by("distance")[:5]
        )


class ProductSemanticSearchView(generics.ListAPIView):
    """
    Phase 4: Enables natural language search using vector embeddings.
    """

    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q", None)
        if not query:
            return Product.objects.none()

        # Convert the text query into a vector in real-time
        query_embedding = model.encode(query).tolist()

        return Product.objects.annotate(
            distance=CosineDistance("embedding", query_embedding)
        ).order_by("distance")[:5]
