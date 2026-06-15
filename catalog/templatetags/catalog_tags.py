from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)


@register.filter
def rub(value):
    try:
        value = float(value)

        if value.is_integer():
            return f"{int(value)} ₽"

        return f"{value:.2f}".rstrip("0").rstrip(".") + " ₽"

    except:
        return value