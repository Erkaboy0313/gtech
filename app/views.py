from rest_framework.viewsets import ModelViewSet,ViewSet
from .serializers import ClientSerializer,PhotoSerializer,ProductSerializer,\
    CatalogSerializer,CategorySerializer,SubCategorySerializer,AboutUsSerializer,HomeSeriaizer
from .models import Client,Photos,Product,Catalog,Category,SubCategory,AboutUs
from rest_framework.permissions import IsAdminUser,AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
import base64
from django.core.files.base import ContentFile


class HomeView(ViewSet):
    
    def list(self,request):
        data = {
            'client':Client.objects.all().count(),
            'product':Product.objects.all().count(),
            'partner':Photos.objects.filter(image_type = 'partner').count(),
            'catalog':Catalog.objects.all().count()
        }
        serializer = HomeSeriaizer(data)
        return Response(serializer.data,HTTP_200_OK)

class ClientView(ModelViewSet):
    queryset = Client.objects.select_related('product').all()
    serializer_class = ClientSerializer
    http_method_names = ('get','post','patch','delete')
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            pr = Product.objects.get(id = request.data.get('product'))
            obj.product = pr
            obj.save()
            return Response('success',HTTP_200_OK)
        except:
            return Response('error',HTTP_400_BAD_REQUEST)
            
class PhotoView(ModelViewSet):
    queryset = Photos.objects.all()
    serializer_class = PhotoSerializer
    http_method_names = ('get','post','delete')
    
    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        return Response('Not implemented',HTTP_200_OK)
    
    @action(['get'],detail=False)
    def dashboard(self,request):
        photos = self.queryset.filter(image_type = "main")    
        serialzier = self.serializer_class(photos,many=True)
        return Response(serialzier.data,HTTP_200_OK)
    
    @action(['get'],detail=False)
    def partner(self,request):
        photos = self.queryset.filter(image_type = "partner")    
        serialzier = self.serializer_class(photos,many=True)
        return Response(serialzier.data,HTTP_200_OK)
    
    @action(['get'],detail=False)
    def mobile(self,request):
        photos = self.queryset.filter(image_type = "mobile")    
        serialzier = self.serializer_class(photos,many=True)
        return Response(serialzier.data,HTTP_200_OK)

class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get','post','put','delete']
    filter_backends = (SearchFilter,)
    search_fields = ['translations__name']
    
    def get_queryset(self):
        main = self.request.query_params.get('main',None)
        category = self.request.query_params.get('category',None)
        main_category = self.request.query_params.get('main-category',None)
        print(main_category)
        if main and main == 'true':
            return Product.objects.filter(main = True)
        elif category:
            return Product.objects.filter(subcategory__id = int(category))
        elif main_category:
            return Product.objects.filter(subcategory__category__id = int(main_category)).order_by('-main')
        else:
            return Product.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action =='retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(['post'],detail=True)
    def add_photo(self,request,*args,**kwargs):
        
        def to_file(base_image_data):
            
            format, datastr = base_image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_decoded = base64.b64decode(datastr)
            return ContentFile(image_decoded, name=f'image.{ext}')
        
        product = self.get_object()
        photos = request.data.get('photos',[])
        photo_ojects = [Photos(image = to_file(data)) for data in photos]
        
        if photo_ojects:
            created_photos = Photos.objects.bulk_create(photo_ojects)
            product.images.add(*created_photos)
        return super().list(request,*args,**kwargs)
            
class CatalogView(ModelViewSet):
    queryset  = Catalog.objects.all()
    serializer_class = CatalogSerializer
    http_method_names = ['get','post','patch','delete']
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get','post','put','delete']
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
class SubCategoryView(ModelViewSet):
    queryset = SubCategory.objects.select_related('category').all()
    serializer_class = SubCategorySerializer
    http_method_names = ['get','post','put','delete']
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
class AboutUsView(ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    http_method_names = ['get','post','patch','delete']
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class LoginView(ViewSet):
    permission_classes = (AllowAny,)

    def create(self,request,format=None):
        try:
            serializer=AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user=serializer.validated_data['user']
            token,created = Token.objects.get_or_create(user=user)
            if user.is_staff:
                data = {'token':token.key}
                return Response(data,status=HTTP_200_OK)
            else:
                return Response({'message':'user not found'},status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':'user not found'},status=HTTP_400_BAD_REQUEST)
        
class ResetPassword(ViewSet):
    permission_classes = (IsAdminUser,)
    
    def list(self,request):
        return Response('not implimented')
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.check_password(request.data.get('old_password')):
            return Response({"message":"error old password is not match"}, status=HTTP_400_BAD_REQUEST)
        password = request.data.get('new_password')
        user.set_password(password)
        user.save()
        return Response({'message':'password saved successfully'})

