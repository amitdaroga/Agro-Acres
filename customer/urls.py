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
from customer import views

urlpatterns = [
    path('registration/',views.registration,name='registration'),
    path('',views.login,name='login'),
    path('index/',views.index,name='index'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('view_product/<int:pk>',views.view_product,name='view_product'),
    path('gallery/',views.gallery,name='gallery'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('new_password/',views.new_password,name='new_password'),
    path('check_email/',views.check_email,name='check_email'),
    path('nur_gallery/',views.nur_gallery,name='nur_gallery'),
    path('addtocart_c/<int:pk>',views.addtocart_c,name="addtocart_c"),
    path('addtodetails_c/',views.addtodetails_c,name="addtodetails_c"),
    path('update_qty_c/',views.update_qty_c,name='update_qty_c'),
    path('edit_img_c/',views.edit_img_c,name='edit_img_c'),
    path('dele_record/<int:pk>',views.dele_record,name="dele_record"),
    path('customerwishlist/<int:pk>',views.customerwishlist,name="customerwishlist"),
    path('wishlist_c/',views.wishlist_c,name="wishlist_c"),
    path('orderpage_cum/<int:pk>',views.orderpage_cum,name="orderpage_cum"),
    path('payment_cus/',views.payment_cus,name="payment_cus"),
    path('pay_cus',views.initiate_payment_cus,name="pay_cus"),
    path('addpayment_cus/',views.addpayment_cus,name="addpayment_cus"),
    path('pay_addtocartcus/',views.initiate_payment_addc,name="pay_addtocartcus"),
]
