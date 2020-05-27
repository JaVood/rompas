from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel
import datetime
from django.utils.translation import gettext as _
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import re
from transliterate import translit
from transliterate.exceptions import LanguageDetectionError


def transliterate(text):
    pieces = str(re.sub('[\W]+', ' ', text)).lower().split(' ')
    result = []

    for piece in pieces:
        try:
            result.append(translit(piece, reversed=True))
        except LanguageDetectionError:
            result.append(piece)
    return '-'.join([r for r in result if r])


class Currency(BaseModel):
    name = models.CharField(
        max_length=16,
        unique=True,
        verbose_name=_('Name'),
    )

    symbol = models.ImageField(verbose_name='Sybmol', null=True, blank=True)

    def __str__(self):
        return self.name


class MainCategory(models.Model):
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name'),
    )

    name_ru = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name Ru'),
    )

    photo = models.ImageField(verbose_name='Photo', null=True, blank=True)

    photo_ru = models.ImageField(verbose_name='Photo Ru', null=True, blank=True)

    description = models.TextField(
        max_length=2000,
        verbose_name=_('Description'),
        blank=True,
        null=True,
    )

    description_ru = models.TextField(
        max_length=2000,
        verbose_name=_('Description Ru'),
        blank=True,
        null=True,
    )

    slug = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Slug'),
        help_text="Don't touch it!"
    )

    def cat(self):
        return Category.objects.filter(main_category_id=self.id)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name'),
    )

    name_ru = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name Ru'),
    )

    price = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Price'),
    )

    slug = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Slug'),
        help_text="Don't touch it!"
    )

    token = models.IntegerField(verbose_name=_('Token'), null=True)

    def __str__(self):
        return self.name


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    subscription = models.ForeignKey(Subscription,
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL,
                                     verbose_name=_('Subscription'),
                                     )

    subscription_end = models.DateTimeField(
        verbose_name='Subscription ends',
        null=True,
        blank=True
    )

    tokens_left = models.IntegerField(blank=True, null=True, verbose_name=_('Tokens Left'), default=0)

    slug = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Slug'),
        help_text="Don't touch it!"
    )

    name = models.CharField(verbose_name='Name', max_length=150, null=True, blank=True)

    bonus = models.BooleanField(default=False)

    email_subscription = models.BooleanField(default=True, verbose_name=_('Email subscription'))

    subscription_active = models.BooleanField(default=False, verbose_name=_('Subscription active'))

    def save(self, *args, **kwargs):
        self.slug = transliterate(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name'),
    )

    name_ru = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name Ru'),
    )

    slug = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Slug'),
        help_text="Don't touch it!"
    )

    main_category = models.ForeignKey(MainCategory,
                                      null=True,
                                      on_delete=models.SET_NULL,
                                      verbose_name=_('Main Category'),
                                      )

    def sub(self):
        return SubCategory.objects.filter(category_id=self.id)

    def __str__(self):
        return self.name + ' - ' + self.main_category.name


class SubCategory(models.Model):
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name'),
    )

    name_ru = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name Ru'),
    )

    slug = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Slug'),
        help_text="Don't touch it!"
    )

    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name=_('Category'),
                                 )

    def __str__(self):
        return self.name + ' - ' + self.category.name + ' - ' + self.category.main_category.name


class Product(BaseModel):
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name'),
    )

    name_ru = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name Ru'),
    )

    slug = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Slug'),
        help_text="Don't touch it!"
    )

    description = models.TextField(
        max_length=2000,
        verbose_name=_('Description'),
        blank=True,
        null=True,
    )

    description_ru = models.TextField(
        max_length=2000,
        verbose_name=_('Description Ru'),
        blank=True,
        null=True,
    )

    category = models.ForeignKey(SubCategory,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name=_('Category'),
                                 )

    currency = models.ForeignKey(Currency,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name=_('Currency'),
                                 )

    url = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        verbose_name=_('Url'),
    )

    you_tube = models.URLField(verbose_name=_('You_Tube, Only Assets'), blank=True, null=True)

    file_size = models.IntegerField(verbose_name=_('Size'), default=0)

    main_photo = models.ImageField(verbose_name='Main Photo')

    price = models.IntegerField(verbose_name=_('Price'))

    old_price = models.IntegerField(null=True, blank=True, verbose_name=_('Old Price'),)

    file = models.FileField(null=True, blank=True)

    def image(self):
        return Image.objects.filter(product_id=self.id)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product,
                                null=True,
                                on_delete=models.CASCADE,
                                verbose_name=_('Product'),
                                )

    photo = models.ImageField(verbose_name='Photo', null=True, blank=True)

    def __str__(self):
        return self.product.name


class BuyHistory(models.Model):
    user = models.ForeignKey(User,
                             null=True,
                             on_delete=models.CASCADE,
                             verbose_name=_('User'),
                             )

    product = models.ForeignKey(Product,
                                null=True,
                                on_delete=models.CASCADE,
                                verbose_name=_('Product'),
                                )

    date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Purchased at'),
        null=True
    )

    def __str__(self):
        return self.user.username


class PagesPhoto(models.Model):
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name'),
    )

    photo = models.ImageField(verbose_name='Photo', null=True, blank=True)

    photo_ru = models.ImageField(verbose_name='Photo ru', null=True, blank=True)

    active = models.BooleanField(default=False)

    top = models.BooleanField(default=False)

    left = models.BooleanField(default=False)

    right = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ArticleCategory(models.Model):
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name'),
    )

    name_ru = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name Ru'),
    )

    slug = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Slug'),
        help_text="Don't touch it!"
    )

    photo = models.ImageField(verbose_name='Photo', null=True, blank=True)

    def __str__(self):
        return self.name


class Article(BaseModel):
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name'),
    )

    name_ru = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Name Ru'),
    )

    slug = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Slug'),
        help_text="Don't touch it!"
    )

    category = models.ForeignKey(ArticleCategory,
                                 null=True,
                                 on_delete=models.CASCADE,
                                 verbose_name=_('Category'),
                                 )

    description = models.TextField(
        max_length=2000,
        verbose_name=_('Description'),
        blank=True,
        null=True,
    )

    description_ru = models.TextField(
        max_length=2000,
        verbose_name=_('Description Ru'),
        blank=True,
        null=True,
    )

    main_text = models.TextField(
        max_length=2000,
        verbose_name=_('Main Text'),
        blank=True,
        null=True,
    )

    main_text_ru = models.TextField(
        max_length=2000,
        verbose_name=_('Main Text Ru'),
        blank=True,
        null=True,
    )

    photo_one = models.ImageField(verbose_name='Photo One', null=True, blank=True)

    photo_two = models.ImageField(verbose_name='Photo Two', null=True, blank=True)

    photo_three = models.ImageField(verbose_name='Photo Three', null=True, blank=True)

    photo_four = models.ImageField(verbose_name='Photo Four', null=True, blank=True)

    photo_five = models.ImageField(verbose_name='Photo Five', null=True, blank=True)

    main_page = models.URLField(verbose_name=_('Main Page'), blank=True, null=True)

    def __str__(self):
        return self.name


class Help(BaseModel):
    name = models.CharField(
        max_length=64,
        null=True,
        verbose_name=_('Name'),
    )

    email = models.CharField(
        max_length=64,
        null=True,
        verbose_name=_('Email'),
    )

    message = models.TextField(
        max_length=2000,
        verbose_name=_('Description'),
        null=True,
    )

    def __str__(self):
        return self.name


class Tokens(models.Model):
    name = models.CharField(
        max_length=64,
        null=True,
        verbose_name=_('Name'),
    )

    name_ru = models.CharField(
        max_length=64,
        null=True,
        verbose_name=_('Name Ru'),
    )

    description = models.CharField(
        max_length=256,
        null=True,
        verbose_name=_('Description'),
    )

    price = models.IntegerField(verbose_name=_('price'), null=True)

    def __str__(self):
        return self.name
