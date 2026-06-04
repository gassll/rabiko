from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import LoginForm, ProfileUpdateForm
from users.forms import RegisterForm
from django.contrib import messages

User = get_user_model()


# REGISTER
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            login(request, user)
            return redirect("profile")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


# LOGIN
def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("profile")

            form.add_error(None, "Неверный логин или пароль")

    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# PROFILE OVERVIEW
@login_required
def profile_view(request):
    return render(request, "profile/profile.html", {
        "orders_count": 0,
        "favorites_count": 0,
        "cart_count": 0,
        "last_orders": [],
    })


@login_required
def profile_orders(request):
    return render(request, "profile/profile_orders.html", {
        "active": "orders"
    })


@login_required
def profile_favorites(request):
    return render(request, "profile/profile_favorites.html", {
        "active": "favorites"
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
