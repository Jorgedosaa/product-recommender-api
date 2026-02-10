from rest_framework import generics
from rest_framework.response import Response
from pgvector.django import CosineDistance
from sentence_transformers import SentenceTransformer
from .models import Product
from .serializers import ProductSerializer

# Initialize model outside the view for better performance (cached in memory)
# Using CPU-only as per requirements
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

class ProductSemanticSearchView(generics.ListAPIView):
    """
    Search products using natural language queries.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if not query:
            return Product.objects.none()

        # Phase 4: Convert user text query into a vector embedding
        query_embedding = model.encode(query).tolist()

        # Perform similarity search against all products
        return Product.objects.annotate(
            distance=CosineDistance('embedding', query_embedding)
        ).order_by('distance')[:5]