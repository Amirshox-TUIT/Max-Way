from django.db import models
from django.utils.translation import gettext_lazy as _


class TelegramUser(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('uz', 'O\'zbekcha'),
        ('ru', 'Русский'),
    ]

    user_id = models.BigIntegerField(unique=True, db_index=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    language_code = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'telegram_users'

    def __str__(self):
        return f"{self.user_id} - {self.first_name or 'No name'}"


class Branch(models.Model):
    title = models.CharField(max_length=128)
    location = models.TextField()
    target = models.CharField(max_length=255)
    working_hours = models.CharField(max_length=16)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'branch'
        verbose_name_plural = 'branches'


class Categories(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class City(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'city'
        verbose_name = _('shahar')
        verbose_name_plural = _('shaharlar')

