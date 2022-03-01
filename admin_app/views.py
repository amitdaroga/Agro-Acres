from django.shortcuts import render,redirect
# Create your views here.
from .models import *
from customer.models import *
from farmer.models import *
from nursery.models import *
from agroshop.models import *
from admin_app.models import *

def home(request):
	if 'email' in request.session:
		adm_id=admin_details.objects.get(email=request.session['email'])
		return render(request,'home.html',{'admin':adm_id})
	else:
		return render(request,'login.html')

def admin_profile(request):
	if 'email' in request.session:
		adm_id=admin_details.objects.get(email=request.session['email'])
		return render(request,'admin_profile.html',{'admin':adm_id})
	else:
		return render(request,'login.html')

def editprofile_admin(request):
	if request.method=='POST':
		
			fname=request.POST['fname']
			lname=request.POST['lname']
			phone=request.POST['phone']
			address=request.POST['address']
			state=request.POST['city']
			email=request.POST['email']
			country=request.POST['country']
			dob=request.POST['dob']
			pincode=request.POST['pincode']
			admin_id=admin_details.objects.get(email=request.session['email'])
			admin_id.first_name=fname
			admin_id.last_name=lname
			admin_id.phone=phone
			admin_id.address=address
			admin_id.state=state
			admin_id.country=country
			admin_id.dod=dob
			admin_id.pincode=pincode
			admin_id.email=email
			admin_id.save()
			return render(request,'admin_profile.html',{'admin':admin_id})

	else:
		if 'email' in request.session:
			admin_id=admin_details.objects.get(email=request.session['email'])
			return render(request,'admin_profile.html',{'admin':admin_id})
		else:
			return render(request,'login.html')

def editimg_admin(request):
	if request.method=='POST':
		pic=request.FILES['pic']
		print("---------------------------------------------->",pic)
		admin_id=admin_details.objects.get(email=request.session['email'])
		admin_id.img=pic
		admin_id.save()
		return render(request,'admin_profile.html',{'admin':admin_id})
	else:
		if 'email' in request.session:
				admin_id=admin_details.objects.get(email=request.session['email'])
				return render(request,'admin_profile.html',{'admin':admin_id})
		else:
			return render(request,'login.html')

def alluser_detail(request):
	if 'email' in request.session:
		admin_id=admin_details.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.all()
		far_id=farmer_details.objects.all()
		nur_id=nursery_details.objects.all()
		agro_id=agro_details.objects.all()
		return render(request,'alluser_detail.html',{'admin':admin_id,'cus':cus_id,'far':far_id,'nur':nur_id,'agro':agro_id})
	else:
		return render(request,'login.html')

def edituser_detail(request,pk):
	if 'email' in request.session:
		admin_id=admin_details.objects.get(email=request.session['email'])
		user_id=user.objects.get(id=pk)
		if user_id.category=='CUSTOMER':
			user_id=customer_details.objects.get(user_id=user_id)
			return render(request,'edituser_detail.html',{'admin':admin_id,'user':user_id})
		elif user_id.category=='FARMER':
			user_id=farmer_details.objects.get(user_id=user_id)
			return render(request,'edituser_detail.html',{'admin':admin_id,'user':user_id})
		elif user_id.category=='NURSERY':
			user_id=nursery_details.objects.get(user_id=user_id)
			return render(request,'edituser_detail.html',{'admin':admin_id,'user':user_id})
		elif user_id.category=='AGROSHOP':
			user_id=agro_details.objects.get(user_id=user_id)
			return render(request,'edituser_detail.html',{'admin':admin_id,'user':user_id})
		else:
			return render(request,'login.html')
	else:
			return render(request,'login.html')
def updateuser_details(request):
	if request.method=='POST':
		fname=request.POST['fname']
		lname=request.POST['lname']
		phone=request.POST['phone']
		address=request.POST['address']
		city=request.POST['city']
		email=request.POST['email']
		category=request.POST['tbcategory']
		dob=request.POST['dob']
		pincode=request.POST['pincode']
		user_id=user.objects.get(email=email)
		if user_id.category=="CUSTOMER":
			cus_id=customer_details.objects.get(user_id=user_id)
			cus_id.first_name=fname
			cus_id.last_name=lname
			cus_id.phone=phone
			cus_id.address=address
			cus_id.city=city
			user_id.category=category
			cus_id.dod=dob
			cus_id.pincode=pincode
			user_id.email=email
			user_id.save()
			cus_id.save()
			admin_id=admin_details.objects.get(email=request.session['email'])
			cus_id=customer_details.objects.all()
			far_id=farmer_details.objects.all()
			nur_id=nursery_details.objects.all()
			agro_id=agro_details.objects.all()
			return render(request,'alluser_detail.html',{'admin':admin_id,'cus':cus_id,'far':far_id,'nur':nur_id,'agro':agro_id})
		elif user_id.category=="FARMER":
			cus_id=farmer_details.objects.get(user_id=user_id)
			cus_id.first_name=fname
			cus_id.last_name=lname
			cus_id.phone=phone
			cus_id.address=address
			cus_id.city=city
			user_id.category=category
			cus_id.dod=dob
			cus_id.pincode=pincode
			user_id.email=email
			user_id.save()
			cus_id.save()
			admin_id=admin_details.objects.get(email=request.session['email'])
			cus_id=customer_details.objects.all()
			far_id=farmer_details.objects.all()
			nur_id=nursery_details.objects.all()
			agro_id=agro_details.objects.all()
			return render(request,'alluser_detail.html',{'admin':admin_id,'cus':cus_id,'far':far_id,'nur':nur_id,'agro':agro_id})
		elif user_id.category=="NURSERY":
			cus_id=nursery_details.objects.get(user_id=user_id)
			cus_id.first_name=fname
			cus_id.last_name=lname
			cus_id.phone=phone
			cus_id.address=address
			cus_id.city=city
			user_id.category=category
			cus_id.dod=dob
			cus_id.pincode=pincode
			user_id.email=email
			user_id.save()
			cus_id.save()
			admin_id=admin_details.objects.get(email=request.session['email'])
			cus_id=customer_details.objects.all()
			far_id=farmer_details.objects.all()
			nur_id=nursery_details.objects.all()
			agro_id=agro_details.objects.all()
			return render(request,'alluser_detail.html',{'admin':admin_id,'cus':cus_id,'far':far_id,'nur':nur_id,'agro':agro_id})

		elif user_id.category=="AGROSHOP":
			cus_id=agro_details.objects.get(user_id=user_id)
			cus_id.first_name=fname
			cus_id.last_name=lname
			cus_id.phone=phone
			cus_id.address=address
			cus_id.city=city
			user_id.category=category
			cus_id.dod=dob
			cus_id.pincode=pincode
			user_id.email=email
			user_id.save()
			cus_id.save()
			admin_id=admin_details.objects.get(email=request.session['email'])
			cus_id=customer_details.objects.all()
			far_id=farmer_details.objects.all()
			nur_id=nursery_details.objects.all()
			agro_id=agro_details.objects.all()
			return render(request,'alluser_detail.html',{'admin':admin_id,'cus':cus_id,'far':far_id,'nur':nur_id,'agro':agro_id})
			
	else:
		if 'email' in request.session:
			admin_id=admin_details.objects.get(email=request.session['email'])
			cus_id=customer_details.objects.all()
			far_id=farmer_details.objects.all()
			nur_id=nursery_details.objects.all()
			agro_id=agro_details.objects.all()
			return render(request,'alluser_detail.html',{'admin':admin_id,'cus':cus_id,'far':far_id,'nur':nur_id,'agro':agro_id})
		else:
			return render(request,'login.html')

def removeuser_details(request,pk):
	if 'email' in request.session:
		user_id= user.objects.get(id=pk)
		user_id.delete()
		admin_id=admin_details.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.all()
		far_id=farmer_details.objects.all()
		nur_id=nursery_details.objects.all()
		agro_id=agro_details.objects.all()
		return render(request,'alluser_detail.html',{'admin':admin_id,'cus':cus_id,'far':far_id,'nur':nur_id,'agro':agro_id})
	else:
		return render(request,'login.html')

def allproduct_detail(request,pk):
	if 'email' in request.session:
		admin_id=admin_details.objects.get(email=request.session['email'])
		user_id=user.objects.get(id=pk)
		if user_id.category=="AGROSHOP":
			agro_id=agro_details.objects.get(user_id=user_id)
			pro_id=agroproduct.objects.filter(agro_id=agro_id)
			return render(request,'allproduct_detail.html',{'admin':admin_id,'pro':pro_id})
		elif user_id.category=="NURSERY":
			pro_id=product.objects.filter(user_id=user_id)
			return render(request,'allproduct_detail.html',{'admin':admin_id,'pro':pro_id})
		elif user_id.category=="FARMER":
			pro_id=product.objects.filter(user_id=user_id)
			return render(request,'allproduct_detail.html',{'admin':admin_id,'pro':pro_id})
		else:
			admin_id=admin_details.objects.get(email=request.session['email'])
			cus_id=customer_details.objects.all()
			far_id=farmer_details.objects.all()
			nur_id=nursery_details.objects.all()
			agro_id=agro_details.objects.all()
			return render(request,'alluser_detail.html',{'admin':admin_id,'cus':cus_id,'far':far_id,'nur':nur_id,'agro':agro_id})	
	else:
		return render(request,'login.html')

	