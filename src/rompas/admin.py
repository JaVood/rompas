from django.contrib import admin
from rompas import models
from rompas import forms
from django.urls import reverse
from django.utils.html import format_html


@admin.register(models.MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    form = forms.MainCategoryForm


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    form = forms.SubscriptionForm


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = forms.ProfileForm


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    form = forms.CategoryForm


@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    form = forms.SubCategoryForm


@admin.register(models.Tokens)
class TokensAdmin(admin.ModelAdmin):
    form = forms.TokensForm


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    form = forms.ProductForm
    search_fields = ('name',)


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    form = forms.ImageForm
    raw_id_fields = ("product",)
    search_fields = ('product__name',)


@admin.register(models.BuyHistory)
class BuyHistoryAdmin(admin.ModelAdmin):
    form = forms.BuyHistoryForm


@admin.register(models.PagesPhoto)
class PagesPhotoAdmin(admin.ModelAdmin):
    form = forms.PagesPhotoForm


@admin.register(models.ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    form = forms.ArticleCategoryForm


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    form = forms.ArticleForm


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    form = forms.CurrencyForm


@admin.register(models.Help)
class HelpAdmin(admin.ModelAdmin):
    form = forms.HelpForm
