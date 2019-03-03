from django.urls import path
from .views import cart_home,cart_update,checkout_home,checkout_handle_view,checkout_done_view
app_name = 'carts'

urlpatterns = [
    path('', cart_home, name='home'),
    path('response/', checkout_handle_view, name='response'),
    path('checkout/success/', checkout_done_view, name='success'),
    path('checkout/', checkout_home, name='checkout'),
    path('update/', cart_update, name='update'),
]

