from django.contrib import admin
from django import forms
from django.utils.html import format_html

from user.models import Profile, TypeProfile
from multimedia.models import Multimedia

# Register your models here.
class ContenidoModelForm( forms.ModelForm ):
    # Que el charfield "contenido" se comporte como un textarea
    bio = forms.CharField( widget=forms.Textarea )
    

class ProfileAdmin(admin.ModelAdmin):
    
    form = ContenidoModelForm
    ordering    =   ('-updated',)
    list_display = ('user','chat_id','bio','phone','address','location', )
    readonly_fields  = ("created", "updated",)

    # def img(self,obj):
        
    #     return format_html('<img src={} width="130" height="100" />',)


class TypeProfileAdmin(admin.ModelAdmin):
    list_display = ('name','created','updated',)
    readonly_fields  = ("created", "updated",)

admin.site.register(TypeProfile,TypeProfileAdmin)
admin.site.register(Profile,ProfileAdmin)