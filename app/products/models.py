from django.db import models
# Importación necesaria para manejar vectores en PostgreSQL
from pgvector.django import VectorField

class Product(models.Model):
    asin = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255, blank=True)
    brand = models.CharField(max_length=255, blank=True)
    price = models.FloatField(null=True, blank=True)

    # Ahora Django reconocerá VectorField
    embedding = VectorField(dimensions=384, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title