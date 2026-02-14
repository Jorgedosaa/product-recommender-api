from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from .tasks import generate_product_embedding

@receiver(post_save, sender=Product)
def trigger_embedding_generation(sender, instance, created, **kwargs):
    """
    Automatically triggers the Celery task when a new product is created
    or when an existing product is saved without an embedding.
    """
    if created or instance.embedding is None:
        # .delay() sends the task to the Redis queue asynchronously
        generate_product_embedding.delay(instance.id)