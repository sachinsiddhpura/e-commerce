"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.conf import settings
from .views import home_page,about_page,contact_page
from accounts.views import guest_register_view,LoginView,register
from django.contrib.auth.views import LogoutView
from addresses.views import checkout_address_create_view,checkout_address_reuse_view,AddressListView,AddressCreateView,AddressUpdateView
from django.contrib.auth import views as auth_views
from orders.views import LibraryView
from custom.views import index

urlpatterns = [
    path('progress/', index, name='progress'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   # path('', views.dashboard, name='dashboard'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('library/', LibraryView.as_view(), name='library'),
    path('addresses/', AddressListView.as_view(), name='addresses'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    re_path(r'^addresses/(?P<pk>\d+)/$', AddressUpdateView.as_view(), name='address-update'),

    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('register/guest/', guest_register_view, name='guest_register'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    #path('login/', LoginView.as_view(), name='login'),
    path('register/', register, name='register'),

    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),

    path('products/',include('products.urls',namespace='products')),
    path('cart/',include('carts.urls',namespace='cart')),
    path('orders/',include('orders.urls',namespace='orders')),
    path('account/',include('accounts.urls',namespace='account')),
    path('search/',include('search.urls',namespace='search')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)