from django.contrib import admin
from .models import Client,Product,Catalog,Category,SubCategory,AboutUs,Photos
# Register your models here.
from parler.admin import TranslatableAdmin

@admin.register(AboutUs)
class AboutUsAdmin(TranslatableAdmin):
    list_display = ('name',)


@admin.register(Client)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','phone','checked')

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ('subcategory','name')
    
@admin.register(Catalog)
class CatalogAdmin(TranslatableAdmin):
    list_display = ('name',)
    
@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('name',)
    
@admin.register(SubCategory)
class SubCategoryAdmin(TranslatableAdmin):
    list_display = ('name',)
    
@admin.register(Photos)
class PhotosAdmin(TranslatableAdmin):
    list_display = ('image_type',)
