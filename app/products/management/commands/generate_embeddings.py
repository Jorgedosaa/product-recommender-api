import torch
from django.core.management.base import BaseCommand
from products.models import Product
from sentence_transformers import SentenceTransformer

class Command(BaseCommand):
    help = 'Genera vectores (embeddings) para los productos usando SentenceTransformers'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando Fase 2: Generación de Embeddings...")
        
        # Cargamos el modelo (se descarga automáticamente la primera vez)
        # Usamos el modelo ligero MiniLM-L6 (384 dimensiones)
        self.stdout.write("Cargando modelo all-MiniLM-L6-v2 en CPU...")
        model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

        # Buscamos productos que tengan texto pero les falte el vector
        products = Product.objects.filter(embedding__isnull=True)
        count = products.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("No hay productos nuevos para procesar."))
            return

        self.stdout.write(f"Procesando {count} productos...")

        for p in products:
            # Combinamos título y descripción para mejor contexto semántico
            text_data = f"{p.title} {p.description}"
            
            # Generar el embedding (vector numérico)
            embedding_vector = model.encode(text_data)
            
            # Guardar en la base de datos (convertido a lista para pgvector)
            p.embedding = embedding_vector.tolist()
            p.save()
            
            self.stdout.write(f"✓ Vector generado para ASIN: {p.asin}")

        self.stdout.write(self.style.SUCCESS(f"¡Proceso terminado! {count} embeddings creados."))