from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from QrCoder import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'QrCode', views.QrCodeViewSet, basename='QrCode')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('QrCodeImageStorage/<str:image_name>/', views.serve_qr_code_image, name='serve_qr_code_image')
]