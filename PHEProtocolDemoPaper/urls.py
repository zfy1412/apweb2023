"""PHEProtocolDemoPaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
import app.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('example/', views.example),
    path('views/', views.views),
    path('knn/', views.knn),
    path('newindex/', views.newindex),
    path('newexample/', views.newexample),
    path('Advance/', views.advance),
    path('Basic/', views.basic),
    re_path(r'^dec', views.decryption),
    re_path(r'^cal$', views.calculation),
    re_path(r'^enc$', views.encryption),
    re_path(r'^gk$', views.generate_keypair),
    re_path(r'^$', views.newindex),

]
