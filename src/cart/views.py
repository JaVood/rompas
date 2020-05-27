from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from rompas.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.http import HttpResponseRedirect


@require_POST
def CartAdd(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=1, update_quantity=cd['update'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def CartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def CartDetail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })
    return render(request, 'cart/cart.html', {'cart': cart})
