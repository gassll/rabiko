from django.core.management.base import BaseCommand
from django.utils.text import slugify

from catalog.models import (
    Category,
    Product,
    ProductImage,
    Size,
    Color,
    ProductVariant
)

import random


DATA = {
    "Боди": [
        {
            "name": "Боди майки для новорожденных",
            "main": "products/body-1-main.webp",
            "images": [
                "products/body-1-2.webp",
                "products/body-1-3.webp",
                "products/body-1-4.webp",
            ]
        },
        {
            "name": "Боди для новорожденных",
            "main": "products/body-2-main.webp",
            "images": [
                "products/body-2-2.webp",
                "products/body-2-3.webp",
            ]
        },
    ],

    "Песочники": [
        {
            "name": "Песочники для малышей",
            "main": "products/sandpipers-1-main.webp",
            "images": [
                "products/sandpipers-1-2.webp",
                "products/sandpipers-1-3.webp",
            ]
        },
        {
            "name": "Песочник для малышей",
            "main": "products/sandpipers-2-main.webp",
            "images": [
                "products/sandpipers-2-2.webp",
                "products/sandpipers-2-3.webp",
            ]
        },
    ],

    "Маечки": [
        {
            "name": "Майки для малышей",
            "main": "products/T-shirt-1-main.webp",
            "images": [
                "products/T-shirt-1-2.webp",
                "products/T-shirt-1-3.webp",
            ]
        },
{
            "name": "Майки для малышей",
            "main": "products/T-shirt-2-main.webp",
            "images": [
                "products/T-shirt-2-2.webp",
                "products/T-shirt-2-3.webp",
            ]
        }
    ]
}


class Command(BaseCommand):
    help = "Заполнение каталога товарами"


    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        ProductVariant.objects.all().delete()
        ProductImage.objects.all().delete()
        Product.objects.all().delete()


        sizes = ["50", "56", "62", "68", "74", "80"]

        for size in sizes:
            Size.objects.get_or_create(name=size)

        colors = [
            "Белый",
            "Бежевый",
            "Кремовый",
            "Розовый",
            "Голубой",
        ]

        for color in colors:
            Color.objects.get_or_create(name=color)

        all_sizes = list(Size.objects.all())
        all_colors = list(Color.objects.all())

        for category_name, products in DATA.items():

            base_slug = slugify(category_name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            category = Category.objects.create(
                name=category_name,
                slug=slug
            )

            for item in products:

                product = Product.objects.create(
                    category=category,
                    name=item["name"],
                    slug=f"{slugify(item['name'])}-{random.randint(1000, 9999)}",
                    description="Мягкая и качественная одежда для новорожденных от Rabiko.",
                    price=random.randint(500, 5000),
                    stock=random.randint(5, 50),
                    image=item["main"]
                )

                for image_path in item["images"]:

                    ProductImage.objects.create(
                        product=product,
                        image=image_path
                    )

                for _ in range(3):

                    ProductVariant.objects.create(
                        product=product,
                        size=random.choice(all_sizes),
                        color=random.choice(all_colors),
                        stock=random.randint(1, 20)
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Каталог успешно заполнен"
            )
        )