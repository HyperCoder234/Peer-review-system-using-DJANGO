from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review, Assignment
import logging
import os

logger = logging.getLogger(__name__)  # Logging setup

# ✅ Review save hone par log likhna
@receiver(post_save, sender=Review)
def review_saved(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New review added by {instance.reviewer} for {instance.reviewee}")
    else:
        logger.info(f"Review updated by {instance.reviewer} for {instance.reviewee}")

# ✅ Review delete hone par log aur related files delete karna
@receiver(post_delete, sender=Review)
def review_deleted(sender, instance, **kwargs):
    logger.warning(f"Review by {instance.reviewer} for {instance.reviewee} deleted.")

# ✅ Assignment save hone par log likhna
@receiver(post_save, sender=Assignment)
def assignment_saved(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New assignment '{instance.title}' uploaded.")
    else:
        logger.info(f"Assignment '{instance.title}' updated.")

# ✅ Assignment delete hone par log likhna aur file delete karna
@receiver(post_delete, sender=Assignment)
def assignment_deleted(sender, instance, **kwargs):
    logger.warning(f"Assignment '{instance.title}' deleted.")
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)  # File delete karna
            logger.info(f"Deleted file: {instance.file.path}")
