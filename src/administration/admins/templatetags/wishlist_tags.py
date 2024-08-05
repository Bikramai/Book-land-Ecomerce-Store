
from django import template
from ..models import Wishlist


register = template.Library()

@register.simple_tag(takes_context=True)
def get_wishlist_item_count(context):
    request = context['request']
    if request.user.is_authenticated:
        return Wishlist.get_wishlist_item_count(request.user)
    return 0