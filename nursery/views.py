from django.shortcuts import render
from .models import *
from agroshop.models import *
from farmer.models import *
from django.core.paginator import Page, Paginator
# Create your views here.

def index_n(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		return render(request,'index_n.html',{'user':user_id,'nur':nur_id})
	else:
		return render(request,'registration.html')

def profile_n(request):
	if 'email' in request.session:    
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		return render(request,'profile_n.html',{'user':user_id,'nur':nur_id})
	else:
		return render(request,'registration.html')

def edit_profile_n(request):
	if request.method=='POST':
		fname=request.POST['fname']
		lname=request.POST['lname']
		phone=request.POST['phone']
		address=request.POST['address']
		city=request.POST['city']
		email=request.POST['email']
		country=request.POST['country']
		dob=request.POST['dob']
		pincode=request.POST['pincode']
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		nur_id.first_name=fname
		nur_id.last_name=lname
		nur_id.phone=phone
		nur_id.address=address
		nur_id.city=city
		nur_id.country=country
		nur_id.dod=dob
		nur_id.pincode=pincode
		user_id.email=email
		user_id.save()
		nur_id.save()
		return render(request,'profile_n.html',{'user':user_id,'nur':nur_id})

	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			return render(request,'profile_f.html',{'user':user_id})
		else:
			return render(request,'login.html')

def upload_product_n(request):
	if request.method=="POST":
		pic=request.FILES['pic']
		p_name=request.POST['pname']
		p_description=request.POST['pdescription']
		p_category=request.POST['pcategory']
		price=request.POST['price']
		p_quantity=request.POST['pquantity']
		user_id=user.objects.get(email=request.session['email'])
		n_id=nursery_details.objects.get(user_id=user_id)
		print("-------->>>>>>>>>>>>",pic)
		print("-------->>>>>>>>>>>>",p_name)
		print("-------->>>>>>>>>>>>",p_description)
		print("-------->>>>>>>>>>>>",p_category)
		print("-------->>>>>>>>>>>>",price)
		print("-------->>>>>>>>>>>>",p_quantity)
		p_id=product.objects.filter(user_id=user_id,product_name=p_name)
		if p_id:
			msg="product in list"
			return render(request,'upload_product_n.html',{'user':user_id,'nur':n_id,'msg':msg})			
		else:
			nur_id=product.objects.create(user_id=user_id,product_name=p_name,pro_description=p_description,pro_category=p_category,Price=price,pro_quantity=p_quantity,pic=pic)
			nur_id=nursery_details.objects.get(user_id=user_id)
			pro_id=product.objects.filter(user_id=user_id)
			return render(request,'my_product_n.html',{'user':user_id,'nur':n_id,'pro':pro_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			nur_id=nursery_details.objects.get(user_id=user_id)
			return render(request,'upload_product_n.html',{'user':user_id,'nur':nur_id})
		else:
			return render(request,'login.html')

def my_product_n(request):
	if request.method=="POST":
		search=request.POST['search']
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		search_id=product.objects.filter(user_id=user_id,product_name__icontains=search)
		return render(request,'my_product_n.html',{'user':user_id,'nur':nur_id,'search_id':search_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			nur_id=nursery_details.objects.get(user_id=user_id)
			pro_id=product.objects.filter(user_id=user_id)
			p=Paginator(pro_id,2)
			page=request.GET.get('page')
			pro_id=p.get_page(page)
			return render(request,'my_product_n.html',{'user':user_id,'nur':nur_id,'pro':pro_id})
		else:
			return render(request,'login.html')

def productdetails_n(request, pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		p_id=product.objects.filter(id=pk)
		return render(request,'productdetails_n.html',{'user':user_id,'nur':nur_id,'product':p_id})
	else:
		return render(request,'login.html')

def update_product_n(request):
	if request.method=='POST':
		id=request.POST['id']
		price=request.POST['price']
		pquantity=request.POST['pquantity']
		enable=request.POST['enable']
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		pro_id=product.objects.filter(user_id=user_id)
		p_id=product.objects.get(id=id)
		p_id.Price=price
		p_id.pro_quantity=pquantity
		p_id.enable=enable
		p_id.save()
		p=Paginator(pro_id,2)
		page=request.GET.get('page')
		pro_id=p.get_page(page)
		return render(request,'my_product_n.html',{'user':user_id,'nur':nur_id,'pro':pro_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			nur_id=nursery_details.objects.get(user_id=user_id)
			pro_id=product.objects.filter(user_id=user_id)
			if pro_id:
				p=Paginator(pro_id,2)
				page=request.GET.get('page')
				pro_id=p.get_page(page)
				return render(request,'my_product_n.html',{'user':user_id,'nur':nur_id,'pro':pro_id})
		else:
			return render(request,'login.html')

def gallery_n(request):
	if request.method=="POST":
		search=request.POST['search']
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		search_id=agroproduct.objects.filter(product_name__icontains=search)
		return render(request,'gallery_n.html',{'user':user_id,'nur':nur_id,'search_id':search_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			nur_id=nursery_details.objects.get(user_id=user_id)
			pro_id=agroproduct.objects.filter(enable='Enable')
			return render(request,'gallery_n.html',{'user':user_id,'nur':nur_id,'pro':pro_id})
		else:
			return render(request,'login.html')

def p_details_n(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		pro_id=agroproduct.objects.get(id=pk)
		return render(request,'p_details_n.html',{'user':user_id,'nur':nur_id,'pro':pro_id})

def addtocart_n(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		pro_id=agroproduct.objects.get(id=pk)
		p=int(pro_id.Price)
		addto_id= faraddtocart.objects.filter(p_id=pro_id,user_id=user_id)
		if addto_id:
			addto_id=faraddtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			
			return render(request,'addtocart_n.html',{'user':user_id,'nur':nur_id,'addtocart':addto_id,'totalamount':total_amount})
		else:
			addto_id=faraddtocart.objects.create(p_id=pro_id,user_id=user_id,total_price=p,qty=1)
			addto_id=faraddtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			return render(request,'addtocart_n.html',{'user':user_id,'nur':nur_id,'addtocart':addto_id,'totalamount':total_amount})
	else:
		return render(request,'login.html')

def addtodetails_n(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		addto_id= faraddtocart.objects.filter(user_id=user_id)
		total_amount=0
		for i in addto_id:
			total_amount=total_amount+i.total_price
		return render(request,'addtocart_n.html',{'user':user_id,'nur':nur_id,'addtocart':addto_id,'totalamount':total_amount})
	else:
		return render(request,'login.html')

def delete_record_n(request,pk):
	if 'email' in request.session:
		try:
			record = faraddtocart.objects.get(id =pk)
			record.delete()
			user_id=user.objects.get(email=request.session['email'])
			nur_id=nursery_details.objects.get(user_id=user_id)
			addto_id= faraddtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			return render(request,'addtocart_n.html',{'user':user_id,'nur':nur_id,'addtocart':addto_id,'totalamount':total_amount})
		except:
			user_id=user.objects.get(email=request.session['email'])
			nur_id=nursery_details.objects.get(user_id=user_id)
			addto_id= faraddtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			return render(request,'addtocart_n.html',{'user':user_id,'nur':nur_id,'addtocart':addto_id,'totalamount':total_amount})
	else:
		return render(request,'login.html')

def edit_img_n(request):
	if request.method=='POST':
		pic=request.FILES['pic']
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		nur_id.img=pic
		nur_id.save()
		return render(request,'profile_n.html',{'user':user_id,'nur':nur_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			return render(request,'profile_n.html',{'user':user_id})
		else:
			return render(request,'login.html')

def wishlist_n(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		pro_id=agroproduct.objects.get(id=pk)
		w_id= farwishlist.objects.filter(p_id=pro_id,user_id=user_id)
		if w_id:
			w_id=farwishlist.objects.filter(user_id=user_id)
			return render(request,'wishlist_n.html',{'user':user_id,'far':far_id,'wishlist':w_id})
		else:
			w_id=farwishlist.objects.create(p_id=pro_id,user_id=user_id)
			w_id=farwishlist.objects.filter(user_id=user_id)
			return render(request,'wishlist_n.html',{'user':user_id,'nur':nur_id,'wishlist':w_id})
	else:
		return render(request,'login.html')

def wdetails_n(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		w_id= farwishlist.objects.filter(user_id=user_id)
		return render(request,'wishlist_n.html',{'user':user_id,'nur':nur_id,'wishlist':w_id})
	else:
		return render(request,'login.html')

def product_detail_n(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		pro_id=agroproduct.objects.get(id=pk,enable='Enable')
		return render(request,'product_detail_n.html',{'user':user_id,'nur':nur_id,'pro':pro_id})
	else:
		return render(request,'login.html')
def myorder_n(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		or_id=order_cus.objects.filter(seller_id=request.session['email'])
		return render(request,'myorder_n.html',{'user':user_id,'nur':nur_id,'order':or_id})
	else:
		return render(request,'login.html')
def orderpage_nur(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		pro_id=agroproduct.objects.get(id=pk,enable='Enable')
		if nur_id.address=="None" or nur_id.city=="None":
			msg="Please Edit your profile "
			return render(request,'profile_n.html',{'user':user_id,'nur':nur_id,'msg':msg})
		else:
			return render(request,'orderpage_nur.html',{'user':user_id,'nur':nur_id,'pro':pro_id})
		# except:
		# 	user_id=user.objects.get(email=request.session['email'])
		# 	nur_id=nursery_details.objects.get(user_id=user_id)
		# 	pro_id=agroproduct.objects.filter(enable='Enable')
		# 	return render(request,'gallery_n.html',{'user':user_id,'nur':nur_id,'pro':pro_id})
	else:
		return render(request,'login.html')

def payment_nur(request):
	if request.method=="POST":
		pquantity=request.POST['pquantity']
		totalpri=request.POST['totalpri']
		pid=request.POST['pid']
		address=request.POST['address']
		city=request.POST['city']
		pin=request.POST['pin']
		user_id=user.objects.get(email=request.session['email'])
		nur_id=nursery_details.objects.get(user_id=user_id)
		pro_id=agroproduct.objects.get(id=pid)
		return render(request,'payment_nur.html',{'user':user_id,'nur':nur_id,'pro':pro_id,'pquantity':pquantity,'totalpri':totalpri,'address':address,'city':city,'pin':pin})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			nur_id=nursery_details.objects.get(user_id=user_id)
			pro_id=agroproduct.objects.filter(enable='Enable')
			return render(request,'gallery_n.html',{'user':user_id,'nur':nur_id,'pro':pro_id})
		else:
			return render(request,'login.html')