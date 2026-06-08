from django.db import models


class Review(models.Model):
    name = models.CharField(max_length=100)

    text = models.TextField()

    rating = models.PositiveSmallIntegerField(
        default=5
    )

    is_published = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
