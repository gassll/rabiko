from django.shortcuts import render
from catalog.models import ProductVariant
from django.http import JsonResponse


class CartService:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get("cart", {})

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True
        self.session.save()

    def add(self, variant_id, quantity=1):
        variant_id = str(variant_id)

        self.cart[variant_id] = self.cart.get(variant_id, 0) + quantity
        self.save()

    def decrease(self, variant_id):
        variant_id = str(variant_id)

        if variant_id in self.cart:
            self.cart[variant_id] -= 1

            if self.cart[variant_id] <= 0:
                del self.cart[variant_id]

        self.save()

    def remove(self, variant_id):
        variant_id = str(variant_id)

        if variant_id in self.cart:
            del self.cart[variant_id]

        self.save()

    def clear(self):
        self.cart = {}
        self.save()

    def items(self):
        variants = ProductVariant.objects.filter(id__in=self.cart.keys())

        items = []
        total = 0

        for variant in variants:
            qty = self.cart.get(str(variant.id), 0)
            price = variant.product.price

            items.append({
                "variant": variant,
                "quantity": qty,
                "price": price,
                "sum": price * qty
            })

            total += price * qty

        return items, total

    def get_count(self):
        return sum(self.cart.values())


# ----------------- VIEWS -----------------

def add_to_cart(request, variant_id):
    cart = CartService(request)
    cart.add(variant_id)

    return JsonResponse({
        "qty": cart.cart.get(str(variant_id), 0),
        "count": cart.get_count()
    })


def decrease_quantity(request, variant_id):
    cart = CartService(request)
    cart.decrease(variant_id)

    return JsonResponse({
        "qty": cart.cart.get(str(variant_id), 0),
        "count": cart.get_count()
    })


def remove_from_cart(request, variant_id):
    cart = CartService(request)
    cart.remove(variant_id)

    return JsonResponse({
        "count": cart.get_count()
    })


def clear_cart(request):
    cart = CartService(request)
    cart.clear()

    return JsonResponse({
        "count": 0
    })


def cart_detail(request):
    cart = CartService(request)
    items, total = cart.items()

    return render(request, "cart/cart_detail.html", {
        "items": items,
        "total": total,
    })


def cart_count(request):
    cart = CartService(request)
    return JsonResponse({
        "count": cart.get_count()
    })