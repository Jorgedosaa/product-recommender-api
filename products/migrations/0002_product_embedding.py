# app/products/migrations/0002_product_embedding.py
import pgvector.django.vector
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "products",
            "0003_enable_pgvector",
        ),  # Depende de la activación de la extensión
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="embedding",
            field=pgvector.django.vector.VectorField(
                blank=True, dimensions=384, null=True
            ),
        ),
    ]
