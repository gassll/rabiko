from django.urls import path
from . import views

urlpatterns = [
    # главная
    path('', views.home, name='home'),

    # каталог
    path('catalog/', views.catalog_view, name='catalog_view'),

    # товар
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # ℹabout
    path('about/', views.about_view, name='about'),

    # профиль
    path('profile/', views.profile, name='profile'),
    path('profile/favorites/', views.profile_favorites, name='profile_favorites'),
    path('profile/orders/', views.profile_orders, name='profile_orders'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),

    # избранное
    path("favorites/", views.favorites_view, name="favorites"),
]
