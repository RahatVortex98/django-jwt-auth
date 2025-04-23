from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import UserManager


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]

    objects = UserManager()


    def __str__(self):
        return self.get_full_name()
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class OneTimePassword(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=6,unique=True)

    def __str__(self):
        return f"{self.user.first_name}--passcode"
    