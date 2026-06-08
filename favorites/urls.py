from django.urls import path
from .views import favorites_list, toggle_favorite

urlpatterns = [
    path("", favorites_list, name="favorites"),

    path(
        "toggle/<int:product_id>/",
        toggle_favorite,
        name="toggle_favorite"
    ),
]