from django.conf.urls import url, include
from . import views
from orders.views import PayCallbackView, SubUpdCallbackView, SubPayCallbackView

urlpatterns = [
    url(r'^create/$', views.OrderCreate, name='OrderCreate'),
    url(r'^admin/order/(?P<order_id>\d+)/$', views.AdminOrderDetail, name='AdminOrderDetail'),
    url(r'^admin/order/(?P<order_id>\d+)/pdf/$', views.AdminOrderPDF, name='AdminOrderPDF'),
    url(r'^form_send/$', views.form_send, name='form_send'),
    url(r'^pay-callback/$', PayCallbackView.as_view(), name='pay_callback'),
    url(r'^sub-pay-callback/$', SubPayCallbackView.as_view(), name='sub_pay_callback'),
    url(r'^update/update-callback/$', SubUpdCallbackView.as_view(), name='update-callback'),
]
