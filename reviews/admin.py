from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "rating",
        "is_published",
        "show_on_homepage",
        "created_at"
    )

    list_filter = (
        "rating",
        "is_published",
        "show_on_homepage"
    )

    list_editable = (
        "is_published",
        "show_on_homepage",
    )