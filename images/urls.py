from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

app_name = "images"

urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.registration, name='userRegistration'),
    path('login/', views.userLogin, name='userlogin'),
    path('userprofile/', views.userProfile, name='userprofile'),
    path('login/imageupload/', views.imageUpload, name='imageupload'),
    path('images/', views.uploadedImages, name='images'),
]