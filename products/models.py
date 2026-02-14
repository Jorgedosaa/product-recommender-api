from django.db import models

# Import necessary to handle vectors in PostgreSQL
from pgvector.django import HnswIndex, VectorField


class Product(models.Model):
    asin = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255, blank=True)
    brand = models.CharField(max_length=255, blank=True)
    price = models.FloatField(null=True, blank=True)

    # Now Django will recognize VectorField
    embedding = VectorField(dimensions=384, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        # Add HNSW index for faster vector similarity search
        indexes = [
            HnswIndex(
                name="product_embedding_hnsw_idx",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]
