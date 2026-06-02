from django.urls import path
from .views import checkout, order_list, order_detail

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("", order_list, name="order_list"),
    path("<int:pk>/", order_detail, name="order_detail"),
]