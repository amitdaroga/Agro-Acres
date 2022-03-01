from django.db import models
from customer.models import *
# Create your models here.

class nursery_details(models.Model):
	img=models.FileField(upload_to="media/profile",default="media/profile/default.png")
	user_id=models.ForeignKey(user,on_delete=models.CASCADE)
	dod=models.CharField(max_length=100,null=True)
	first_name=models.CharField(max_length=100,null=True)
	last_name=models.CharField(max_length=100,null=True)
	phone=models.CharField(max_length=100,null=True)
	address=models.CharField(max_length=100,null=True)
	country=models.CharField(max_length=100,null=True)
	city=models.CharField(max_length=100,null=True)
	pincode=models.CharField(max_length=100,null=True)

# class nurproduct(models.Model):
# 	nur_id=models.ForeignKey(nursery_details,on_delete=models.CASCADE)
# 	product_name=models.CharField(max_length=100)
# 	pro_description=models.CharField(max_length=200)
# 	pro_category=models.CharField(max_length=100)
# 	Price=models.CharField(max_length=100)
# 	pro_quantity=models.CharField(max_length=100)
# 	pic=models.FileField(upload_to="media/nurproduct")
# 	enable=models.CharField(max_length=100,default="Enable")
