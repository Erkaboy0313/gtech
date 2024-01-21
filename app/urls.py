from rest_framework.routers import DefaultRouter
from .views import ClientView,PhotoView,ProductView,CatalogView,\
    CategoryView,SubCategoryView,AboutUsView,LoginView,ResetPassword,HomeView
from django.urls import path,include
router = DefaultRouter()


router.register(r'home',HomeView,basename='home')
router.register(r'client',ClientView,basename='client')
router.register(r'photo',PhotoView,basename='photo')
router.register(r'product',ProductView,basename='product')
router.register(r'catalog',CatalogView,basename='catalog')
router.register(r'category',CategoryView,basename='category')
router.register(r'subcategory',SubCategoryView,basename='subcategory')
router.register(r'about-us',AboutUsView,basename='about-us')

router.register(r'login',LoginView,basename='login')
router.register(r'reset-password',ResetPassword,basename='reset-password')

urlpatterns = [
    path('', include(router.urls)),
]
