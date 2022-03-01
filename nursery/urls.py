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
from os import name
from django.contrib import admin
from django.urls import path
from nursery import views

urlpatterns = [
    path('index_n/',views.index_n,name='index_n'),
    path('profile_n/',views.profile_n,name='profile_n'),
    path('edit_profile_n/',views.edit_profile_n,name='edit_profile_n'),
    path('upload_product_n/',views.upload_product_n,name='upload_product_n'),
    path('my_product_n/',views.my_product_n,name='my_product_n'),
    path('productdetails_n/<int:pk>',views.productdetails_n,name='productdetails_n'),
    path('update_product_n/',views.update_product_n,name='update_product_n'),
    path('gallery_n/',views.gallery_n,name='gallery_n'),
    path('p_details_n/<int:pk>',views.p_details_n,name='p_details_n'),
    path('addtocart_n/<int:pk>',views.addtocart_n,name='addtocart_n'),
    path('addtodetails_n/',views.addtodetails_n,name='addtodetails_n'),
    path('delete_record_n/<int:pk>',views.delete_record_n,name="delete_record_n"),
    path('edit_img_n',views.edit_img_n,name="edit_img_n"),
    path('wishlist_n/<int:pk>',views.wishlist_n,name="wishlist_n"),
    path('wdetails_n/',views.wdetails_n,name="wdetails_n"),
    path('product_detail_n/<int:pk>',views.product_detail_n,name="product_detail_n"),
    path('myorder_n/',views.myorder_n,name="myorder_n"),
    path('orderpage_nur/<int:pk>',views.orderpage_nur,name="orderpage_nur"),
    path('payment_nur/',views.payment_nur,name="payment_nur"),
]
