import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Seed database with Amazon product data from JSON file'

    def handle(self, *args, **options):
        # Construimos la ruta dinámica al archivo JSON
        json_path = os.path.join(settings.BASE_DIR, 'products', 'data', 'products_data.json')
        
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"Archivo no encontrado en: {json_path}"))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.stdout.write(f"Cargando {len(data)} productos desde el JSON...")
        
        created_count = 0
        for item in data:
            # Usamos get_or_create para evitar duplicados por ASIN
            obj, created = Product.objects.get_or_create(
                asin=item['asin'],
                defaults={
                    'title': item.get('title'),
                    'description': item.get('description'),
                    'category': item.get('category', ''),
                    'brand': item.get('brand', ''),
                    'price': item.get('price')
                }
            )
            if created:
                self.stdout.write(f"Creado: {item['title']}")
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"Proceso terminado. {created_count} productos nuevos añadidos."))