import torch
from django.core.management.base import BaseCommand
from products.models import Product
from sentence_transformers import SentenceTransformer


class Command(BaseCommand):
    help = "Generates vectors (embeddings) for products using SentenceTransformers"

    def handle(self, *args, **options):
        self.stdout.write("Starting Phase 2: Embedding Generation...")

        # Load the model (downloaded automatically the first time)
        # We use the lightweight MiniLM-L6 model (384 dimensions)
        self.stdout.write("Loading model all-MiniLM-L6-v2 on CPU...")
        model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

        # Find products that have text but are missing the vector
        products = Product.objects.filter(embedding__isnull=True)
        count = products.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("No new products to process."))
            return

        self.stdout.write(f"Processing {count} products...")

        for p in products:
            # Combine title and description for better semantic context
            text_data = f"{p.title} {p.description}"

            # Generate the embedding (numeric vector)
            embedding_vector = model.encode(text_data)

            # Save to the database (converted to list for pgvector)
            p.embedding = embedding_vector.tolist()
            p.save()

            self.stdout.write(f"✓ Vector generated for ASIN: {p.asin}")

        self.stdout.write(
            self.style.SUCCESS(f"Process finished! {count} embeddings created.")
        )
