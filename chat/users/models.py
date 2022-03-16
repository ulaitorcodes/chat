from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import IntegerField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import random



################################################
#######                                 ########
#######    Core Model                   ########
#######                                 ########
################################################



from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone, password=None, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)




class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=240)
    username = None
    last_name = models.CharField(max_length=240)
    phone = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=240)
    lat = models.CharField(max_length=20)
    lon = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_delivery = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    is_active = models.BooleanField(('active'), default=False)
    avatar = models.ImageField(upload_to='media/avatars/', null=True)
    cover_photo = models.ImageField(
        upload_to='media/profile/cover_photo/', null=True)
    vendor = models.BooleanField(default=False)
    code = models.CharField(max_length=5, null= True, blank = True)

    # is_driver = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        number_list = [x for x in range(10)]
        code_items = []

        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)
            code_string = "".join(str(item) for item in code_items)
        profile = Profile.objects.create(user=instance)
        profile.code = code_string
        profile.phone = instance.phone
        profile.save()
        
        
        


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
