import json
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Seed database with sample Amazon product data'

    def handle(self, *args, **options):
        # Sample data for testing Phase 2 and 3
        sample_data = [
            {
                "asin": "B07ZPKN6LQ",
                "title": "Apple AirPods Pro",
                "description": "Active noise cancellation, transparency mode, and spatial audio.",
                "category": "Electronics",
                "brand": "Apple",
                "price": 249.00
            },
            {
                "asin": "B081FGTPDQ",
                "title": "Sony WH-1000XM4",
                "description": "Industry leading noise canceling with Dual Noise Sensor technology.",
                "category": "Electronics",
                "brand": "Sony",
                "price": 348.00
            },
            {
                "asin": "B09V7S1D97",
                "title": "Logitech MX Master 3S",
                "description": "Ergonomic wireless mouse with ultra-fast scrolling and 8K DPI.",
                "category": "Computers",
                "brand": "Logitech",
                "price": 99.00
            }
        ]

        self.stdout.write("Seeding products into database...")
        
        created_count = 0
        for item in sample_data:
            obj, created = Product.objects.get_or_create(
                asin=item['asin'],
                defaults=item
            )
            if created:
                self.stdout.write(f"Successfully created: {item['title']}")
                created_count += 1
            else:
                self.stdout.write(self.style.WARNING(f"Product {item['asin']} already exists. Skipping..."))
        
        self.stdout.write(self.style.SUCCESS(f"Seed process finished. {created_count} new products added."))