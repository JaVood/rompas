from django.db import models
from rompas.models import Product, Subscription, Tokens
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Order(models.Model):
    name = models.ForeignKey(User,
                             null=True,
                             on_delete=models.CASCADE,
                             verbose_name=_('Name'),
                             )
    created = models.DateTimeField(verbose_name='Create', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Update', auto_now=True)
    paid = models.BooleanField(verbose_name='Paid', default=False)
    paid_status = models.CharField(verbose_name='paid_status', max_length=50, blank=True)
    product = models.BooleanField(default=False)
    subscription = models.BooleanField(default=False)
    tokens = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order: {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost

    def save(self, *args, **kwargs):
        if self.paid_status == 'sandbox' or self.paid_status == 'success' or self.paid_status == 'wait_accept':
            self.paid = True
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE,)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, related_name='order_subscription', on_delete=models.PROTECT,
                                     null=True, blank=True)
    tokens = models.ForeignKey(Tokens, related_name='order_tokens', on_delete=models.PROTECT, null=True, blank=True)
    price = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Amount', default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
