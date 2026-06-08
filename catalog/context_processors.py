from catalog.models import Favorite

def cart_counter(request):
    cart = request.session.get("cart", {})
    count = sum(cart.values())

    return {
        "cart_count": count
    }


def favorites_counter(request):
    if request.user.is_authenticated:
        count = Favorite.objects.filter(user=request.user).count()
    else:
        count = 0

    return {
        "favorites_count": count
    }