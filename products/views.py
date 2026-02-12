import logging
from typing import List
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from pgvector.django import CosineDistance
from rest_framework import generics
from rest_framework.request import Request
from sentence_transformers import SentenceTransformer

from .models import Product
from .serializers import ProductSerializer

# Set up logging for easier debugging in the server
logger = logging.getLogger(__name__)

# Initialize model outside the view for better performance (cached in memory)
# Using CPU device explicitly as per requirements optimization
try:
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    logger.info("SentenceTransformer model loaded successfully on CPU.")
except Exception as e:
    logger.error(f"Error loading SentenceTransformer: {e}")

class ProductListCreateView(generics.ListCreateAPIView):
    """
    Standard view to list all products or create new ones.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRecommendationView(generics.ListAPIView):
    """
    Phase 3 & 4: Provides product recommendations based on a specific product ID.
    Uses Cosine Distance for vector similarity search.
    """
    serializer_class = ProductSerializer

    def get_queryset(self) -> QuerySet:
        product_id = self.kwargs.get("pk")
        target_product = get_object_or_404(Product, pk=product_id)

        # Safety check: Ensure the product has an embedding processed
        if target_product.embedding is None:
            logger.warning(f"Product ID {product_id} has no embedding.")
            return Product.objects.none()

        # Search for similar items excluding the reference product itself
        # Annotate with distance to allow frontend to display similarity score if needed
        return (
            Product.objects.exclude(id=product_id)
            .annotate(distance=CosineDistance("embedding", target_product.embedding))
            .order_by("distance")[:5]
        )


class ProductSemanticSearchView(generics.ListAPIView):
    """
    Phase 4: Enables natural language search using vector embeddings.
    Converts search queries into vectors in real-time.
    """
    serializer_class = ProductSerializer

    def get_queryset(self) -> QuerySet:
        query = self.request.query_params.get("q", None)
        if not query:
            return Product.objects.none()

        try:
            # Convert text query into a vector (list)
            query_embedding = model.encode(query).tolist()

            # Return top 5 matches based on semantic similarity
            return Product.objects.annotate(
                distance=CosineDistance("embedding", query_embedding)
            ).order_by("distance")[:5]
        except Exception as e:
            logger.error(f"Search error: {e}")
            return Product.objects.none()