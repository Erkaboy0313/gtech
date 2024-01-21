from django.db import models
from parler.models import TranslatableModel, TranslatedFields
# Create your models here.


class Client(models.Model):
    first_name = models.CharField(max_length = 150,blank=True, null=True)
    last_name = models.CharField(max_length = 150,blank=True, null=True)
    phone = models.CharField(max_length = 150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey('Product',on_delete=models.SET_NULL,null = True)
    checked = models.BooleanField(default = False)
    time = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} | {self.last_name} -- "

class Product(TranslatableModel):
    subcategory = models.ForeignKey('SubCategory',on_delete=models.CASCADE,blank=True, null=True)
    translations = TranslatedFields(
        name = models.CharField(max_length = 100, blank=True, null=True),
        description = models.TextField()
    )
    price = models.CharField(max_length = 30)
    images = models.ManyToManyField('Photos')
    main = models.BooleanField(default = False)

class Catalog(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length = 100, blank=True, null=True),
        description = models.TextField()
    )
    image = models.TextField()

class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length = 100, blank=True, null=True),
    )

class SubCategory(TranslatableModel):
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    translations = TranslatedFields(
        name = models.CharField(max_length = 100, blank=True, null=True),
    )

class AboutUs(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length = 100, blank=True, null=True),
        description = models.TextField()
    )
    image = models.TextField()

    class Meta:
        verbose_name_plural = 'About Us'

class Photos(models.Model):
    
    class Photo_type(models.TextChoices):
        PRODUCT = 'product'
        PARTNER = 'partner'
        MOBILE = 'mobile'
        MAIN = 'main'
    
    image_type = models.CharField(max_length = 8,choices = Photo_type.choices, default = Photo_type.PRODUCT)
    image = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Photos'
    