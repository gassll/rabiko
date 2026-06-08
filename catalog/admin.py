from django.contrib import admin
from .models import Size, Color, Product, ProductVariant

admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(ProductVariant)