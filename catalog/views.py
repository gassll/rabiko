from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from reviews.models import Review
from .models import Product, ProductVariant, Category, Favorite
from django.contrib import messages
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q


# ГЛАВНАЯ
def home(request):
    reviews = Review.objects.filter(is_published=True)[:6]

    recommended = Product.objects.order_by("?")[:5]

    return render(request, "index.html", {
        "reviews": reviews,
        "recommended": recommended
    })


# КАТАЛОГ
def catalog_view(request):
    favorites = []

    if request.user.is_authenticated:
        favorites = list(
            Favorite.objects.filter(
                user=request.user
            ).values_list(
                "product_id",
                flat=True
            )
        )

    products = Product.objects.filter(
        is_available=True
    )

    query = request.GET.get("q", "").strip()

    if query:
        products = (
            products
            .annotate(
                similarity=TrigramSimilarity("name", query)
            )
            .filter(
                Q(name__icontains=query) |
                Q(similarity__gt=0.1)
            )
            .order_by("-similarity")
        )

    category_slug = request.GET.get("category")

    if category_slug:
        products = products.filter(
            category__slug=category_slug
        )

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price:
        products = products.filter(
            price__gte=min_price
        )

    if max_price:
        products = products.filter(
            price__lte=max_price
        )

    categories = Category.objects.all()

    cart = request.session.get("cart", {})

    for product in products:
        qty = 0

        for variant in product.variants.all():
            qty += cart.get(str(variant.id), 0)

        product.cart_qty = qty

    return render(
        request,
        "catalog/catalog.html",
        {
            "products": products,
            "categories": categories,
            "favorites": favorites,

            "selected_category": category_slug,
            "min_price": min_price,
            "max_price": max_price,
        }
    )


# ТОВАР
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    variants = product.variants.all()

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    back_url = request.META.get("HTTP_REFERER")

    return render(
        request,
        "catalog/product_detail.html",
        {
            "product": product,
            "variants": variants,
            "related_products": related_products,
            "back_url": back_url,
        }
    )


# ABOUT
def about_view(request):
    return render(request, "about.html")


# ПРОФИЛЬ (ЕДИНЫЙ!)
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


# ЗАКАЗЫ
@login_required
def profile_orders(request):
    return render(request, "profile/profile_orders.html")


#  НАСТРОЙКИ
@login_required
def profile_settings(request):
    return render(request, "profile/profile_edit.html")


def reviews_view(request):
    if request.method == "POST":
        Review.objects.create(
            name=request.POST.get("name"),
            text=request.POST.get("text"),
            rating=request.POST.get("rating", 5),
            is_published=False
        )

        messages.success(
            request,
            "Спасибо! Ваш отзыв отправлен на модерацию "
        )

        return redirect("reviews")

    reviews = Review.objects.filter(
        is_published=True
    ).order_by("-created_at")

    return render(
        request,
        "reviews.html",
        {
            "reviews": reviews
        }
    )
