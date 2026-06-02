from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product, ProductVariant


# ГЛАВНАЯ
def home(request):
    return render(request, "index.html")


# КАТАЛОГ
def catalog_view(request):
    products = Product.objects.all()

    query = request.GET.get("q")
    if query:
        products = products.filter(name__icontains=query)

    return render(request, "catalog/catalog.html", {
        "products": products
    })


# 📄 ТОВАР
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    variants = ProductVariant.objects.filter(product=product)

    return render(request, "catalog/product_detail.html", {
        "product": product,
        "variants": variants
    })


# ABOUT
def about_view(request):
    return render(request, "about.html")


#ПРОФИЛЬ (ЕДИНЫЙ!)
@login_required
def profile(request):
    context = {
        "user": request.user,
        "total_orders": 0,
        "recent_orders": [],
        "favorites_count": 0,
        "cart_count": 0,
    }
    return render(request, "profile/profile.html", context)


# ИЗБРАННОЕ
@login_required
def profile_favorites(request):
    return render(request, "profile/profile_favorites.html")


#ЗАКАЗЫ
@login_required
def profile_orders(request):
    return render(request, "profile/profile_orders.html")


#  НАСТРОЙКИ
@login_required
def profile_settings(request):
    return render(request, "profile/profile_settings.html")

@login_required(login_url='login')
def favorites_view(request):
    return render(request, "favorites.html")
