from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from orders.models import Order
from catalog.models import Favorite

from .forms import LoginForm, ProfileUpdateForm
from users.forms import RegisterForm
from django.contrib import messages

User = get_user_model()


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(form.cleaned_data["password1"])
            user.save()

            login(request, user)
            messages.success(request, "Регистрация успешна")
            return redirect("profile")

        print(form.errors)

    return render(request, "registration/register.html", {"form": form})

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:
                login(request, user)

                favorite_id = request.GET.get("favorite")

                if favorite_id:
                    from catalog.models import Product, Favorite

                    product = Product.objects.get(id=favorite_id)

                    Favorite.objects.get_or_create(
                        user=user,
                        product=product
                    )

                next_url = request.POST.get("next")

                if next_url:
                    return redirect(next_url)

                return redirect("profile")

            form.add_error(None, "Неверный логин или пароль")

    return render(
        request,
        "registration/login.html",
        {"form": form}
    )

def logout_view(request):
    logout(request)
    return redirect("login")


# PROFILE OVERVIEW
@login_required
def profile_view(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    favorites_count = Favorite.objects.filter(
        user=request.user
    ).count()

    cart_count = len(
        request.session.get("cart", {})
    )

    return render(
        request,
        "profile/profile.html",
        {
            "orders_count": orders.count(),
            "favorites_count": favorites_count,
            "cart_count": cart_count,
            "last_orders": orders[:5],
        }
    )

@login_required
def profile_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "profile/profile_orders.html",
        {
            "orders": orders
        }
    )


@login_required
def profile_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)

    return render(request, "profile/profile_favorites.html", {
        "favorites": favorites
    })

@login_required
def profile_edit(request):
    if request.method == "POST":

        form = ProfileUpdateForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Профиль успешно обновлен"
            )

            return redirect("profile_edit")

    else:

        form = ProfileUpdateForm(
            instance=request.user
        )

    return render(
        request,
        "profile/profile_edit.html",
        {
            "form": form
        }
    )


@login_required
def profile_password(request):
    user = request.user

    form = PasswordChangeForm(user)

    form.fields["old_password"].label = "Текущий пароль"
    form.fields["new_password1"].label = "Новый пароль"
    form.fields["new_password2"].label = "Подтвердите новый пароль"

    if request.method == "POST":
        form = PasswordChangeForm(user, request.POST)

        form.fields["old_password"].label = "Текущий пароль"
        form.fields["new_password1"].label = "Новый пароль"
        form.fields["new_password2"].label = "Подтвердите новый пароль"

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            messages.success(
                request,
                "Пароль успешно изменён"
            )

            return redirect("profile_password")

    return render(
        request,
        "profile/profile_password.html",
        {"form": form}
    )
