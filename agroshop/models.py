from django.db import models
from customer.models import *
# Create your models here.

class agro_details(models.Model):
	user_id=models.ForeignKey(user,on_delete=models.CASCADE)
	img=models.FileField(upload_to="media/profile",default="media/profile/default.png")
	dod=models.CharField(max_length=100,null=True)
	first_name=models.CharField(max_length=100,null=True)
	last_name=models.CharField(max_length=100,null=True)
	phone=models.CharField(max_length=100,null=True)
	address=models.CharField(max_length=100,null=True)
	country=models.CharField(max_length=100,null=True)
	city=models.CharField(max_length=100,null=True)
	pincode=models.CharField(max_length=100,null=True)

class agroproduct(models.Model):
	agro_id=models.ForeignKey(agro_details,on_delete=models.CASCADE)
	product_name=models.CharField(max_length=100)
	pro_description=models.CharField(max_length=200)
	pro_category=models.CharField(max_length=100)
	Price=models.CharField(max_length=100)
	pro_quantity=models.CharField(max_length=100)
	pic=models.FileField(upload_to="media/agroproduct")
	enable=models.CharField(max_length=100,default="Enable")

class order_a(models.Model):
	quantity=models.CharField(max_length=100)
	totalpri=models.CharField(max_length=100)
	pid=models.ForeignKey(agroproduct,on_delete=models.CASCADE)
	cus_id=models.ForeignKey(user,on_delete=models.CASCADE)
	seller_id=models.CharField(max_length=100)
	orderdate=models.DateTimeField(auto_now_add=True,blank=False)
	