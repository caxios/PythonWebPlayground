from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django_countries.fields import CountryField
from django.core.mail import send_mail

# Translate in accordance with user's local machine's default language.
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):
        
        """
        Q: What is '**other_fields'? And what is 'setdefault'?
        A: It is just renamed version of '**kwargs'. '**kwargs'(where kwargs is just a conventional
           name, and we're using 'other_fields' instead) captures any additional keyword arguments
           passed to the method that are not explicitly listed in the method's signature.
           These arguments are stored in a dictionary (in this case, 'other_fields'), where the 
           keys are the argument names and the values are the argument values.
           And as its name suggest 'setdefault' method of dictionary sets default values for 
           value of specified key. In this case, 'is_staff' key is gonna have default value of 
           True(boolean). 
           In this case, when we creating superuser, then we might use this function something like 
           this in some other file, where we are making superuser : 
           custom_user_manager.create_superuser(
                email="superuser@example.com",
                user_name="superuser",
                password="superpassword",
                is_staff=True,
                is_superuser=True,
                is_active=True
                )
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be is_staff True')
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be is_superuser True')

        return self.create_user(email, user_name, password, **other_fields)
    
    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError('Must provide email')
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        
        # 'set_password' is a method of 'AbstractBaseUser'. It creates hashed password, 
        # and not automatically saved to database.
        user.set_password(password)
        
        # Need to explicitly call 'save' method to save any modifications on model instance.
        user.save()
        
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(_('about'), max_length=500, blank=True)
    # Delivery details
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    """
    Q: What is purpose of 'objects = CustomAccountManager()'?
    A: When explicitly add this code when making model, then django replaces the default
       model manager instance with given manager instance(class). So if we want to use 
       custom model manager then, we have to set it like this. Similar thing in store/models.py's
       'Product' model class. Every django model has at least one model manager, and this is provided
       variable named 'objects'. And we are now overriding it with our custom model manager, since 
       we need our own behavior for this model.
    """
    objects = CustomAccountManager()

    # Fields that are required when making user account(?)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"\

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.user_name