from django.contrib import admin
from django import forms
from django.utils.html import format_html

from usuario.models import Profile, TipoPerfil

# Register your models here.
class ContenidoModelForm( forms.ModelForm ):
    # Que el charfield "contenido" se comporte como un textarea
    bio = forms.CharField( widget=forms.Textarea )
    

class ProfileAdmin(admin.ModelAdmin):
    
    form = ContenidoModelForm
    ordering    =   ('-updated',)
    list_display = ('img','user','chat_id','tipo','bio','telf','direccion','localizacion', )
    readonly_fields  = ("created", "updated",)

    def img(self,obj):
        return format_html('<img src={} width="130" height="100" />',obj.imagen.url )


class TipoPerfilAdmin(admin.ModelAdmin):
    list_display = ('nombre','created','updated',)
    readonly_fields  = ("created", "updated",)

admin.site.register(TipoPerfil,TipoPerfilAdmin)
admin.site.register(Profile,ProfileAdmin)