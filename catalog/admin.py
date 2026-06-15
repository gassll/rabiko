from django.contrib import admin
from .models import Category, Product, ProductVariant, Size, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    max_num = 10


def create_all_variants(modeladmin, request, queryset):
    for product in queryset:
        sizes = Size.objects.all()

        for size in sizes:
            ProductVariant.objects.get_or_create(
                product=product,
                size=size
            )


create_all_variants.short_description = "Создать все размеры автоматически"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "price",
        "is_available",
        "created_at",
    )

    list_filter = (
        "category",
        "is_available",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    inlines = [ProductVariantInline, ProductImageInline]

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None

        super().save_model(request, obj, form, change)

        if is_new:
            sizes = Size.objects.all()

            for size in sizes:
                ProductVariant.objects.get_or_create(
                    product=obj,
                    size=size
                )

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "size",
    )

    list_filter = (
        "product__category",
        "size",
    )

    search_fields = (
        "product__name",
        "size__name",
    )