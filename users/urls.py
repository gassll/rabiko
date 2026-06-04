from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/password/", views.profile_password, name="profile_password"),
    path("profile/orders/", views.profile_orders, name="profile_orders"),
    path("profile/favorites/", views.profile_favorites, name="profile_favorites"),

    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

]
