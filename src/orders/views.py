from django.shortcuts import get_object_or_404
from orders.models import OrderItem, Order
from orders.forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from orders.liqpay import LiqPay
from django.shortcuts import render
from django.http import HttpResponse
from core import settings
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rompas.models import BuyHistory, Profile
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import requests



@staff_member_required
def AdminOrderPDF(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    # weasyprint.HTML(string=html).write_pdf(response,
    #            stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/bootstrap.min.css')])
    return response


@staff_member_required
def AdminOrderDetail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


def OrderCreate(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.warehouse = order.nova_warehouse
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return form_send(request, order=order)
    form = OrderCreateForm()

    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form,
                                                        })


def form_send(request, order):
    cart = Cart(request)
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    a = OrderItem.objects.filter(order_id=order)
    price = 0
    for i in a:
        price += i.quantity * i.price
    price = (price * 103) / 100
    params = {
        'action': 'pay',
        'amount': float(price),
        'currency': 'UAH',
        'description': order.id,
        'order_id': order.id,
        'version': '3',
        'server_url': 'https://pasta-family.com.ua/order/pay-callback/',
        'language': 'ua',
    }
    signature = liqpay.cnb_signature(params)
    data = liqpay.cnb_data(params)
    return render(request, 'orders/order/form_send.html', {'signature': signature,
                                                           'data': data,
                                                           'cart': cart,
                                                           'order': order})


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        if sign == signature:
            print('callback is valid')
        response = liqpay.decode_data_from_str(data)
        order_id = response['order_id']
        status = response['status']
        order = Order.objects.get(id=order_id)
        new = False
        if order.paid_status != 'subscribed' and order.paid_status != 'success' and not order.paid_status:
            new = True
        order.paid_status = status
        order.save()
        products = OrderItem.objects.filter(order_id=order.id, product_id__isnull=False)
        if new:
            if status == 'success':
                for i in products:
                    a = BuyHistory(user_id=order.name_id, product_id=i.product_id)
                    a.save()
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class SubPayCallbackView(View):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        if sign == signature:
            print('callback is valid')
        response = liqpay.decode_data_from_str(data)
        order_id = response['order_id']
        status = response['status']
        order = Order.objects.get(id=order_id)
        new = False
        if order.paid_status != 'subscribed' and order.paid_status != 'success' and not order.paid_status:
            new = True
        order.paid_status = status
        order.save()
        subscriptions = OrderItem.objects.filter(order_id=order.id)
        profile = Profile.objects.get(user_id=order.name_id)
        if new:
            if status == 'subscribed' or status == 'success':
                profile.subscription_active = True
                profile.subscription_end = timezone.now() + relativedelta(months=1)
                for i in subscriptions:
                    profile.subscription_id = i.subscription_id
                    profile.tokens_left += i.subscription.token
                profile.save()
            else:
                profile.subscription_active = False
                profile.save()
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class SubUpdCallbackView(View):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        if sign == signature:
            print('callback is valid')
        response = liqpay.decode_data_from_str(data)
        order_id = response['order_id']
        status = response['status']
        order = Order.objects.get(id=order_id)
        new = False
        if order.paid_status != 'subscribed' and order.paid_status != 'success' and not order.paid_status:
            new = True
        order.paid_status = status
        order.save()
        subscriptions = OrderItem.objects.filter(order_id=order.id)[0]
        profile = Profile.objects.get(user_id=order.name_id)
        if new:
            if status == 'subscribed' or status == 'success':
                if profile.subscription_id == subscriptions.subscription_id:
                    profile.subscription_active = True
                    profile.subscription_end = timezone.now() + relativedelta(months=1)
                    profile.tokens_left += subscriptions.subscription.token
                    profile.save()
                else:
                    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
                    params = {
                        "action": "unsubscribe",
                        "version": "3",
                        "order_id": Order.objects.filter(name_id=order.name_id, subscription=True)[1].id,
                        "language": 'en',
                    }
                    post_data = {'data': liqpay.cnb_data(params), 'signature': liqpay.cnb_signature(params)}
                    requests.post('https://www.liqpay.ua/api/request', data=post_data)
                    profile.subscription_active = True
                    profile.subscription_end = timezone.now() + relativedelta(months=1)
                    profile.subscription_id = subscriptions.subscription_id
                    profile.tokens_left += subscriptions.subscription.token
                    profile.save()
            elif profile.subscription_end < timezone.now():
                profile.subscription_active = False
                profile.save()
        return HttpResponse()
