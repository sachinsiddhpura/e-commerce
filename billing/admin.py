from django.contrib import admin

# Register your models here.
from .models import BillingProfile,Charge

admin.site.register(BillingProfile)
admin.site.register(Charge)