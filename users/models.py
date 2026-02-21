from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Укажите email')
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='Телефон', help_text='Укажите телефон')
    city = models.CharField(verbose_name='Город', help_text='Укажите город')
    avatar = models.ImageField(upload_to='users/avatars', blank=True, null=True, verbose_name='Аватар', help_text='Загрузите аватарку')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ ]