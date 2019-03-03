from django.db import models

# Create your models here.
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, mobile_number=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, first_name=None, last_name=None, mobile_number=None, password=None):
        user = self.create_user(
                email,
                first_name=first_name,
                last_name=last_name,
                mobile_number=mobile_number,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, email, first_name=None, last_name=None, mobile_number=None, password=None):
        user = self.create_user(
                email,
                first_name=first_name,
                last_name=last_name,
                mobile_number=mobile_number,
                password=password,
                is_staff=True,
                is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email         = models.EmailField(max_length=255, unique=True)
    first_name    = models.CharField(max_length=255, blank=True, null=True)
    last_name     = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    active        = models.BooleanField(default=True) # can login 
    staff         = models.BooleanField(default=False) # staff user non superuser
    admin         = models.BooleanField(default=False) # superuser 
    timestamp     = models.DateTimeField(auto_now_add=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email' #username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile_number'] #['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email


    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_mobile_number(self):
        if self.mobile_number:
            return self.mobile_number
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class GuestEmail(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email