from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



# Create your models here.

class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, password, *args, **kwargs):
        if not email:
            raise ValueError('User must have email address')
        if not username:
            raise ValueError('username must be entered')

        if not first_name:
            raise ValueError('first name must be entered')
        if not last_name:
            raise ValueError('last name must be entered')

        user = self.model(
            email= self.normalize_email(email),
            username= username,
            first_name=first_name,
            last_name= last_name
        )

        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, first_name, last_name, *args, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True) # login using E-mail, that why you need this to be unique
    username = models.CharField(max_length=30, unique=True)
    date_join = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(verbose_name='first name', max_length=50, unique=False)
    last_name = models.CharField(verbose_name='last name', max_length=50, unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_level):
        return True

