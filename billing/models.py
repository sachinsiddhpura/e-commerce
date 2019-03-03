from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

from accounts.models import GuestEmail
import juspayp3

User = settings.AUTH_USER_MODEL

# abc@teamcfe.com -->> 1000000 billing profiles
# user abc@teamcfe.com -- 1 billing profile

# juspayp3.api_key = 'D304CC61928C4E67A6519D2CD4639D51'
# juspayp3.environment = 'sandbox'
juspayp3.api_key = settings.JUSPAY_API_KEY
juspayp3.environment = settings.JUSPAY_ENV


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            'logged in user checkout; remember payment stuff'
            obj, created = BillingProfile.objects.get_or_create(
                            user=user, 
                            email=user.email,
                            first_name=str(user.first_name),
                            last_name=str(user.last_name),
                            
                            )
            print(obj, created)
        elif guest_email_id is not None:
            'guest user checkout; auto reloads payment stuff'
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                                            email=guest_email_obj.email)
        else:
            pass
        return obj, created

class BillingProfile(models.Model):
    user          = models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE)
    email         = models.EmailField()
    first_name    = models.CharField(max_length=255, blank=True, null=True)
    last_name     = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], blank=True, null=True)
    active        = models.BooleanField(default=True)
    update        = models.DateTimeField(auto_now=True)
    timestamp     = models.DateTimeField(auto_now_add=True)
    customer_id   = models.CharField(max_length=120, null=True, blank=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

    def charge(self, order_obj):
        return Charge.objects.do(self, order_obj)

def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        # print("ACTUAL API REQUEST Send to stripe/braintree")
        customer = juspayp3.Customers.create(
                    object_reference_id = instance.email, 
                    mobile_number = instance.mobile_number,
                    email_address = instance.email,
                    first_name = instance.first_name,
                    last_name = instance.last_name,
                    mobile_country_code = '91'
            )
        # print(vars(customer))
        instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, 
                                             email=instance.email,
                                             first_name = instance.first_name,
                                             last_name = instance.last_name,
                                             mobile_number = instance.mobile_number,
                                             )

post_save.connect(user_created_receiver, sender=User)

class ChargeManager(models.Manager):
    def do(self, billing_profile, order_obj):
        pass
        # c = juspayp3.Orders.create(
        #     order_id=order_obj.order_id,
        #     amount=order_obj.total,
        #     customer_id=billing_profile.customer_id,
        #     customer_email=billing_profile.email,
        #     customer_phone='9988665522',
        #     return_url='http://127.0.0.1:8910/cart/checkout/success/'
        # )
        # new_charge_obj = self.model(
        #         billing_profile = billing_profile,
        #         customer_id = c.id,
        #         order_id = c.order_id,
        #         status = c.status,
        #         status_id = c.status_id,

        #     )
        # print(vars(c))
        # return c.payment_links

class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    order_id        = models.CharField(max_length=120)
    status          = models.CharField(max_length=120)
    signature       = models.CharField(max_length=120)
    signature_algorithm = models.CharField(max_length=120)

    objects = ChargeManager()
