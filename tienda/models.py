from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tienda(models.Model):
    nombre      = models.CharField(max_length=150)
    descripcion = models.TextField()
    direccion   = models.CharField(max_length=300)
    encargado   = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen1      = models.ImageField(upload_to='tienda')
    imagen2      = models.ImageField(upload_to='tienda')
    imagen3      = models.ImageField(upload_to='tienda')
    # categorias  = models.ManyToManyField(CategoriaTienda, null=True, blank=True, related_name='categorias_tienda')
    open        = models.BooleanField(default=True)
    # likes       = models.ManyToManyField(User, null=True, blank=True, related_name='tienda_likes' )
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name    = "tienda"
        verbose_name_plural = "tiendas"
        ordering = ['-created']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre          = models.CharField(max_length=255)
    precio          = models.FloatField()
    precio_old      = models.FloatField(blank=True, null=True)
    descripcion     = models.TextField(max_length=1000, null=True, blank=True)
    image1          = models.ImageField(upload_to='producto')
    image2          = models.ImageField(upload_to='producto')
    image3          = models.ImageField(upload_to='producto')
    tienda          = models.ForeignKey(Tienda, null=True, blank=True, on_delete=models.CASCADE)
    cantidad        = models.IntegerField()
    vender          = models.BooleanField(default= True)
    # categorias      = models.ManyToManyField(CategoriaProducto, related_name='categorias_p')
    # likes           = models.ManyToManyField(User, null=True, blank=True, related_name='producto_likes' )
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name    = "producto"
        verbose_name_plural = "productos"
        ordering = ['-created']
