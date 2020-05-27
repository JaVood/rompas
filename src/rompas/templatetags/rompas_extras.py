from django.template import Library
from rompas.models import Product, BuyHistory
import datetime

register = Library()


@register.filter(name='download_check')
def download_check(user, product):
    history = BuyHistory.objects.filter(user_id=user.id)
    exist = False
    for i in history:
        if i.product_id == product.id:
            exist = True
    return exist
