from django.db import models

from user.models import Profile
from business.models import Business, Product

# Create your models here.

# class TypeMultimedia(models.Model):
#     name      = models.CharField(max_length=255)
#     created   = models.DateTimeField(auto_now_add=True)
#     updated   = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name        = "type_multimedia"
#         verbose_name_plural = "type_multimedias"
        
#     def __str__(self):
#         return self.name

class Multimedia(models.Model):
    # id          = models.AutoField(primary_key=True, unique=False, )
    name        = models.CharField(max_length=255, null=True, blank=True)
    file        = models.FileField()
    TYPE        = (('1', 'profile'), ('2', 'business'), ('3', 'product'),)
    type        = models.CharField(max_length=1, choices=TYPE)
    profiles    = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="multi_profiles")
    business    = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True, related_name="multi_business")
    products    = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name="multi_products")
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "multimedia"
        verbose_name_plural = "multimedias"
        
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.created:
            print("CREATE")
            if self.type == "1":
                self.business = None
                self.products = None

                self.name = self.file.url.split("/")[-1].split(".")[-2]
                return super().save(self,*args,**kwargs)

            elif self.type == "2":
                self.profiles = None
                self.products = None
                
                self.name = self.file.url.split("/")[-1].split(".")[-2]
                return super().save(self,*args,**kwargs)

            elif self.type == "3":
                self.business = None
                self.profiles = None

                self.name = self.file.url.split("/")[-1].split(".")[-2]
                return super().save(self,*args,**kwargs)
        else:
            print("UPDATED")
            if self.type == "1":
                self.business = None
                self.products = None

                self.name = self.file.url.split("/")[-1].split(".")[-2]
                return super(Multimedia,self).save(force_update=True)

            elif self.type == "2":
                self.profiles = None
                self.products = None
                
                self.name = self.file.url.split("/")[-1].split(".")[-2]
                return super(Multimedia,self).save(force_update=True)

            elif self.type == "3":
                self.business = None
                self.profiles = None
                self.name = self.file.url.split("/")[-1].split(".")[-2]
                return super(Multimedia,self).save(force_update=True)
        

        
        
        

    
    