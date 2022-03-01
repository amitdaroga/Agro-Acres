"""myproject URL Configuration

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
from admin_app import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('admin_profile/',views.admin_profile,name='admin_profile'),
    path('editprofile_admin/',views.editprofile_admin,name='editprofile_admin'),
    path('editimg_admin/',views.editimg_admin,name="editimg_admin"),
    path('alluser_detail/',views.alluser_detail,name="alluser_detail"),
    path('edituser_detail/<int:pk>',views.edituser_detail,name="edituser_detail"),
    path('updateuser_details/',views.updateuser_details,name="updateuser_details"),
    path('removeuser_details/<int:pk>',views.removeuser_details,name="removeuser_details"),
    path('allproduct_detail/<int:pk>',views.allproduct_detail,name="allproduct_detail"),
    

]
