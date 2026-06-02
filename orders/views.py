from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Order, DeliveryAddress
from cart.views import CartService


@login_required
def checkout(request):
    cart = CartService(request)
    items, total = cart.items()

    if request.method == "POST":
        # твоя логика заказа (уже делали раньше)
        pass

    addresses = DeliveryAddress.objects.filter(user=request.user)

    return render(request, "orders/checkout.html", {
        "items": items,
        "total": total,
        "addresses": addresses
    })


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, "orders/order_list.html", {
        "orders": orders
    })


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    return render(request, "orders/order_detail.html", {
        "order": order
    })