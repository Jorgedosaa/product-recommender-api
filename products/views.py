import logging

from django.db.models import BooleanField, Case, QuerySet, Value, When
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from pgvector.django import CosineDistance
from rest_framework import filters, generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from sentence_transformers import SentenceTransformer

from .models import Product
from .serializers import ProductSerializer

# Set up logging for production-ready debugging
logger = logging.getLogger(__name__)

# Constants for AI Logic
SIMILARITY_THRESHOLD = 0.7  # Distances > 0.7 are considered low confidence

# Initialize model outside the view for better performance (cached in memory)
try:
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    logger.info("SentenceTransformer model loaded successfully on CPU.")
except Exception as e:
    logger.error(f"Error loading SentenceTransformer: {e}")


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductListCreateView(generics.ListCreateAPIView):
    """
    Standard view to list all products or create new ones.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    # Protect write operations, allow read-only for public
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Add standard filtering, searching, and ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category"]  # Enable ?category=Electronics
    search_fields = [
        "title",
        "description",
    ]  # Enable ?search=keyword (Standard DB search)
    ordering_fields = ["price", "created_at"]  # Enable ?ordering=price


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates or deletes a single product instance.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # Protect write operations, allow read-only for public
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductRecommendationView(generics.ListAPIView):
    """
    Phase 3 & 4: Provides product recommendations based on a specific product ID.
    Uses Cosine Distance for vector similarity search.
    """

    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]  # Public endpoint
    throttle_classes = [AnonRateThrottle, UserRateThrottle]  # Prevent abuse

    def get_queryset(self) -> QuerySet:
        product_id = self.kwargs.get("pk")
        target_product = get_object_or_404(Product, pk=product_id)

        if target_product.embedding is None:
            logger.warning(f"Product ID {product_id} has no embedding.")
            return Product.objects.none()

        # Start with all other products
        queryset = Product.objects.exclude(id=product_id)

        # 1. Filter by Category (if available) to ensure relevance
        if target_product.category:
            queryset = queryset.filter(category=target_product.category)

        # 2. Filter by Price Range (e.g., +/- 50%) to keep recommendations affordable/comparable
        if target_product.price is not None:
            min_price = target_product.price * 0.5
            max_price = target_product.price * 1.5
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset.annotate(
            distance=CosineDistance("embedding", target_product.embedding)
        ).order_by("distance")[:5]


class ProductSemanticSearchView(generics.ListAPIView):
    """
    Phase 4: Enables natural language search using vector embeddings.
    Includes a quality filter to identify high-confidence matches.
    """

    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]  # Public endpoint
    pagination_class = (
        StandardResultsSetPagination  # Enable pagination for search results
    )
    throttle_classes = [AnonRateThrottle, UserRateThrottle]  # Prevent abuse

    def get_queryset(self) -> QuerySet:
        query = self.request.query_params.get("q", None)
        if not query:
            # Return 400 if 'q' is missing, as it's required for this endpoint
            raise ValidationError({"q": "This query parameter is required."})

        try:
            # Convert text query into a vector in real-time
            query_embedding = model.encode(query).tolist()

            # Annotate each result with a boolean 'is_high_confidence'
            return (
                Product.objects.annotate(
                    distance=CosineDistance("embedding", query_embedding)
                )
                .annotate(
                    is_high_confidence=Case(
                        When(distance__lt=SIMILARITY_THRESHOLD, then=Value(True)),
                        default=Value(False),
                        output_field=BooleanField(),
                    )
                )
                .order_by("distance")
            )
        except Exception as e:
            logger.error(f"Search error: {e}")
            return Product.objects.none()

    def list(self, request, *args, **kwargs):
        """
        Custom response format to provide metadata about match quality.
        This allows the frontend to show "closest alternatives" warnings.
        """
        queryset = self.get_queryset()

        # Apply pagination to the semantic search results
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            # Determine if we have any high-confidence matches in the current page
            has_exact_matches = any(
                item.get("is_high_confidence", False) for item in serializer.data
            )

            # Return standard paginated response but inject our custom metadata
            response = self.get_paginated_response(serializer.data)
            response.data["has_exact_matches"] = has_exact_matches
            return response

        # Fallback if pagination is disabled
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
