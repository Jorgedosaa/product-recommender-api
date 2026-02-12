# app/products/migrations/0003_enable_pgvector.py
from django.db import migrations
from pgvector.django import VectorExtension


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [VectorExtension()]
