from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Client,Product,Catalog,Category,SubCategory,AboutUs,Photos
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

        
class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__'
        
class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model = Product)
    images = PhotoSerializer(read_only = True,many=True)
    photos = serializers.ListField(child = PhotoSerializer(),write_only = True,required=False)
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def create(self, validated_data):
        photos = validated_data.pop('photos',[])
        product = super().create(validated_data)
        photo_ojects = [Photos(**data) for data in photos]
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
    
    image = serializers.CharField(required = False)
    class Meta:
        model = Catalog
        fields = "__all__" 
        
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
    class Meta:
        model = AboutUs
        fields = "__all__" 
        
class HomeSeriaizer(serializers.Serializer):
    client = serializers.IntegerField()
    product = serializers.IntegerField()
    partner = serializers.IntegerField()
    catalog = serializers.IntegerField()