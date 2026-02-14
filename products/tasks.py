import logging
from celery import shared_task
from .models import Product
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# Global model loading for memory optimization.
# This ensures the model is loaded only once when the worker starts.
try:
    logger.info("Loading SentenceTransformer model into Worker memory...")
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load AI model: {e}")
    model = None

@shared_task
def generate_product_embedding(product_id):
    """
    Async task to generate vector embeddings for a given product.
    This runs in the background worker, not the main API thread.
    """
    if model is None:
        logger.error("Model is not loaded. Cannot generate embedding.")
        return

    try:
        # Fetch the product from the database
        product = Product.objects.get(id=product_id)
        
        logger.info(f"Generating embedding for Product ID: {product_id} ({product.title})")
        
        # AI Logic: Combine title and description
        text_data = f"{product.title} {product.description}"
        
        # Generate vector
        embedding_vector = model.encode(text_data)
        
        # Update database
        product.embedding = embedding_vector.tolist()
        product.save(update_fields=['embedding'])
        
        logger.info(f"Successfully saved embedding for Product ID: {product_id}")
        
    except Product.DoesNotExist:
        logger.warning(f"Product ID {product_id} not found. Task skipped.")
    except Exception as e:
        logger.error(f"Error processing Product ID {product_id}: {e}")