from django.contrib import admin
from business.models import Product, Business, BusinessType
# Register your models here.
from django import forms
from django.utils.html import format_html


class ContentModelForm( forms.ModelForm ):
    # Que el charfield "contenido" se comporte como un textarea
    description = forms.CharField( widget=forms.Textarea )

class BusinessAdmin(admin.ModelAdmin):
    form = ContentModelForm
    list_display = ('name','manager','description','address','open',)
    readonly_fields  = ("created", "updated",)

    # def img(self,obj):
    #     return format_html('<img src={} width="130" height="100" />',obj.imagen1.url )


class ProductAdmin(admin.ModelAdmin):
    form = ContentModelForm
    list_display = ('name','price','old_price','description','business','quantity','sell',)
    readonly_fields  = ("created", "updated",)

    # def img(self,obj):
    #     return format_html('<img src={} width="130" height="100" />',obj.image1.url )

admin.site.register(Business,BusinessAdmin)
admin.site.register(Product,ProductAdmin)