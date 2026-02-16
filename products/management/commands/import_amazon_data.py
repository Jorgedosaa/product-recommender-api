import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer

from products.models import Product


class Command(BaseCommand):
    help = "Seed database with Amazon product data from JSON file"

    def handle(self, *args, **options):
        # Construimos la ruta dinámica al archivo JSON
        json_path = os.path.join(
            settings.BASE_DIR, "products", "data", "products_data.json"
        )

        if not os.path.exists(json_path):
            self.stdout.write(
                self.style.ERROR(f"Archivo no encontrado en: {json_path}")
            )
            return

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.stdout.write("Cargando modelo de embeddings (all-MiniLM-L6-v2)...")
        # Cargamos el modelo una sola vez antes del bucle
        model = SentenceTransformer("all-MiniLM-L6-v2")

        self.stdout.write(f"Cargando {len(data)} productos desde el JSON...")

        created_count = 0
        for item in data:
            # Generamos el texto para el embedding (título + descripción)
            text_to_embed = f"{item.get('title') or ''} {item.get('description') or ''}"
            embedding = model.encode(text_to_embed).tolist()

            # Usamos get_or_create para evitar duplicados por ASIN
            obj, created = Product.objects.get_or_create(
                asin=item["asin"],
                defaults={
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "category": item.get("category", ""),
                    "brand": item.get("brand", ""),
                    "price": item.get("price"),
                    "embedding": embedding,
                },
            )
            if created:
                self.stdout.write(f"Creado: {item['title']}")
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Proceso terminado. {created_count} productos nuevos añadidos."
            )
        )
