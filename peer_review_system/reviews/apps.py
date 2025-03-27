from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)  # Logging setup for debugging

class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'

    def ready(self):
        try:
            import reviews.signals  # Ensure that signals are imported
            logger.info("✅ Signals module successfully loaded.")
        except ImportError as e:
            logger.error(f"❌ Error loading signals module: {e}")
