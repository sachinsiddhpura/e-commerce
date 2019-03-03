from django.urls import path
from .views import AccountHomeView,UserDetailUpdateView
from products.views import UserProductHistoryView
app_name = 'account'

urlpatterns = [
    path('', AccountHomeView.as_view(), name='home'),
    path('details/', UserDetailUpdateView.as_view(), name='user-update'),
    path('history/products/', UserProductHistoryView.as_view(), name='user-product-history'),
]

