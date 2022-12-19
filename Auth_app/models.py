from django.db import models

# To create a custom user modeland custom user panel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from django.dispatch import receiver
from django.db.models.signals import post_save


class MyUserManager(BaseUserManager):
    # a custom user deal with email and uniqe field
    def _create_user(self, email, password, **Others_field):
        # create user with given his email and password
        if not email:
            raise ValueError('Email must be set!')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **Others_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **Others_field):
        Others_field.setdefault('is_staff', True)
        Others_field.setdefault('is_superuser', True)
        Others_field.setdefault('is_active', True)

        # if Others_field.get('is_satff') is not True:
        #     raise ValueError('superuser must have is_staff True')
        
        # if Others_field.get('is_superuser') is not True:
        #     raise ValueError('superuser must have is_useruser True')
        return self._create_user(email, password, **Others_field)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        gettext_lazy('staff'),
        default = False,
        help_text = gettext_lazy('Designetes whether the user can log in this site')
    )

    is_active = models.BooleanField(
        gettext_lazy('active'),
        default = True,
        help_text = gettext_lazy('Designetes whether the user should be created as active. Ulselect insted of deleting accounts')
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self) -> str:
        return self.email

    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email
 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=264, blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    address_1 = models.TextField(max_length=300, blank=True)
    city = models.CharField(max_length=40, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.user) + "'s Profile"


    # chack user Preofile fully filed or Not

    def is_fully_filed(self):
        # all field name stor in fields_name
        fields_name=[f.name for f in self._meta.get_fields()] 
        for field_name in fields_name:
            value = getattr(self, field_name)
            if value is None or value=='':
                return False
        return True

@receiver(post_save, sender=User)
def create_profile(sender,instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()