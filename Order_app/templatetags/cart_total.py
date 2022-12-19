from django import template
from Order_app.models import Order, Cart


register = template.Library()


@register.filter
def cart_total(user):
    order = Cart.objects.filter(user=user, purchased=False)


    if order.exists():
        return order.count()
    else:
        return 0