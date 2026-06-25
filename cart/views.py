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

        current = self.cart.get(variant_id, 0)

        limit_reached = False

        if current >= 20:
            return current, True  # уже лимит

        new_qty = min(current + quantity, 20)

        if new_qty == 20:
            limit_reached = True

        self.cart[variant_id] = new_qty
        self.save()

        return new_qty, limit_reached

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

    def get_total(self):
        from catalog.models import ProductVariant

        variants = ProductVariant.objects.filter(id__in=self.cart.keys())

        total = 0
        for v in variants:
            qty = self.cart.get(str(v.id), 0)
            total += qty * v.product.price

        return total


# ----------------- VIEWS -----------------


def add_to_cart(request, variant_id):
    cart = CartService(request)

    qty, limit_reached = cart.add(variant_id)

    variant = ProductVariant.objects.get(id=variant_id)

    return JsonResponse({
        "qty": qty,
        "count": cart.get_count(),
        "line_sum": qty * variant.product.price,
        "total": cart.get_total(),
        "limit_reached": limit_reached,
    })


def decrease_quantity(request, variant_id):
    cart = CartService(request)
    cart.decrease(variant_id)

    items, total = cart.items()

    qty = cart.cart.get(str(variant_id), 0)
    variant = ProductVariant.objects.get(id=variant_id)
    line_sum = qty * variant.product.price

    return JsonResponse({
        "qty": qty,
        "count": cart.get_count(),
        "line_sum": line_sum,
        "total": total,
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