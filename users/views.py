from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .forms import ProfileUpdateForm

from django.contrib.auth import get_user_model

from users.forms import RegisterForm

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

    return render(request, "registration/register.html", {
        "form": form
    })


# LOGIN
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
                return redirect("profile")

            form.add_error(None, "Неверный логин или пароль")

    return render(request, "registration/login.html", {
        "form": form
    })


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request):
    return render(request, "profile/profile.html", {
        "user": request.user
    })

@login_required
def profile_settings(request):
    user = request.user

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile_settings")
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, "profile/profile_settings.html", {
        "form": form
    })
