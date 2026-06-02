from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import ProductVariant


class CartService:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get("cart", {})

    def add(self, variant_id, quantity=1):
        variant_id = str(variant_id)

        if variant_id in self.cart:
            self.cart[variant_id] += quantity
        else:
            self.cart[variant_id] = quantity

        self.save()

    def remove(self, variant_id):
        variant_id = str(variant_id)

        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True

    def items(self):
        variants = ProductVariant.objects.filter(id__in=self.cart.keys())

        items = []
        total = 0

        for variant in variants:
            qty = self.cart[str(variant.id)]
            price = variant.price  # 🔥 ТОЛЬКО СЕРВЕРНАЯ ЦЕНА

            items.append({
                "variant": variant,
                "quantity": qty,
                "price": price,
                "sum": price * qty
            })

            total += price * qty

        return items, total

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True


def add_to_cart(request, variant_id):
    cart = CartService(request)
    cart.add(variant_id)

    return redirect("cart_detail")


def cart_detail(request):
    cart = CartService(request)

    items, total = cart.items()

    return render(request, "cart/cart_detail.html", {
        "items": items,
        "total": total
    })


def remove_from_cart(request, variant_id):
    cart = CartService(request)
    cart.remove(variant_id)

    return redirect("cart_detail")


def clear_cart(request):
    cart = CartService(request)
    cart.clear()

    return redirect("cart_detail")