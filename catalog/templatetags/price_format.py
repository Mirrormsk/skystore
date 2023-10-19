from django import template

register = template.Library()


@register.filter(needs_autoescape=True)
def price_format(price: int, autoescape=True):
    price_string = str(price)[::-1]
    chunked = [price_string[i:i + 3][::-1] for i in range(0, len(price_string), 3)][::-1]

    format_string = ' '.join(chunked) + ' ₽'
    return format_string
