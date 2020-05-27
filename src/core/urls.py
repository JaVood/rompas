"""rompas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import LogoutView
from core.views import LoginRuView, PasswordRuResetView


admin.site.index_title = 'Rompas administration'


urlpatterns = [
    path('boss/', admin.site.urls),
    re_path(r'', include(('rompas.urls', 'rompas'), namespace='rompas')),
    url(r'^login/',
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name='login'),
    url(r'^ru/login/',
        LoginRuView.as_view(redirect_authenticated_user=True),
        name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout', ),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    re_path('^ru/accounts/password_reset/', PasswordRuResetView.as_view(), name='password_reset_ru'),
    url(r'^cart/', include(('cart.urls', 'cart'), namespace='cart')),
    url(r'^order/', include(('orders.urls', 'orders'), namespace='orders')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
admin.site.site_header = "Rompas Administration"
admin.site.site_title = "Rompas Admin Portal"
admin.site.index_title = "Rompas Administration"
