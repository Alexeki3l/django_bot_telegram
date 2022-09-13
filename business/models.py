from django.db import models
from django.contrib.auth.models import User

from user.models import Profile

# Create your models here.

class BusinessType(models.Model):
    name    = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Business(models.Model):
    name        = models.CharField(max_length=150)
    description = models.TextField(max_length=500,null=True,blank=True)
    address     = models.CharField(max_length=300,null=True,blank=True)
    manager     = models.ForeignKey(Profile, on_delete=models.CASCADE)
    types       = models.ManyToManyField(BusinessType, blank=True, related_name='categorias_tienda')
    open        = models.BooleanField(default=True)
    # likes       = models.ManyToManyField(User, null=True, blank=True, related_name='tienda_likes' )
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name    = "business"
        verbose_name_plural = "business"
        ordering = ['-created']

    def __str__(self):
        return self.name

class Product(models.Model):
    name            = models.CharField(max_length=255)
    price           = models.FloatField()
    old_price       = models.FloatField(blank=True, null=True)
    description     = models.TextField(max_length=1000, null=True, blank=True)
    business        = models.ForeignKey(Business, null=True, blank=True, on_delete=models.CASCADE)
    quantity        = models.IntegerField()
    sell            = models.BooleanField(default= True)
    # categorias      = models.ManyToManyField(CategoriaProducto, related_name='categorias_p')
    # likes           = models.ManyToManyField(User, null=True, blank=True, related_name='producto_likes' )
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name    = "product"
        verbose_name_plural = "products"
        ordering = ['-created']

    def __str__(self):
        return self.name

