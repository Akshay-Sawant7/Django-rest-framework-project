from django.db import models
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
# from django.dispatch import receiver
# from django.db.models.signals import post_save
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, username, password, address):
        if not email:
            raise ValueError("user must have an email address!")
        if not username:
            raise ValueError("user must have their username!")
        if not address:
            raise ValueError("user must have a address!")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            address = address
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, username, password, address):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            address=address,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserRegister(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'address']

    def __str__(self):
        return self.email