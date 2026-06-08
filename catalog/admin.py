from django.contrib import admin
from .models import Size, Product, ProductVariant

admin.site.register(Size)
admin.site.register(Product)
admin.site.register(ProductVariant)