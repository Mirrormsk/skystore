
from django import template
from django.db.models import ImageField

register = template.Library()


@register.filter(needs_autoescape=True)
def price_format(price: int, autoescape=True):
    price_string = str(price)[::-1]
    chunked = [price_string[i:i + 3][::-1] for i in range(0, len(price_string), 3)][::-1]

    format_string = ' '.join(chunked) + ' ₽'
    return format_string


@register.simple_tag()
def media_path(path: str):
    """Returns object media url if exists, else photo placeholder"""
    if path:
        return f"../../media/{path}"
    return '/static/img/no_photo.jpg'


# @register.filter()
# def photo_placeholder(photo):
#     if not photo:
#         return '/static/img/no_photo.jpg'
#     return photo.url
