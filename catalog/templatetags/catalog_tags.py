from django import template

from catalog.models import Version

register = template.Library()


@register.filter(needs_autoescape=True)
def price_format(price: int, autoescape=True):
    price_string = str(price)[::-1]
    chunked = [price_string[i: i + 3][::-1] for i in range(0, len(price_string), 3)][
        ::-1
    ]

    format_string = " ".join(chunked) + " ₽"
    return format_string


@register.simple_tag()
def media_path(path: str):
    """Returns object media url if exists, else photo placeholder"""
    if path:
        return f"/media/{path}"
    return "/static/img/no_photo.jpg"


@register.filter()
def is_version_active(version: Version):
    """Check is that version is active"""
    if not isinstance(version, Version):
        raise ValueError('Tag is_version_active can be used only with Version instances')
    return version.is_active
