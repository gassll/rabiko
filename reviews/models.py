from django.db import models


class Review(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()

    rating = models.PositiveSmallIntegerField(
        default=5,
        choices=[(i, str(i)) for i in range(1, 6)]
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликован"
    )
    show_on_homepage = models.BooleanField(
        default=False,
        verbose_name="Показывать на главной"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rating})"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
