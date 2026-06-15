from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, ProductVariant, Size


@receiver(post_save, sender=Product)
def create_default_variant(sender, instance, created, **kwargs):
    if created:
        size = Size.objects.first()

        ProductVariant.objects.create(
            product=instance,
            size=size,
            stock=10
        )