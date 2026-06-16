from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from catalog.models import Product, Favorite


@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    favorite_qs = Favorite.objects.filter(
        user=request.user,
        product=product
    )

    if favorite_qs.exists():
        favorite_qs.delete()

    else:
        Favorite.objects.create(
            user=request.user,
            product=product
        )

    return redirect(request.META.get("HTTP_REFERER", "/"))


from cart.views import CartService

@login_required
def favorites_list(request):
    favorites = (
        Favorite.objects
        .filter(user=request.user)
        .select_related("product")
    )

    cart = CartService(request)
    cart_dict = cart.cart

    for fav in favorites:
        variant = fav.product.variants.first()
        fav.cart_qty = cart_dict.get(str(variant.id), 0) if variant else 0

    return render(
        request,
        "favorites.html",
        {
            "favorites": favorites
        }
    )