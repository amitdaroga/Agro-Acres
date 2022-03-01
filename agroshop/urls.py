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
from agroshop import views

urlpatterns = [
    path('index_a/',views.index_a,name='index_a'),
    path('profile_a/',views.profile_a,name='profile_a'),
    path('edit_profile_a/',views.edit_profile_a,name='edit_profile_a'),
    path('upload_product_a/',views.upload_product_a,name='upload_product_a'),
    path('my_product_a/',views.my_product_a,name='my_product_a'),
    path('productdetails_a/<int:pk>',views.productdetails_a,name='productdetails_a'),
    path('update_product_a',views.update_product_a,name='update_product_a'),
    path('edit_img_a/',views.edit_img_a,name="edit_img_a"),
    path('myorder_a/',views.myorder_a,name="myorder_a"),
]
