from rompas.models import Profile, MainCategory, PagesPhoto, BuyHistory, Currency
from orders.models import *
from orders.forms import OrderCreateForm
from rompas.forms import SignUpForm, EmailChangeForm, EmailSubscription, HelpForm, AddTokensForm, BuyHistoryForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.cart import Cart
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .liqpay import LiqPay
from core import settings
from django.http import HttpResponse, JsonResponse
from dateutil.relativedelta import relativedelta
import inflect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from time import gmtime, strftime
import requests
import json


def index(request):
    one = Subscription.objects.get(id=1)
    two = Subscription.objects.get(id=2)
    three = Subscription.objects.get(id=3)
    four = Subscription.objects.get(id=4)
    five = Subscription.objects.get(id=5)
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    left = MainCategory.objects.get(id=1)
    right_one = MainCategory.objects.get(id=2)
    right_two = MainCategory.objects.get(id=3)
    right_three = MainCategory.objects.get(id=4)
    top_image = PagesPhoto.objects.get(active=True, top=True)
    user = request.user
    return render(request, 'rompas/index.html', {'one': one,
                                                 'two': two,
                                                 'three': three,
                                                 'four': four,
                                                 'five': five,
                                                 'top_image': top_image,
                                                 'cart': cart,
                                                 'dollar': dollar,
                                                 'rompas': rompas,
                                                 'left': left,
                                                 'right_one': right_one,
                                                 'right_two': right_two,
                                                 'right_three': right_three,
                                                 'user': user,
                                                 })


def library_category(request, category_slug):
    user = request.user
    categories = MainCategory.objects.all()
    products = Product.objects.all()
    active_category = MainCategory.objects.get(slug=category_slug)
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    if request.method == 'POST':
        buy = BuyHistoryForm(request.POST)
        if buy.is_valid():
            buy.save()
            profile = Profile.objects.get(user_id=user.id)
            product = Product.objects.get(name=buy.cleaned_data.get('product'))
            profile.tokens_left -= product.price
            profile.save()
            return redirect('rompas:library_category', category_slug=category_slug)
    else:
        buy = BuyHistoryForm()
    return render(request, 'rompas/library-category.html', {'categories': categories,
                                                            'products': products,
                                                            'buy': buy,
                                                            'active_category': active_category,
                                                            'cart': cart,
                                                            'dollar': dollar,
                                                            'rompas': rompas,
                                                            'user': user,
                                                            })


def about(request):
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    user = request.user
    return render(request, 'rompas/about.html', {'cart': cart,
                                                 'dollar': dollar,
                                                 'rompas': rompas,
                                                 'user': user,
                                                 })


def faq(request):
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    user = request.user
    return render(request, 'rompas/faq.html', {'cart': cart,
                                               'dollar': dollar,
                                               'rompas': rompas,
                                               'user': user,
                                               })


def help(request):
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    user = request.user
    if request.method == 'POST':
        form = HelpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rompas:help_send')
    else:
        form = HelpForm()
    return render(request, 'rompas/help.html', {'form': form,
                                                'cart': cart,
                                                'dollar': dollar,
                                                'rompas': rompas,
                                                'user': user,
                                                })


def help_send(request):
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    user = request.user
    return render(request, 'rompas/help_send.html', {'cart': cart,
                                                     'dollar': dollar,
                                                     'rompas': rompas,
                                                     'user': user,
                                                     })


def private_policy(request):
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    user = request.user
    return render(request, 'rompas/private_policy.html', {'cart': cart,
                                                          'dollar': dollar,
                                                          'rompas': rompas,
                                                          'user': user,
                                                          })


def terms_of_use(request):
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    user = request.user
    return render(request, 'rompas/terms_of_use.html', {'cart': cart,
                                                        'dollar': dollar,
                                                        'rompas': rompas,
                                                        'user': user,
                                                        })


@login_required
def profile(request):
    user = request.user
    if user.is_authenticated == False:
        return redirect('/login')
    profile = Profile.objects.get(user_id=user.id)
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    subscription = Subscription.objects.exclude(id=1)
    tokens = Tokens.objects.all()
    if request.method == 'POST':
        change_password = PasswordChangeForm(request.user, request.POST)
        change_email = EmailChangeForm(request.POST)
        email_subscription = EmailSubscription(request.POST)
        add_tokens = AddTokensForm(request.POST)
        if change_password.is_valid():
            user = change_password.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('rompas:profile')
        elif change_email.is_valid():
            user.email = change_email.cleaned_data.get('email')
            user.save()
            return redirect('rompas:profile')
        elif add_tokens.is_valid():
            token = inflect.engine()
            return redirect('rompas:liqpay_tokens', profile_slug=profile.slug, tokens=token.number_to_words(add_tokens.cleaned_data.get('tokens')))
        elif email_subscription.is_valid():
            profile.email_subscription = email_subscription.cleaned_data.get('subscription')
            profile.save()
            return redirect('rompas:profile')
    else:
        change_password = PasswordChangeForm(request.user)
        change_email = EmailChangeForm()
        email_subscription = EmailSubscription()
        add_tokens = AddTokensForm()
    return render(request, 'rompas/profile.html', {'change_password': change_password,
                                                   'change_email': change_email,
                                                   'email_subscription': email_subscription,
                                                   'add_tokens': add_tokens,
                                                   'profile': profile,
                                                   'cart': cart,
                                                   'dollar': dollar,
                                                   'rompas': rompas,
                                                   'subscription': subscription,
                                                   'user': user,
                                                   'tokens': tokens,
                                                   })


@login_required
def purchase_history(request):
    user = request.user
    if user.is_authenticated == False:
        return redirect('/login')
    profile = Profile.objects.get(user_id=user.id)
    file = BuyHistory.objects.filter(user_id=user.id).order_by('-id')
    categories = MainCategory.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(file, 30)
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    try:
        files = paginator.page(page)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)
    return render(request, 'rompas/purchase_history.html', {'profile': profile,
                                                            'files': files,
                                                            'categories': categories,
                                                            'cart': cart,
                                                            'dollar': dollar,
                                                            'rompas': rompas,
                                                            'user': user,
                                                            })


@login_required
def purchase_history_category(request, category_slug):
    user = request.user
    if user.is_authenticated == False:
        return redirect('/login')
    profile = Profile.objects.get(user_id=user.id)
    category = MainCategory.objects.get(slug=category_slug)
    categories = MainCategory.objects.all()
    file = BuyHistory.objects.filter(user_id=user.id, product__category__category__main_category_id=category.id).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(file, 30)
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    try:
        files = paginator.page(page)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)
    return render(request, 'rompas/purchase_history_category.html', {'profile': profile,
                                                                     'files': files,
                                                                     'category': category,
                                                                     'categories': categories,
                                                                     'cart': cart,
                                                                     'dollar': dollar,
                                                                     'rompas': rompas,
                                                                     'user': user,
                                                                     })


def signin(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/profile')
    one = Subscription.objects.get(id=1)
    two = Subscription.objects.get(id=2)
    three = Subscription.objects.get(id=3)
    four = Subscription.objects.get(id=4)
    five = Subscription.objects.get(id=5)
    user = User.objects.all()
    users = []
    emails = []
    rompas = Currency.objects.get(id=2)
    for i in user:
        users.append(i.username)
        emails.append(i.email)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            subscriprion = Subscription.objects.get(name=form.cleaned_data.get('subscription'))
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            if subscriprion.id != 1:
                return redirect('rompas:buy_sub', sub_name=subscriprion.name)
            else:
                return redirect('/profile')
    else:
        form = SignUpForm
    return render(request, 'rompas/sign_in.html', {'form': form,
                                                   'one': one,
                                                   'two': two,
                                                   'three': three,
                                                   'four': four,
                                                   'five': five,
                                                   'users': users,
                                                   'emails': emails,
                                                   'rompas': rompas,
                                                   'user': user,
                                                   })


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        print('hi')
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        if sign == signature:
            print('callback is valid')
        response = liqpay.decode_data_from_str(data)
        print(response)
        order_id = response['order_id']
        status = response['status']
        profile = Profile.objects.get(order_id=order_id)
        if status == 'subscribed' or status == 'success':
            profile.subscription = True
            profile.subscription_ends = timezone.now() + relativedelta(months=1)
            profile.user_status_id = 2
            profile.save()
        if status == 'unsubscribed':
            profile.subscription = False
            profile.order_id = profile.order_id + '1'
            profile.save()
        return HttpResponse()


def index_ru(request):
    one = Subscription.objects.get(id=1)
    two = Subscription.objects.get(id=2)
    three = Subscription.objects.get(id=3)
    four = Subscription.objects.get(id=4)
    five = Subscription.objects.get(id=5)
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    left = MainCategory.objects.get(id=1)
    right_one = MainCategory.objects.get(id=2)
    right_two = MainCategory.objects.get(id=3)
    right_three = MainCategory.objects.get(id=4)
    top_image = PagesPhoto.objects.get(active=True, top=True)
    user = request.user
    return render(request, 'rompas/index_ru.html', {'one': one,
                                                    'two': two,
                                                     'three': three,
                                                     'four': four,
                                                     'five': five,
                                                     'top_image': top_image,
                                                     'cart': cart,
                                                     'dollar': dollar,
                                                     'rompas': rompas,
                                                     'left': left,
                                                     'right_one': right_one,
                                                     'right_two': right_two,
                                                     'right_three': right_three,
                                                     'user': user,
                                                     })


def library_category_ru(request, category_slug):
    user = request.user
    categories = MainCategory.objects.all()
    products = Product.objects.all()
    active_category = MainCategory.objects.get(slug=category_slug)
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    if request.method == 'POST':
        buy = BuyHistoryForm(request.POST)
        if buy.is_valid():
            buy.save()
            profile = Profile.objects.get(user_id=user.id)
            product = Product.objects.get(name=buy.cleaned_data.get('product'))
            profile.tokens_left -= product.price
            profile.save()
            return redirect('rompas:library_category_ru', category_slug=category_slug)
    else:
        buy = BuyHistoryForm()
    return render(request, 'rompas/library-category_ru.html', {'categories': categories,
                                                               'products': products,
                                                               'buy': buy,
                                                               'active_category': active_category,
                                                               'cart': cart,
                                                               'dollar': dollar,
                                                               'rompas': rompas,
                                                               'user': user,
                                                               })


def about_ru(request):
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    user = request.user
    return render(request, 'rompas/about_ru.html', {'cart': cart,
                                                    'dollar': dollar,
                                                    'rompas': rompas,
                                                    'user': user,
                                                    })


def faq_ru(request):
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    user = request.user
    return render(request, 'rompas/faq_ru.html', {'cart': cart,
                                                  'dollar': dollar,
                                                  'rompas': rompas,
                                                  'user': user,
                                                  })


def help_ru(request):
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    user = request.user
    if request.method == 'POST':
        form = HelpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rompas:help_send_ru')
    else:
        form = HelpForm()
    return render(request, 'rompas/help_ru.html', {'form': form,
                                                   'cart': cart,
                                                   'dollar': dollar,
                                                   'rompas': rompas,
                                                   'user': user,
                                                   })


def help_send_ru(request):
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    user = request.user
    return render(request, 'rompas/help_send_ru.html', {'cart': cart,
                                                        'dollar': dollar,
                                                        'rompas': rompas,
                                                        'user': user,
                                                        })


def private_policy_ru(request):
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    user = request.user
    return render(request, 'rompas/private_policy_ru.html', {'cart': cart,
                                                             'dollar': dollar,
                                                             'rompas': rompas,
                                                             'user': user,
                                                             })


def terms_of_use_ru(request):
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    user = request.user
    return render(request, 'rompas/terms_of_use_ru.html', {'cart': cart,
                                                           'dollar': dollar,
                                                           'rompas': rompas,
                                                           'user': user,
                                                           })


@login_required
def profile_ru(request):
    user = request.user
    if user.is_authenticated == False:
        return redirect('/login')
    profile = Profile.objects.get(user_id=user.id)
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    subscription = Subscription.objects.exclude(id=1)
    tokens = Tokens.objects.all()
    if request.method == 'POST':
        change_password = PasswordChangeForm(request.user, request.POST)
        change_email = EmailChangeForm(request.POST)
        email_subscription = EmailSubscription(request.POST)
        add_tokens = AddTokensForm(request.POST)
        if change_password.is_valid():
            user = change_password.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('rompas:profile_ru')
        elif change_email.is_valid():
            user.email = change_email.cleaned_data.get('email')
            user.save()
            return redirect('rompas:profile_ru')
        elif add_tokens.is_valid():
            token = inflect.engine()
            return redirect('rompas:liqpay_tokens', profile_slug=profile.slug, tokens=token.number_to_words(add_tokens.cleaned_data.get('tokens')))
        elif email_subscription.is_valid():
            profile.email_subscription = email_subscription.cleaned_data.get('subscription')
            profile.save()
            return redirect('rompas:profile_ru')
    else:
        change_password = PasswordChangeForm(request.user)
        change_email = EmailChangeForm()
        email_subscription = EmailSubscription()
        add_tokens = AddTokensForm()
    return render(request, 'rompas/profile_ru.html', {'change_password': change_password,
                                                      'change_email': change_email,
                                                      'email_subscription': email_subscription,
                                                      'add_tokens': add_tokens,
                                                      'profile': profile,
                                                      'cart': cart,
                                                      'dollar': dollar,
                                                      'rompas': rompas,
                                                      'subscription': subscription,
                                                      'user': user,
                                                      'tokens': tokens,
                                                      })


@login_required
def purchase_history_ru(request):
    user = request.user
    profile = Profile.objects.get(user_id=user.id)
    file = BuyHistory.objects.filter(user_id=user.id).order_by('-id')
    categories = MainCategory.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(file, 30)
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    try:
        files = paginator.page(page)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)
    return render(request, 'rompas/purchase_history_ru.html', {'profile': profile,
                                                               'files': files,
                                                               'categories': categories,
                                                               'cart': cart,
                                                               'dollar': dollar,
                                                               'rompas': rompas,
                                                               'user': user,
                                                               })


@login_required
def purchase_history_category_ru(request, category_slug):
    user = request.user
    profile = Profile.objects.get(user_id=user.id)
    category = MainCategory.objects.get(slug=category_slug)
    categories = MainCategory.objects.all()
    file = BuyHistory.objects.filter(user_id=user.id, product__category__category__main_category_id=category.id).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(file, 30)
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    try:
        files = paginator.page(page)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)
    return render(request, 'rompas/purchase_history_category_ru.html', {'profile': profile,
                                                                        'files': files,
                                                                        'category': category,
                                                                        'categories': categories,
                                                                        'cart': cart,
                                                                        'dollar': dollar,
                                                                        'rompas': rompas,
                                                                        'user': user,
                                                                        })


def signin_ru(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/ru/profile')
    one = Subscription.objects.get(id=1)
    two = Subscription.objects.get(id=2)
    three = Subscription.objects.get(id=3)
    four = Subscription.objects.get(id=4)
    five = Subscription.objects.get(id=5)
    user = User.objects.all()
    users = []
    emails = []
    rompas = Currency.objects.get(id=2)
    for i in user:
        users.append(i.username)
        emails.append(i.email)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            subscriprion = Subscription.objects.get(name=form.cleaned_data.get('subscription'))
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            if subscriprion.id != 1:
                return redirect('rompas:buy_sub', sub_name=subscriprion.name)
            else:
                return redirect('/ru/profile')
    else:
        form = SignUpForm
    return render(request, 'rompas/sign_in_ru.html', {'form': form,
                                                      'one': one,
                                                      'two': two,
                                                      'three': three,
                                                      'four': four,
                                                      'five': five,
                                                      'users': users,
                                                      'emails': emails,
                                                      'rompas': rompas,
                                                      'user': user,
                                                      })


@login_required
def cart_form(request):
    cart = Cart(request)
    user = request.user
    order = Order(name=user, product=True)
    order.save()
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'],
                                 price=item['price'],
                                 quantity=item['quantity'])
    cart.clear()

    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    products = OrderItem.objects.filter(order_id=order)
    price = 0
    for i in products:
        price += i.quantity * i.price
    params = {
        'action': 'pay',
        'amount': float(price),
        'currency': 'USD',
        'description': 'items Rompas.com.ua',
        'order_id': order.id,
        'version': '3',
        'server_url': 'https://www.rompas.com.ua/order/pay-callback/',
        'language': 'en',
    }
    data = {
        'signature': liqpay.cnb_signature(params),
        'data': liqpay.cnb_data(params),
    }
    return JsonResponse(data)


@login_required
def subscription(request, subscription_name):
    subscription = Subscription.objects.get(name=subscription_name)
    user = request.user
    order = Order(name=user, subscription=True)
    order.save()
    OrderItem.objects.create(order=order, subscription_id=subscription.id,
                             price=subscription.price,
                             quantity=1)
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    params = {
        'action': 'subscribe',
        'amount': subscription.price,
        'currency': 'USD',
        'description': 'Rompas subscription',
        'order_id': order.id,
        'version': '3',
        'subscribe_periodicity': 'month',
        'subscribe_date_start': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
        'server_url': 'https://www.rompas.com.ua/order/sub-pay-callback/',
        'language': 'en',
    }
    data = {
        'signature': liqpay.cnb_signature(params),
        'data': liqpay.cnb_data(params),
    }
    return JsonResponse(data)


@login_required
def subscription_update(request, subscription_name):
    subscription = Subscription.objects.get(name=subscription_name)
    user = request.user
    order = Order(name=user, subscription=True)
    order.save()
    OrderItem.objects.create(order=order, subscription_id=subscription.id,
                             price=subscription.price,
                             quantity=1)
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    params = {
        'action': 'subscribe',
        'amount': subscription.price,
        'currency': 'USD',
        'description': 'Rompas Update subscription',
        'order_id': order.id,
        'version': '3',
        'subscribe_periodicity': 'month',
        'subscribe_date_start': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
        'server_url': 'https://www.rompas.com.ua/order/update/update-callback/',
        'language': 'en',
    }
    data = {
        'signature': liqpay.cnb_signature(params),
        'data': liqpay.cnb_data(params),
    }
    return JsonResponse(data)


@login_required
def cancel_subscription(request):
    user = request.user
    order = Order.objects.filter(name=user, subscription=True).order_by('-id')[0]
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    params = {
        "action": "unsubscribe",
        "version": "3",
        "order_id": order.id,
        "language": 'en',
    }
    post_data = {'data': liqpay.cnb_data(params), 'signature': liqpay.cnb_signature(params)}
    response = requests.post('https://www.liqpay.ua/api/request', data=post_data)
    content = json.loads(response.content)
    status = content['status']
    order.paid_status = status
    order.save()
    answer = False
    if status == 'unsubscribed' or status == 'success':
        profile = Profile.objects.get(user_id=order.name_id)
        profile.subscription_active = False
        profile.save()
        answer = True
    data = {
        'answer': answer,
    }
    return JsonResponse(data)


def add_tokens(request, tokens_name):
    user = request.user
    order = Order(name=user, tokens=True)
    order.save()
    token = Tokens.objects.get(name=tokens_name)
    OrderItem.objects.create(order=order, tokens_id=token.id,
                             price=token.price,
                             quantity=1)
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    params = {
        'action': 'pay',
        'amount': token.price,
        'currency': 'USD',
        'description': 'Tokens Rompas.com.ua',
        'order_id': order.id,
        'version': '3',
        'server_url': 'https://www.rompas.com.ua/order/token-pay-callback/',
        'language': 'en',
    }
    data = {
        'signature': liqpay.cnb_signature(params),
        'data': liqpay.cnb_data(params),
    }
    return JsonResponse(data)


def buy_sub(request, sub_name):
    subscription = Subscription.objects.get(name=sub_name)
    user = request.user
    order = Order(name=user, subscription=True)
    order.save()
    OrderItem.objects.create(order=order, subscription_id=subscription.id,
                             price=subscription.price,
                             quantity=1)
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    cart = Cart(request)
    dollar = Currency.objects.get(id=1)
    rompas = Currency.objects.get(id=2)
    params = {
        'action': 'subscribe',
        'amount': subscription.price,
        'currency': 'USD',
        'description': 'Rompas subscription',
        'order_id': order.id,
        'version': '3',
        'subscribe_periodicity': 'month',
        'subscribe_date_start': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
        'server_url': 'https://www.rompas.com.ua/order/sub-pay-callback/',
        'language': 'en',
    }
    return render(request, 'rompas/buy_sub.html', {'user': user,
                                                   'signature': liqpay.cnb_signature(params),
                                                   'data': liqpay.cnb_data(params),
                                                   'cart': cart,
                                                   'rompas': rompas,
                                                   'dollar': dollar,
                                                   })



@staff_member_required
def AdminOrderDetail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


def test(request):
    cart = Cart(request)
    print(cart)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
    form = OrderCreateForm()
    return render(request, 'rompas/test.html', {'cart': cart,
                                                'form': form,
                                                })
