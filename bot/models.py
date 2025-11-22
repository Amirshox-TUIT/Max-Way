from django.db import models

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
