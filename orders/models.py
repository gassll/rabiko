from django.conf import settings
from django.db import models

from catalog.models import ProductVariant


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Оформлен'),
        ('processing', 'Собирается'),
        ('delivery', 'В пути'),
        ('done', 'Доставлен'),
        ('cancelled', 'Отменён'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


class DeliveryAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=50)
    apartment = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
