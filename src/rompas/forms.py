from django import forms
from rompas import models
from transliterate.exceptions import LanguageDetectionError
import re
from transliterate import translit
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def transliterate(text):
    pieces = str(re.sub('[\W]+', ' ', text)).lower().split(' ')
    result = []

    for piece in pieces:
        try:
            result.append(translit(piece, reversed=True))
        except LanguageDetectionError:
            result.append(piece)
    return '-'.join([r for r in result if r])


class MainCategoryForm(forms.ModelForm):
    def clean_slug(self):
        return transliterate(self.cleaned_data['name'])

    class Meta:
        model = models.MainCategory
        fields = '__all__'


class SubscriptionForm(forms.ModelForm):
    def clean_slug(self):
        return transliterate(self.cleaned_data['name'])

    class Meta:
        model = models.Subscription
        fields = '__all__'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    def clean_slug(self):
        return transliterate(self.cleaned_data['name'])

    class Meta:
        model = models.Category
        fields = '__all__'


class SubCategoryForm(forms.ModelForm):
    def clean_slug(self):
        return transliterate(self.cleaned_data['name'])

    class Meta:
        model = models.SubCategory
        fields = '__all__'


class ProductForm(forms.ModelForm):
    def clean_slug(self):
        return transliterate(self.cleaned_data['name'])

    class Meta:
        model = models.Product
        fields = '__all__'


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Image
        fields = '__all__'


class TokensForm(forms.ModelForm):
    class Meta:
        model = models.Tokens
        fields = '__all__'


class BuyHistoryForm(forms.ModelForm):
    class Meta:
        model = models.BuyHistory
        fields = '__all__'


class PagesPhotoForm(forms.ModelForm):
    class Meta:
        model = models.PagesPhoto
        fields = '__all__'


class ArticleCategoryForm(forms.ModelForm):
    def clean_slug(self):
        return transliterate(self.cleaned_data['name'])

    class Meta:
        model = models.ArticleCategory
        fields = '__all__'


class ArticleForm(forms.ModelForm):
    def clean_slug(self):
        return transliterate(self.cleaned_data['name'])

    class Meta:
        model = models.Article
        fields = '__all__'


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = models.Currency
        fields = '__all__'


class SignUpForm(forms.Form):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Name'}), min_length=3, max_length=150)
    email = forms.EmailField(widget=TextInput(attrs={'placeholder': 'Email'}), max_length=254)
    password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}), min_length=6)
    password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Confirm password'}), min_length=6)
    subscription = forms.ModelChoiceField(queryset=models.Subscription.objects.all())

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'subscription')


class EmailChangeForm(forms.Form):
    email = forms.EmailField(widget=TextInput(attrs={'placeholder': 'Email'}), max_length=254)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    class Meta:
        model = User
        fields = ['email']


class EmailSubscription(forms.Form):
    subscription = forms.BooleanField(required=False,
                                      initial=False,
                                      )


class HelpForm(forms.ModelForm):
    class Meta:
        model = models.Help
        fields = '__all__'


class BuyProductForm(forms.Form):
    buy = forms.BooleanField(required=True, initial=True,)


TOKENS_CHOICES = (
    (1, _("50 tokens - 5$")),
    (2, _("200 tokens - 18$")),
    (3, _("500 tokens - 40$")),
    (4, _("1000 tokens - 70$")),
    (5, _("2500 tokens - 150$"))
)


class AddTokensForm(forms.Form):
    tokens = forms.ChoiceField(choices=TOKENS_CHOICES)
