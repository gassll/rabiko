from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, DeliveryAddress, OrderItem
from cart.views import CartService
from django.shortcuts import redirect




@login_required
def checkout(request):
    cart = CartService(request)
    items, total = cart.items()

    if request.method == "POST":

        order = Order.objects.create(
            user=request.user,
            total_price=total
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product_variant=item["variant"],
                price=item["price"],
                quantity=item["quantity"]
            )

        # очистка корзины
        request.session["cart"] = {}

        messages.success(
            request,
            f"Заказ №{order.id} успешно оформлен!"
        )

        return redirect("order_list")

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


@login_required
def cancel_order(request, pk):
    order = Order.objects.get(
        pk=pk,
        user=request.user
    )

    if order.status in ["new", "processing"]:
        order.status = "cancelled"
        order.save()

        messages.success(
            request,
            f"Заказ №{order.id} отменён"
        )

    return redirect("profile_orders")