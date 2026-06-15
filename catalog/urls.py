from django.urls import path
from . import views

urlpatterns = [
    # главная
    path('', views.home, name='home'),

    # каталог
    path("catalog/", views.catalog_view, name="catalog"),

    # товар
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # about
    path('about/', views.about_view, name='about'),

    # профиль
    path("reviews/", views.reviews_view, name="reviews"),
    path("cart/status/<int:variant_id>/", views.cart_status, name="cart_status"),

]
