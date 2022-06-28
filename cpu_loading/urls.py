"""cpu_loading URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from cpu_ldng import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='gohome'),
    path('start/', views.start, name='start'),
    path('stop/', views.stop, name='stop'),
    path('reset/', views.reset, name='reset'),
    path('create_fig/', views.create_fig, name='create_fig'),
    path('send_fig/', views.send_fig, name='send_fig'),

]
