from statistics import mode
from django.db import models
from customer.models import *
from agroshop.models import *
# Create your models here.
class farmer_details(models.Model):
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

class product(models.Model):
	user_id=models.ForeignKey(user,on_delete=models.CASCADE)
	product_name=models.CharField(max_length=100)
	pro_description=models.CharField(max_length=200)
	pro_category=models.CharField(max_length=100)
	Price=models.CharField(max_length=100)
	pro_quantity=models.CharField(max_length=100)
	pic=models.FileField(upload_to="media/farproduct")
	enable=models.CharField(max_length=100,default="Enable")

class faraddtocart(models.Model):
	p_id=models.ForeignKey(agroproduct,on_delete=models.CASCADE)
	user_id=models.ForeignKey(user,on_delete=models.CASCADE)
	total_price = models.IntegerField()
	qty = models.IntegerField()

class farwishlist(models.Model):
	p_id=models.ForeignKey(agroproduct,on_delete=models.CASCADE)
	user_id=models.ForeignKey(user,on_delete=models.CASCADE)

class addtocart(models.Model):
	p_id=models.ForeignKey(product,on_delete=models.CASCADE)
	user_id=models.ForeignKey(user,on_delete=models.CASCADE)
	total_price = models.IntegerField()
	qty = models.IntegerField()

class Transaction(models.Model):
    made_by = models.ForeignKey(user, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

class cuswishlist(models.Model):
	p_id=models.ForeignKey(product,on_delete=models.CASCADE)
	user_id=models.ForeignKey(user,on_delete=models.CASCADE)

class order_cus(models.Model):
	quantity=models.CharField(max_length=100)
	totalpri=models.CharField(max_length=100)
	pid=models.ForeignKey(product,on_delete=models.CASCADE)
	cus_id=models.ForeignKey(user,on_delete=models.CASCADE)
	seller_id=models.CharField(max_length=100)
	orderdate=models.DateTimeField(auto_now_add=True,blank=False)