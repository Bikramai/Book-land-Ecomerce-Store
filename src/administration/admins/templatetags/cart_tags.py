# yourapp/templatetags/cart_tags.py

from django import template
from ..models import Cart
from ..models import Wishlist

register = template.Library()

@register.simple_tag(takes_context=True)
def get_cart_item_count(context):
    request = context['request']
    if request.user.is_authenticated:
        return Cart.get_cart_item_count(request.user)
    return 0


