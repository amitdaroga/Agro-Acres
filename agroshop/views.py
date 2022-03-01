import types
from django.shortcuts import render
from .models import *
from farmer.models import *
from nursery.models import *
from agroshop.models import *
from django.core.paginator import Page, Paginator
# Create your views here.

def index_a(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		agro_id=agro_details.objects.get(user_id=user_id)
		pro_id=agroproduct.objects.filter(agro_id=agro_id).count()
		return render(request,'index_a.html',{'user':user_id,'agro':agro_id,'pro':pro_id})
	else:
		return render(request,'login.html')
def profile_a(request):
	if 'email' in request.session:    
		user_id=user.objects.get(email=request.session['email'])
		agro_id=agro_details.objects.get(user_id=user_id)
		return render(request,'profile_a.html',{'user':user_id,'agro':agro_id})
	else:
		return render(request,'login.html')

def edit_profile_a(request):
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
			user_id=user.objects.get(email=request.session['email'])

			agro_id=agro_details.objects.get(user_id=user_id)
			agro_id.first_name=fname
			agro_id.last_name=lname
			agro_id.phone=phone
			agro_id.address=address
			agro_id.state=state
			agro_id.country=country
			agro_id.dod=dob
			agro_id.pincode=pincode
			user_id.email=email
			user_id.save()
			agro_id.save()
			return render(request,'profile_a.html',{'user':user_id,'agro':agro_id})

	else:
		if 'email' in request.session:
				user_id=user.objects.get(email=request.session['email'])
				return render(request,'profile_a.html',{'user':user_id})
		else:
			return render(request,'login.html')
def edit_img_a(request):
	if request.method=='POST':
		pic=request.FILES['pic']
		print("---------------------------------------------->",pic)
		user_id=user.objects.get(email=request.session['email'])
		agro_id=agro_details.objects.get(user_id=user_id)
		agro_id.img=pic
		agro_id.save()
		return render(request,'profile_a.html',{'user':user_id,'agro':agro_id})
	else:
		if 'email' in request.session:
				user_id=user.objects.get(email=request.session['email'])
				return render(request,'profile_a.html',{'user':user_id})
		else:
			return render(request,'login.html')

def upload_product_a(request):
	if request.method=='POST':
		pic=request.FILES['pic']
		pcategory=request.POST['pcategory']
		price=request.POST['price']
		pname=request.POST['pname']
		pquantity=request.POST['pquantity']
		pdescription=request.POST['pdescription']
		user_id=user.objects.get(email=request.session['email'])
		agro_id=agro_details.objects.get(user_id=user_id)
		p_id=agroproduct.objects.filter(agro_id=agro_id,product_name=pname)
		if p_id:
			msg="product in list"
			return render(request,'upload_product_a.html',{'user':user_id,'agro':agro_id,'msg':msg})
		else:
			pro_id=agroproduct.objects.create(agro_id=agro_id,product_name=pname,pro_description=pdescription,pro_category=pcategory,Price=price,pro_quantity=pquantity,pic=pic)
			pro_id=agroproduct.objects.filter(agro_id=agro_id)
			p=Paginator(pro_id,2)
			page=request.GET.get('page')
			pro_id=p.get_page(page)
			return render(request,'my_product_a.html',{'user':user_id,'agro':agro_id,'pro':pro_id})
	else:
		if 'email' in request.session:
				user_id=user.objects.get(email=request.session['email'])
				agro_id=agro_details.objects.get(user_id=user_id)
				return render(request,'upload_product_a.html',{'user':user_id,'agro':agro_id})
		else:
			return render(request,'login.html')

def my_product_a(request):
	if request.method=="POST":
		search=request.POST['search']
		user_id=user.objects.get(email=request.session['email'])
		agro_id=agro_details.objects.get(user_id=user_id)
		seaech_id=agroproduct.objects.filter(agro_id=agro_id,product_name__icontains=search)
		return render(request,'my_product_a.html',{'user':user_id,'agro':agro_id,'seaech_id':seaech_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			agro_id=agro_details.objects.get(user_id=user_id)
			pro_id=agroproduct.objects.filter(agro_id=agro_id)
			p=Paginator(pro_id,2)
			page=request.GET.get('page')
			pro_id=p.get_page(page)
			return render(request,'my_product_a.html',{'user':user_id,'agro':agro_id,'pro':pro_id})
		else:
			return render(request,'login.html')

def productdetails_a(request, pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		agro_id=agro_details.objects.get(user_id=user_id)
		p_id=agroproduct.objects.filter(id=pk)
		return render(request,'productdetails_a.html',{'user':user_id,'agro':agro_id,'product':p_id})
	else:
		return render(request,'login.html')

def update_product_a(request):
	if request.method=='POST':
		id=request.POST['id']
		price=request.POST['price']
		pquantity=request.POST['pquantity']
		enable=request.POST['enable']
		user_id=user.objects.get(email=request.session['email'])
		agro_id=agro_details.objects.get(user_id=user_id)
		pro_id=agroproduct.objects.filter(agro_id=agro_id)
		p_id=agroproduct.objects.get(id=id)
		p_id.Price=price
		p_id.pro_quantity=pquantity
		p_id.enable=enable
		p_id.save()
		p=Paginator(pro_id,2)
		page=request.GET.get('page')
		pro_id=p.get_page(page)
		return render(request,'my_product_a.html',{'user':user_id,'agro':agro_id,'pro':pro_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			agro_id=agro_details.objects.get(user_id=user_id)
			pro_id=agroproduct.objects.filter(agro_id=agro_id)
			p=Paginator(pro_id,2)
			page=request.GET.get('page')
			pro_id=p.get_page(page)
			return render(request,'my_product_a.html',{'user':user_id,'agro':agro_id,'pro':pro_id})
		else:
			return render(request,'login.html')

def myorder_a(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		agro_id=agro_details.objects.get(user_id=user_id)
		or_id=order_a.objects.filter(seller_id=request.session['email'])
		return render(request,'myorder_a.html',{'user':user_id,'agro':agro_id,'order':or_id})
	else:
		return render(request,'login.html')
		