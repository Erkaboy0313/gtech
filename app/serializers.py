from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Client,Product,Catalog,Category,SubCategory,AboutUs,Photos
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
import base64
from django.core.files.base import ContentFile
        
class PhotoSerializer(ModelSerializer):
    
    photo = serializers.CharField(required = False)
    image = serializers.FileField(read_only = True)
    
    class Meta:
        model = Photos
        fields = '__all__'
        
    def create(self, validated_data):
        image_data = validated_data.pop('photo')
        format, datastr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        image_decoded = base64.b64decode(datastr)
        validated_data['image'] = ContentFile(image_decoded, name=f'image.{ext}')
        return super().create(validated_data)
        
class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model = Product)
    images = PhotoSerializer(read_only = True,many=True)
    photos = serializers.ListField(child = serializers.CharField(),write_only = True,required=False)
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def create(self, validated_data):
        photos = validated_data.pop('photos',[])
        product = super().create(validated_data)

        def to_file(base_image_data):
            
            format, datastr = base_image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_decoded = base64.b64decode(datastr)
            return ContentFile(image_decoded, name=f'image.{ext}')
       
        photo_ojects = [Photos(image = to_file(data)) for data in photos]

        if photo_ojects:
            created_photos = Photos.objects.bulk_create(photo_ojects)
            product.images.add(*created_photos)
        return product
    
class ClientSerializer(ModelSerializer):
    product = ProductSerializer(read_only = True)
    
    class Meta:
        model = Client
        fields = "__all__"
    
class CatalogSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model = Catalog)
    photo = serializers.CharField(required = False)
    image = serializers.FileField(read_only = True)
    
    class Meta:
        model = Catalog
        fields = "__all__" 
        
    def create(self, validated_data):
        image_data = validated_data.pop('photo')
        format, datastr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        image_decoded = base64.b64decode(datastr)
        validated_data['image'] = ContentFile(image_decoded, name=f'image.{ext}')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        image_data = validated_data.pop('photo',"")
        if image_data:
            format, datastr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_decoded = base64.b64decode(datastr)
            instance.image = ContentFile(image_decoded, name=f'image.{ext}')
            instance.save()
        return super().update(instance, validated_data)
        
class CategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model = Category)
    class Meta:
        model = Category
        fields = "__all__" 
        
class SubCategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model = SubCategory)
    class Meta:
        model = SubCategory
        fields = "__all__" 
        
class AboutUsSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model = AboutUs)
    photo = serializers.CharField(required = False)
    image = serializers.FileField(read_only = True)
    
    class Meta:
        model = AboutUs
        fields = "__all__" 
        
    def create(self, validated_data):
        image_data = validated_data.pop('photo')
        format, datastr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        image_decoded = base64.b64decode(datastr)
        validated_data['image'] = ContentFile(image_decoded, name=f'image.{ext}')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        image_data = validated_data.pop('photo',"")
        if image_data:
            format, datastr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_decoded = base64.b64decode(datastr)
            instance.image = ContentFile(image_decoded, name=f'image.{ext}')
            instance.save()
        return super().update(instance, validated_data)
        
class HomeSeriaizer(serializers.Serializer):
    client = serializers.IntegerField()
    product = serializers.IntegerField()
    partner = serializers.IntegerField()
    catalog = serializers.IntegerField()
     