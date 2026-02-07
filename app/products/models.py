from django.db import models

from django.db import models

class Product(models.Model):
    asin = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255, blank=True)
    brand = models.CharField(max_length=255, blank=True)
    price = models.FloatField(null=True, blank=True)

    # Embedding se añadirá en Fase 2
    # embedding = VectorField(dimensions=384)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

