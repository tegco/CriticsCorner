from django.urls import include, path
from . import views

app_name ='review'

urlpatterns = [
 path("", views.index, name="index"),
 path('registaruser', views.registar_user, name='registar_user'),
 path('logoutview', views.logoutview, name='logoutview'),
 path('loginview', views.loginview, name='loginview'),
]

