from cgitb import enable
import imp
from random import randint
from django.shortcuts import render,redirect
from .models import *
from farmer.models import *
from nursery.models import *
from agroshop.models import *
from admin_app.models import *
from .utils import *
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.core.paginator import Page, Paginator
from django.conf import settings
from farmer.models import Transaction
from farmer.paytm import generate_checksum, verify_checksum

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]   
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)


# Create your views here.
def registration(request):
	if request.method=='POST':
		category=request.POST['tbcategory']
		fname=request.POST['tbfirstname']
		lname=request.POST['tblastname']
		email=request.POST['tbemail']
		phone=request.POST['tbphone']
		password=request.POST['tbpassword']
		c_password=request.POST['tbc_password']
		if category == "FARMER":
			if c_password == password:
				uid=user.objects.create(category=category,email=email,password=password)
				uid=user.objects.get(email=email)
				far_id=farmer_details.objects.create(user_id=uid,first_name=fname,last_name=lname,phone=phone)
				sendmail("confirmation","mail",email,{'firstname':fname,'lastname':lname})
				return render(request,'login.html')
			else:
				msg="password and conform password must be same"
				return render(request,'registration.html',{'msg':msg})
		elif category == "CUSTOMER":
			if c_password == password:
				uid=user.objects.create(category=category,email=email,password=password)
				uid=user.objects.get(email=email)
				cus_id=customer_details.objects.create(user_id=uid,first_name=fname,last_name=lname,phone=phone)
				sendmail("confirmation","mail",email,{'firstname':fname,'lastname':lname})
				return render(request,'login.html')
			else:
				msg="password and conform password must be same"
				return render(request,'registration.html',{'msg':msg})
		elif category=="NURSERY":
			if c_password == password:
				uid=user.objects.create(category=category,email=email,password=password)
				uid=user.objects.get(email=email)
				nur_id=nursery_details.objects.create(user_id=uid,first_name=fname,last_name=lname,phone=phone)
				sendmail("confirmation","mail",email,{'firstname':fname,'lastname':lname})
				return render(request,'login.html')
			else:
				msg="password and conform password must be same"
				return render(request,'registration.html',{'msg':msg})
		elif category=="AGROSHOP":
			if c_password == password:
				uid=user.objects.create(category=category,email=email,password=password)
				uid=user.objects.get(email=email)
				agro_id=agro_details.objects.create(user_id=uid,first_name=fname,last_name=lname,phone=phone)
				sendmail("confirmation","mail",email,{'firstname':fname,'lastname':lname})
				return render(request,'login.html')
			else:
				msg="password and conform password must be same"
				return render(request,'registration.html',{'msg':msg})
		else:
			msg="not work "
			return render(request,'registration.html',{'msg':msg})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			if user_id.category =="CUSTOMER":
				cus_id=customer_details.objects.get(user_id=user_id)
				return render(request,'index.html',{'user':user_id,'cus':cus_id})
			elif user_id.category =="FARMER":
				far_id=farmer_details.objects.get(user_id=user_id)
				cuscount=customer_details.objects.all().count()
				return render(request,'index_f.html',{'user':user_id,'far':far_id,'cuscount':cuscount})
			elif user_id.category =="NURSERY":
				nur_id=nursery_details.objects.get(user_id=user_id)
				return render(request,'index_n.html',{'user':user_id,'nur':nur_id})
			elif user_id.category =="AGROSHOP":
				agro_id=agro_details.objects.get(user_id=user_id)
				return render(request,'index_a.html',{'user':user_id,'agro':agro_id})
		else:
			return render(request,'registration.html')

def login(request):
	if request.method=='POST':
		Email=request.POST['email']
		print('email------------------------>',type(Email))
		password=request.POST['password']
		print('password ======================>',password)
		if Email=="" or password=="":
			msg="Please enter your email and password"
			return render (request,'login.html',{'msg':msg})

		elif Email=="admin@gmail.com": 
				if password =='admin':
					request.session['email']=Email
					adm_id=admin_details.objects.get(email=Email)
					return render(request,'home.html',{'admin':adm_id})
				else:
					msg="Please Enter valid password"
					return render(request,'login.html',{'msg':msg})

		else:
			user_id = user.objects.get(email=request.POST['email'])
			if user_id.category=="FARMER": 
				if user_id.password == password:
					request.session['email']=user_id.email
					far_id=farmer_details.objects.get(user_id=user_id)
					cuscount=customer_details.objects.all().count()
					ordercount=order_cus.objects.all().count()
					return render(request,'index_f.html',{'user':user_id,'far':far_id,'cuscount':cuscount,'ordercount':ordercount})
				else:
					msg="Please Enter valid password"
					return render(request,'login.html',{'msg':msg})

			elif user_id.category=="CUSTOMER": 
				if user_id.password == password:
					request.session['email']=user_id.email
					cus_id=customer_details.objects.get(user_id=user_id)
					return render(request,'index.html',{'user':user_id,'cus':cus_id})
				else:
					msg="Please Enter valid password"
					return render(request,'login.html',{'msg':msg})

			elif user_id.category=="NURSERY": 
				if user_id.password == password:
					request.session['email']=user_id.email
					nur_id=nursery_details.objects.get(user_id=user_id)
					return render(request,'index_n.html',{'user':user_id,'nur':nur_id})
				else:
					msg="Please Enter valid password"
					return render(request,'login.html',{'msg':msg})
			elif user_id.category=="AGROSHOP": 
				if user_id.password == password:
					request.session['email']=user_id.email
					agro_id=agro_details.objects.get(user_id=user_id)
					return render(request,'index_a.html',{'user':user_id,'agro':agro_id})
				else:
					msg="Please Enter valid password"
					return render(request,'login.html',{'msg':msg})
			
		# except:
		# 	msg="Your Email Address is wrong !"
		# 	return render(request,'registration.html',{'msg':msg})

	else:
		if 'email' in request.session:
			email=request.session['email']
			if 'admin@gmail.com' in email:
				adm_id=admin_details.objects.get(email=email)
				return render(request,'home.html',{'admin':adm_id})
			else:
				user_id=user.objects.get(email=request.session['email'])
				if user_id.category=="FARMER":
					far_id=farmer_details.objects.get(user_id=user_id)
					cuscount=customer_details.objects.all().count()
					return render(request,'index_f.html',{'user':user_id,'far':far_id,'cuscount':cuscount})
				elif user_id.category=="CUSTOMER":
					cus_id=customer_details.objects.get(user_id=user_id)
					return render(request,'index.html',{'user':user_id,'cus':cus_id})
				elif user_id.category=="NURSERY":
					nur_id=nursery_details.objects.get(user_id=user_id)
					return render(request,'index_n.html',{'user':user_id,'nur':nur_id})
				elif user_id.category=="AGROSHOP":
					agro_id=agro_details.objects.get(user_id=user_id)
					return render(request,'index_a.html',{'user':user_id,'agro':agro_id})
				else:
					return render(request,'login.html')
		else:
			return render(request,'login.html')

def index(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.get(user_id=user_id)
		return render(request,'index.html',{'user':user_id,'cus':cus_id})
	else:
		return render(request,'login.html')

def logout(request):
	if 'email' in request.session:
		if 'admin@gmail.com' == request.session['email']:
			del request.session['email']
			return render(request,'login.html')
		else:
			user_id=user.objects.get(email=request.session['email'])
			del request.session['email']
			return render(request,'login.html')
	else:
		return render(request,'login.html')

def profile(request):
	if 'email' in request.session:    
		user_id=user.objects.get(email=request.session['email'])
		if user_id.category=="CUSTOMER":
			cus_id=customer_details.objects.get(user_id=user_id)
			return render(request,'profile.html',{'user':user_id,'cus':cus_id})
		elif user_id.category=='FARMER':
			far_id=farmer_details.objects.get(user_id=user_id)
			return render(request,'profile_f.html',{'user':user_id,'cus':far_id})
	else:
		return render(request,'login.html')


def edit_profile(request):
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

			cus_id=customer_details.objects.get(user_id=user_id)
			cus_id.first_name=fname
			cus_id.last_name=lname
			cus_id.phone=phone
			cus_id.address=address
			cus_id.state=state
			cus_id.country=country
			cus_id.dod=dob
			cus_id.pincode=pincode
			user_id.email=email
			user_id.save()
			cus_id.save()
			return render(request,'profile.html',{'user':user_id,'cus':cus_id})

	else:
		if 'email' in request.session:
				user_id=user.objects.get(email=request.session['email'])
				return render(request,'profile.html',{'user':user_id})
		else:
			return render(request,'login.html')

def view_product(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.get(user_id=user_id)
		pro_id=product.objects.get(id=pk)
		return render(request,'view_product.html',{'user':user_id,'cus':cus_id,'pro':pro_id})
	else:
		return render(request,'login.html')

def gallery(request):
	if request.method=="POST":
		search=request.POST['search']
		user_id=user.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.get(user_id=user_id)
		p_id=product.objects.filter(product_name__icontains=search,enable='Enable')
		search_id=[]
		for i in p_id:
			if i.user_id.category=='FARMER':
				search_id.append(i)
		return render(request,'gallery.html',{'user':user_id,'cus':cus_id,'search_id':search_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			cus_id=customer_details.objects.get(user_id=user_id)
			pro_id=product.objects.filter(enable='Enable')
			p_id=[]
			for i in pro_id:
				if i.user_id.category=='FARMER':
					p_id.append(i)
				
			return render(request,'gallery.html',{'user':user_id,'cus':cus_id,'pro':p_id})
		else:
			return render(request,'registration.html')

def forgot_password(request):
	if request.method=="POST":
		email=request.POST['email']
		user_id=user.objects.filter(email=email)
		if user_id:
			user_id=user.objects.get(email=email)
			otp=random.randint(111111,999999)
			user_id.otp=otp
			user_id.save()
			sendmail("OTP",'f_password',email,{'otp':otp})
			return render(request,'new_password.html',{'email':email})
		else:
			msg="Email does not exits"
			return render(request,'forgot_password.html',{'msg':msg})
	else:
		return render(request,"forgot_password.html")

def new_password(request):
	if request.method=="POST":
		email=request.POST['email']
		otp=request.POST['otp']
		new_password=request.POST['password']
		conformpassword=request.POST['conformpassword']
		user_id=user.objects.get(email=email)
		if user_id.otp==int(otp):
			if new_password==conformpassword:
				user_id.password=new_password
				user_id.save()
				return render(request,'registration.html')
			else:
				msg="password and confrom password must be same"
				return render(request,'new_password.html',{'msg':msg})
		else:
			msg="incorrect otp"
			return render(request,'new_password.html',{'msg':msg})
	else:
		return render(request,"new_password.html")

def check_email(request):
	if 'POST' in request.method:
		email=request.POST['email']
		uid=user.objects.filter(email=email)
		if uid:
			status="Email found"
			JsonResponse({'status':status})
		else:
			status="Email not found"
			JsonResponse({'status':status})
	else:
		return redirect('/')


def nur_gallery(request):
	if request.method=="POST":
		search=request.POST['search']
		user_id=user.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.get(user_id=user_id)
		p_id=product.objects.filter(product_name__icontains=search,enable='Enable')
		search_id=[]
		for i in p_id:
			if i.user_id.category=='NURSERY':
				search_id.append(i)
		return render(request,'nur_gallery.html',{'user':user_id,'cus':cus_id,'search_id':search_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			cus_id=customer_details.objects.get(user_id=user_id)
			pro_id=product.objects.filter(enable='Enable')
			p_id=[]
			for i in pro_id:
				if i.user_id.category=='NURSERY':
					p_id.append(i)	
			return render(request,'nur_gallery.html',{'user':user_id,'cus':cus_id,'pro':p_id})
		else:
			return render(request,'login.html')

def addtocart_c(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.get(user_id=user_id)
		pro_id=product.objects.get(id=pk)
		p=int(pro_id.Price)
		addto_id= addtocart.objects.filter(p_id=pro_id,user_id=user_id)
		if addto_id:
			addto_id=addtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			return render(request,'addtocart_c.html',{'user':user_id,'cus':cus_id,'addtocart':addto_id,'totalamount':total_amount})
		else:
			add_id=addtocart.objects.create(p_id=pro_id,user_id=user_id,total_price=p,qty=1)
			add_id=addtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in add_id:
				total_amount=total_amount+i.total_price
			return render(request,'addtocart_c.html',{'user':user_id,'cus':cus_id,'addtocart':add_id,'totalamount':total_amount})
	else:
		return render(request,'login.html')
	
def addtodetails_c(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		nur_id=customer_details.objects.get(user_id=user_id)
		addto_id= addtocart.objects.filter(user_id=user_id)
		total_amount=0
		for i in addto_id:
			total_amount=total_amount+i.total_price
		return render(request,'addtocart_c.html',{'user':user_id,'cus':nur_id,'addtocart':addto_id,'totalamount':total_amount})
	else:
		return render(request,'login.html')

def update_qty_c(request):
	if request.method=="POST":
		cart_id = request.POST['cart_id']
		qty = request.POST['qty']
		price = request.POST['price']
		if(addtocart.objects.filter(id=cart_id)):
			qty=int(qty)
			cart = addtocart.objects.get(id=cart_id)
			total=int(qty)*int(price)
			cart.total_price = total
			cart.qty=int(qty)
			cart.save()
			all_items = addtocart.objects.filter(user_id=cart.user_id)
			subtotal=0
			for i in all_items:
				subtotal=subtotal+i.total_price
			data={
				'status':'updated',
				'total':total,
				'sub_total':subtotal,
			}
			return JsonResponse(data)
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			nur_id=customer_details.objects.get(user_id=user_id)
			addto_id= addtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			return render(request,'addtocart_c.html',{'user':user_id,'cus':nur_id,'addtocart':addto_id,'totalamount':total_amount})
		else:
			return render(request,'login.html')

def edit_img_c(request):
	if request.method=='POST':
		pic=request.FILES['pic']
		print("---------------------------------------------->",pic)
		user_id=user.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.get(user_id=user_id)
		cus_id.img=pic
		cus_id.save()
		return render(request,'profile.html',{'user':user_id,'cus':cus_id})
	else:
		if 'email' in request.session:
				user_id=user.objects.get(email=request.session['email'])
				cus_id=customer_details.objects.get(user_id=user_id)
				return render(request,'profile.html',{'user':user_id,'cus':cus_id})
		else:
			return render(request,'login.html')

def dele_record(request,pk):
	if 'email' in request.session:
		try:
			record = addtocart.objects.get(id=pk)
			record.delete()
			user_id=user.objects.get(email=request.session['email'])
			cus_id=customer_details.objects.get(user_id=user_id)
			addto_id=addtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			return render(request,'addtocart_c.html',{'user':user_id,'cus':cus_id,'addtocart':addto_id,'totalamount':total_amount})
		except:
			user_id=user.objects.get(email=request.session['email'])
			cus_id=customer_details.objects.get(user_id=user_id)
			addto_id= faraddtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			return render(request,'addtocart_c.html',{'user':user_id,'cus':cus_id,'addtocart':addto_id,'totalamount':total_amount})
	else:
		return render(request,'login.html')

def customerwishlist(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.get(user_id=user_id)
		pro_id=product.objects.get(id=pk)
		w_id= cuswishlist.objects.filter(p_id=pro_id,user_id=user_id)
		if w_id:
			w_id=cuswishlist.objects.filter(user_id=user_id)
			return render(request,'customerwishlist.html',{'user':user_id,'cus':cus_id,'wishlist':w_id})
		else:
			w_id=cuswishlist.objects.create(p_id=pro_id,user_id=user_id)
			w_id=cuswishlist.objects.filter(user_id=user_id)
			return render(request,'customerwishlist.html',{'user':user_id,'cus':cus_id,'wishlist':w_id})
	else:
		return render(request,'login.html')

def wishlist_c(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.get(user_id=user_id)
		w_id= cuswishlist.objects.filter(user_id=user_id)
		return render(request,'customerwishlist.html',{'user':user_id,'cus':cus_id,'wishlist':w_id})
	else:
		return render(request,'login.html')

def orderpage_cum(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.get(user_id=user_id)
		pro_id=product.objects.get(id=pk,enable='Enable')
		try:
			if cus_id.address=="None" or cus_id.city=="None":
				msg="Please Edit your profile "
				return render(request,'profile.html',{'user':user_id,'cus':cus_id,'msg':msg})
			else:
				return render(request,'orderpage_cum.html',{'user':user_id,'cus':cus_id,'pro':pro_id})
		except:
			user_id=user.objects.get(email=request.session['email'])
			cus_id=customer_details.objects.get(user_id=user_id)
			pro_id=product.objects.filter(enable='Enable')
			return render(request,'gallery.html',{'user':user_id,'cus':cus_id,'pro':pro_id})
	else:
		return render(request,'login.html')

def payment_cus(request):
	if request.method=="POST":
		pquantity=request.POST['pquantity']
		totalpri=request.POST['totalpri']
		pid=request.POST['pid']
		address=request.POST['address']
		city=request.POST['city']
		pin=request.POST['pin']
		user_id=user.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.get(user_id=user_id)
		pro_id=product.objects.get(id=pid)
		return render(request,'payment_cus.html',{'user':user_id,'cus':cus_id,'pro':pro_id,'pquantity':pquantity,'totalpri':totalpri,'address':address,'city':city,'pin':pin})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			cus_id=customer_details.objects.get(user_id=user_id)
			pro_id=product.objects.filter(enable='Enable')
			return render(request,'gallery.html',{'user':user_id,'cus':cus_id,'pro':pro_id})
		else:
			return render(request,'login.html')

def initiate_payment_cus(request):
    if request.method == "GET":
        print("Inside if")
        return render(request, 'pay.html')
    elif request.method=="POST":
        print("Inside else")
        pquantity=request.POST['pquantity']
        pid=request.POST['pid']
        address=request.POST['address']
        city=request.POST['city']
        pin=request.POST['pin']
        amount = int(request.POST['amount'])
        email=request.session['email']
        order_c(email,pquantity,pid,address,city,pin,amount)
        user_id = user.objects.get(email=request.session['email'])
        transaction = Transaction.objects.create(made_by=user_id, amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/farmer/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )
        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'redirect.html', context=paytm_params)

def order_c(email,pquantity,pid,address,city,pin,amount,request):
	pquantity=pquantity
	totalpri=amount
	pid=pid
	address=address
	city=city
	pin=pin
	email=email
	print("---------------------->",pquantity)
	print("---------------------->",pid)
	print("---------------------->",address)
	print("---------------------->",city)
	print("---------------------->",pin)
	print("---------------------->",totalpri)
	print("---------------------->",email)
	user_id=user.objects.get(email=email)
	order_id =order_cus.objects.filter(cus_id=user_id)
	for i in order_id:
		print("*"*20,i.orderdate)
	cus_id=customer_details.objects.get(user_id=user_id)
	cus_id.address=address
	cus_id.city=city
	cus_id.pincode=pin
	cus_id.save()
	pro_id=product.objects.get(id=pid)
	if int(pro_id.pro_quantity)>=int(pquantity):
		print("------------------------------>",pro_id.pro_quantity)
		order_id=order_cus.objects.create(pid=pro_id,cus_id=user_id,totalpri=totalpri,quantity=pquantity,seller_id=pro_id.user_id.email)
		quantity=int(pro_id.pro_quantity)-int(pquantity)
		pro_id=product.objects.get(id=pid)
		pro_id.pro_quantity=quantity
		pro_id.save()
		pro_id=product.objects.get(id=pid)
		if int(pro_id.pro_quantity)<=0:
			print("------------------------>")
			pro_id=product.objects.get(id=pid)
			pro_id.enable='Disable'
			pro_id.save()
	else:
		print("------------------------------>work not ")
		return render(request,'orderpage_f.html',{'user':user_id,'cus':cus_id,'pro':pro_id})

def addpayment_cus(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		cus_id=customer_details.objects.get(user_id=user_id)
		if cus_id.address=="None" or cus_id.city=="None" or cus_id.pincode=="None":
			msg="Please Edit your profile "
			return render(request,'profile.html',{'user':user_id,'cus':cus_id,'msg':msg})
		else:
			addto_id=addtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			return render(request,'addpayment_cus.html',{'user':user_id,'cus':cus_id,'addtocart':addto_id,'totalamount':total_amount})
	else:
		return render(request,'login.html')

def initiate_payment_addc(request):
    if request.method == "GET":
        print("Inside if")
        return render(request, 'pay.html')
    elif request.method=="POST":
        print("Inside else")
        # pquantity=request.POST['pquantity']
        # pid=request.POST['pid']
        address=request.POST['address']
        city=request.POST['city']
        pin=request.POST['pin']
        amount = int(request.POST['amount'])
        email=request.session['email']
        user_id = user.objects.get(email=request.session['email'])
        addto_id= addtocart.objects.filter(user_id=user_id)
        for i in addto_id:
        	order_c(email,i.qty,i.p_id.id,address,city,pin,i.total_price,request)
      #  user_id = user.objects.get(email=request.session['email'])
        transaction = Transaction.objects.create(made_by=user_id, amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/farmer/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )
        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'redirect.html', context=paytm_params)