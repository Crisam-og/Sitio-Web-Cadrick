from django import template
from django.conf import settings

register = template.Library()

@register.filter
def get_image(obj, image_field):
    image = getattr(obj, image_field)
    if image:
        return '{}{}'.format(settings.MEDIA_URL, image)
    return '{}{}'.format(settings.STATIC_URL, 'img/image_not_found.png')