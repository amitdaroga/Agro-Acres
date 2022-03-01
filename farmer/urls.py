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
from farmer import views
urlpatterns = [
    path('index_f/',views.index_f,name='index_f'),
    path('logout_f/',views.logout_f,name='logout_f'),
    path('profile_f/',views.profile_f,name='profile_f'),
    path('edit_profile_f/',views.edit_profile_f,name='edit_profile_f'),
    path('customer_det/',views.customer_det,name='customer_det'),
    path('upload_product_f/',views.upload_product_f,name='upload_product_f'),
    path('view_myproduct_f/',views.view_myproduct_f,name='view_myproduct_f'),
    path('gallery_f/',views.gallery_f,name='gallery_f'),
    path('productdetails_f/<int:pk>',views.productdetails_f,name='productdetails_f'),
    path('update_product_f',views.update_product_f,name='update_product_f'),
    path('p_details_f/<int:pk>',views.p_details_f,name="p_details_f"),
    path('addtocart_f/<int:pk>',views.addtocart_f,name="addtocart_f"),
    path('addtodetails_f/',views.addtodetails_f,name="addtodetails_f"),
    path('wishlist_f/<int:pk>',views.wishlist_f,name="wishlist_f"),
    path('update_qty/',views.update_qty,name='update_qty'),
    path('delete_record/<int:pk>',views.delete_record,name="delete_record"),
    path('edit_img_f/',views.edit_img_f,name="edit_img_f"),
    path('wdetails_f/',views.wdetails_f,name="wdetails_f"),
    path('orderpage_f/<int:pk>',views.orderpage_f,name="orderpage_f"),
    path('payment_f',views.payment_f,name="payment_f"),
    path('addpayment_f',views.addpayment_f,name="addpayment_f"),
    path('pay',views.initiate_payment,name="pay"),
    path('callback/',views.callback,name="callback"),
    path('pay_addtocart',views.initiate_payment_addf,name="pay_addtocart"),
    path('myorder_f/',views.myorder_f,name="myorder_f"),
]
