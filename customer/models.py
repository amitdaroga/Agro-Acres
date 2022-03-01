from django.db import models
#from farmer.models import *
# Create your models here.
class user(models.Model):
	category=models.CharField(max_length=100)
	email=models.CharField(max_length=100,unique=True)
	password=models.CharField(max_length=100)
	otp=models.IntegerField(default=7812)

class customer_details(models.Model):
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

