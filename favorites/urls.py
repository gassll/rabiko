from django.urls import path
from .views import favorites_list

urlpatterns = [
    path("", favorites_list, name="favorites"),
]