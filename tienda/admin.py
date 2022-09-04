from django.contrib import admin
from tienda.models import Producto, Tienda
# Register your models here.
from django import forms
from django.utils.html import format_html


class ContenidoModelForm( forms.ModelForm ):
    # Que el charfield "contenido" se comporte como un textarea
    descripcion = forms.CharField( widget=forms.Textarea )

class TiendaAdmin(admin.ModelAdmin):
    form = ContenidoModelForm
    list_display = ('img','nombre','encargado','descripcion','direccion','open',)
    readonly_fields  = ("created", "updated",)

    def img(self,obj):
        return format_html('<img src={} width="130" height="100" />',obj.imagen1.url )


class ProductoAdmin(admin.ModelAdmin):
    form = ContenidoModelForm
    list_display = ('img','nombre','precio','precio_old','descripcion','tienda','cantidad','vender',)
    readonly_fields  = ("created", "updated",)

    def img(self,obj):
        return format_html('<img src={} width="130" height="100" />',obj.image1.url )

admin.site.register(Tienda,TiendaAdmin)
admin.site.register(Producto,ProductoAdmin)