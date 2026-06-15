from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

        fields = [
            "category",
            "name",
            "description",
            "price",
            "image",
            "is_available",
        ]

        widgets = {
            "category": forms.Select(
                attrs={"class": "form-select"}
            ),

            "name": forms.TextInput(
                attrs={"class": "form-input"}
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 6
                }
            ),

            "price": forms.NumberInput(
                attrs={"class": "form-input"}
            ),
            "is_available": forms.CheckboxInput(
                attrs={"class": "form-checkbox"}
            ),
        }