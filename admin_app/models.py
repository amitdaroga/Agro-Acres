from django.db import models

# Create your models here.
class admin_details(models.Model):
	email=models.CharField(max_length=100,default="admin@gmail.com")
	img=models.FileField(upload_to="media/profile",default="media/profile/default.png")
	dod=models.CharField(max_length=100,null=True)
	first_name=models.CharField(max_length=100,null=True)
	last_name=models.CharField(max_length=100,null=True)
	phone=models.CharField(max_length=100,null=True)
	address=models.CharField(max_length=100,null=True)
	country=models.CharField(max_length=100,null=True)
	city=models.CharField(max_length=100,null=True)
	pincode=models.CharField(max_length=100,null=True)
