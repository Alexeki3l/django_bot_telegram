from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Trabajo con señales
from django.db.models.signals import post_save

# Create your models here.
class TypeProfile(models.Model):
    name  = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name    = "typeprofile"
        verbose_name_plural = "typeprofiles"
        ordering = ['-created']

    def __str__(self):
        return self.nombre

class Profile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # type         = models.Choices
    bio          = models.TextField(null=True, blank=True)
    phone        = models.CharField(max_length=15, null=True, blank=True)
    address      = models.TextField(null=True, blank=True)
    location     = models.TextField(null=True, blank=True)
    chat_id      = models.IntegerField(null=True, blank=True)
    created      = models.DateTimeField(auto_now_add=True)
    updated      = models.DateTimeField(auto_now=True)        

    class Meta:
        verbose_name    = "profile"
        verbose_name_plural = "profiles"
        
    def __str__(self):
        return self.user.username

    # def image_url(self):
    #     if self.imagen and hasattr(self.imagen, 'url'):
    #         return self.imagen.url

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

post_save.connect(create_profile, sender = User)