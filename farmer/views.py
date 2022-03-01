from cgitb import enable
import imp
import json
from random import randint
from django.shortcuts import render
from .models import *
from customer.models import *
from agroshop.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.core.paginator import Page, Paginator
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum

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


def index_f(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		cuscount=customer_details.objects.all().count()
		pro_id=product.objects.filter(user_id=user_id).count()
		ordercount=order_cus.objects.all().count()
		return render(request,'index_f.html',{'user':user_id,'far':far_id,'cuscount':cuscount,"pro":pro_id,'ordercount':ordercount})
	else:
		return render(request,'login.html')
def logout_f(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		del request.session['email']
		return render(request,'login.html')
	else:
		return render(request,'login.html')
def profile_f(request):
	if 'email' in request.session:    
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		return render(request,'profile_f.html',{'user':user_id,'far':far_id})
	else:
		return render(request,'login.html')
def edit_profile_f(request):
	if request.method=='POST':
		
			fname=request.POST['fname']
			lname=request.POST['lname']
			phone=request.POST['phone']
			address=request.POST['address']
			city=request.POST['city']
			email=request.POST['email']
			dob=request.POST['dob']
			country=request.POST['country']
			pincode=request.POST['pincode']
			user_id=user.objects.get(email=request.session['email'])
			far_id=farmer_details.objects.get(user_id=user_id)
			far_id.first_name=fname
			far_id.last_name=lname
			far_id.phone=phone
			far_id.address=address
			far_id.city=city
			far_id.dod=dob
			far_id.country=country
			far_id.pincode=pincode
			user_id.email=email
			user_id.save()
			far_id.save()
			return render(request,'profile_f.html',{'user':user_id,'far':far_id})

	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			return render(request,'profile_f.html',{'user':user_id})
		else:
			return render(request,'login.html')

def customer_det(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		cuscount=customer_details.objects.all()
		return render(request,'customer_det.html',{'user':user_id,'far':far_id,'cuscount':cuscount})
	else:
		return render(request,'login.html') 

def upload_product_f(request):
	if request.method=="POST":
		pic=request.FILES['pic']
		p_name=request.POST['pname']
		p_description=request.POST['pdescription']
		p_category=request.POST['pcategory']
		price=request.POST['price']
		p_quantity=request.POST['pquantity']
		user_id=user.objects.get(email=request.session['email'])
		f_id=farmer_details.objects.get(user_id=user_id)
		p_id=product.objects.filter(user_id=user_id,product_name=p_name)
		if p_id:
			msg="product in list"
			return render(request,'upload_product_f.html',{'user':user_id,'far':f_id,'msg':msg})
		else:
			far_id=product.objects.create(user_id=user_id,product_name=p_name,pro_description=p_description,pro_category=p_category,Price=price,pro_quantity=p_quantity,pic=pic)
			far_id=farmer_details.objects.get(user_id=user_id)
			pro_id=product.objects.filter(user_id=user_id)
			p=Paginator(pro_id,1)
			page=request.GET.get('page')
			pro_id=p.get_page(page)
			return render(request,'view_myproduct_f.html',{'user':user_id,'far':f_id,'pro':pro_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			far_id=farmer_details.objects.get(user_id=user_id)
			return render(request,'upload_product_f.html',{'user':user_id,'far':far_id})
		else:
			return render(request,'login.html')
def view_myproduct_f(request):
	if request.method=="POST":
		search=request.POST['search']
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		search_id=product.objects.filter(user_id=user_id,product_name__icontains=search)
		return render(request,'view_myproduct_f.html',{'user':user_id,'far':far_id,'search_id':search_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			far_id=farmer_details.objects.get(user_id=user_id)
			pro_id=product.objects.filter(user_id=user_id)
			p=Paginator(pro_id,2)
			page=request.GET.get('page')
			pro_id=p.get_page(page)
			return render(request,'view_myproduct_f.html',{'user':user_id,'far':far_id,'pro':pro_id})
		else:
			return render(request,'login.html')

def gallery_f(request):
	if request.method=="POST":
		search=request.POST['search']
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		search_id=agroproduct.objects.filter(product_name__icontains=search,enable='Enable')
		return render(request,'gallery_f.html',{'user':user_id,'far':far_id,'search_id':search_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			far_id=farmer_details.objects.get(user_id=user_id)
			pro_id=agroproduct.objects.filter(enable='Enable')
			return render(request,'gallery_f.html',{'user':user_id,'far':far_id,'pro':pro_id})
		else:
			return render(request,'login.html')

def productdetails_f(request, pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		p_id=product.objects.filter(id=pk)
		return render(request,'productdetails_f.html',{'user':user_id,'far':far_id,'product':p_id})
	else:
		return render(request,'login.html')

def update_product_f(request):
	if request.method=='POST':
		id=request.POST['id']
		price=request.POST['price']
		pquantity=request.POST['pquantity']
		enable=request.POST['enable']
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		pro_id=product.objects.filter(user_id=user_id)
		p_id=product.objects.get(id=id)
		p_id.Price=price
		p_id.pro_quantity=pquantity
		p_id.enable=enable
		p_id.save()
		p=Paginator(pro_id,2)
		page=request.GET.get('page')
		pro_id=p.get_page(page)
		return render(request,'view_myproduct_f.html',{'user':user_id,'far':far_id,'pro':pro_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			far_id=farmer_details.objects.get(user_id=user_id)
			pro_id=product.objects.filter(user_id=user_id)
			if pro_id:
				p=Paginator(pro_id,2)
				page=request.GET.get('page')
				pro_id=p.get_page(page)
				return render(request,'view_myproduct_f.html',{'user':user_id,'far':far_id,'pro':pro_id})
		else:
			return render(request,'login.html')

def p_details_f(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		pro_id=agroproduct.objects.get(id=pk,enable='Enable')
		return render(request,'p_details_f.html',{'user':user_id,'far':far_id,'pro':pro_id})
	else:
		return render(request,'login.html')

def addtocart_f(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		pro_id=agroproduct.objects.get(id=pk)
		p=int(pro_id.Price)
		addto_id= faraddtocart.objects.filter(p_id=pro_id,user_id=user_id)
		if addto_id:
			addto_id=faraddtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			return render(request,'addtocart_f.html',{'user':user_id,'far':far_id,'addtocart':addto_id,'totalamount':total_amount})
		else:
			add_id=faraddtocart.objects.create(p_id=pro_id,user_id=user_id,total_price=p,qty=1)
			add_id=faraddtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in add_id:
				total_amount=total_amount+i.total_price
			return render(request,'addtocart_f.html',{'user':user_id,'far':far_id,'addtocart':add_id,'totalamount':total_amount})
	else:
		return render(request,'login.html')

def addtodetails_f(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		addto_id= faraddtocart.objects.filter(user_id=user_id)
		total_amount=0
		for i in addto_id:
			total_amount=total_amount+i.total_price
		return render(request,'addtocart_f.html',{'user':user_id,'far':far_id,'addtocart':addto_id,'totalamount':total_amount})
	else:
		return render(request,'login.html')

def wishlist_f(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		pro_id=agroproduct.objects.get(id=pk)
		w_id= farwishlist.objects.filter(p_id=pro_id,user_id=user_id)
		if w_id:
			w_id=farwishlist.objects.filter(user_id=user_id)
			return render(request,'wishlist_f.html',{'user':user_id,'far':far_id,'wishlist':w_id})
		else:
			w_id=farwishlist.objects.create(p_id=pro_id,user_id=user_id)
			w_id=farwishlist.objects.filter(user_id=user_id)
			return render(request,'wishlist_f.html',{'user':user_id,'far':far_id,'wishlist':w_id})
	else:
		return render(request,'login.html')

def update_qty(request):
	if request.method=="POST":
		cart_id = request.POST['cart_id']
		qty = request.POST['qty']
		price = request.POST['price']
		if(faraddtocart.objects.filter(id=cart_id)):
			qty=int(qty)
			cart = faraddtocart.objects.get(id=cart_id)
			total=int(qty)*int(price)
			cart.total_price = total
			cart.qty=int(qty)
			cart.save()
			all_items = faraddtocart.objects.filter(user_id=cart.user_id)
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
		return render(request,'login.html')

def delete_record(request,pk):
	if 'email' in request.session:
		try:
			record = faraddtocart.objects.get(id =pk)
			record.delete()
			user_id=user.objects.get(email=request.session['email'])
			far_id=farmer_details.objects.get(user_id=user_id)
			addto_id= faraddtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			return render(request,'addtocart_f.html',{'user':user_id,'far':far_id,'addtocart':addto_id,'totalamount':total_amount})
		except:
			user_id=user.objects.get(email=request.session['email'])
			far_id=farmer_details.objects.get(user_id=user_id)
			addto_id= faraddtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			return render(request,'addtocart_f.html',{'user':user_id,'far':far_id,'addtocart':addto_id,'totalamount':total_amount})
	else:
		return render(request,'login.html')
		
def edit_img_f(request):
	if request.method=='POST':
		pic=request.FILES['pic']
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		far_id.img=pic
		far_id.save()
		return render(request,'profile_f.html',{'user':user_id,'far':far_id})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			return render(request,'profile_f.html',{'user':user_id})
		else:
			return render(request,'login.html')

def wdetails_f(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		w_id= farwishlist.objects.filter(user_id=user_id)
		return render(request,'wishlist_f.html',{'user':user_id,'far':far_id,'wishlist':w_id})
	else:
		return render(request,'login.html')

def orderpage_f(request,pk):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		try:
			pro_id=agroproduct.objects.get(id=pk,enable='Enable')
			if far_id.address=="None" or far_id.city=="None":
				msg="Please Edit your profile "
				return render(request,'profile_f.html',{'user':user_id,'far':far_id,'msg':msg})
			else:
				return render(request,'orderpage_f.html',{'user':user_id,'far':far_id,'pro':pro_id})
		except:
			user_id=user.objects.get(email=request.session['email'])
			far_id=farmer_details.objects.get(user_id=user_id)
			pro_id=agroproduct.objects.filter(enable='Enable')
			return render(request,'gallery_f.html',{'user':user_id,'far':far_id,'pro':pro_id})
	else:
		return render(request,'login.html')

def payment_f(request):
	if request.method=="POST":
		pquantity=request.POST['pquantity']
		totalpri=request.POST['totalpri']
		pid=request.POST['pid']
		address=request.POST['address']
		city=request.POST['city']
		pin=request.POST['pin']
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		pro_id=agroproduct.objects.get(id=pid)
		return render(request,'payment_f.html',{'user':user_id,'far':far_id,'pro':pro_id,'pquantity':pquantity,'totalpri':totalpri,'address':address,'city':city,'pin':pin})
	else:
		if 'email' in request.session:
			user_id=user.objects.get(email=request.session['email'])
			far_id=farmer_details.objects.get(user_id=user_id)
			pro_id=agroproduct.objects.filter(enable='Enable')
			return render(request,'gallery_f.html',{'user':user_id,'far':far_id,'pro':pro_id})
		else:
			return render(request,'login.html')

def initiate_payment(request):
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
        order_f(email,pquantity,pid,address,city,pin,amount,request)
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


def order_f(email,pquantity,pid,address,city,pin,amount,request):
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
	order_id = order_a.objects.filter(cus_id=user_id)
	for i in order_id:
		print("*"*20,i.orderdate)
	far_id=farmer_details.objects.get(user_id=user_id)
	far_id.address=address
	far_id.city=city
	far_id.pincode=pin
	far_id.save()
	pro_id=agroproduct.objects.get(id=pid)
	if int(pro_id.pro_quantity)>=int(pquantity):
		print("------------------------------>",pro_id.pro_quantity)
		order_id=order_a.objects.create(pid=pro_id,cus_id=user_id,totalpri=totalpri,quantity=pquantity,seller_id=pro_id.agro_id.user_id.email)
		quantity=int(pro_id.pro_quantity)-int(pquantity)
		pro_id=agroproduct.objects.get(id=pid)
		pro_id.pro_quantity=quantity
		pro_id.save()
		pro_id=agroproduct.objects.get(id=pid)
		if int(pro_id.pro_quantity)<=0:
			print("------------------------>")
			pro_id=agroproduct.objects.get(id=pid)
			pro_id.enable='Disable'
			pro_id.save()
	else:
		print("------------------------------>work not ")
		return render(request,'orderpage_f.html',{'user':user_id,'far':far_id,'pro':pro_id})

def addpayment_f(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		if far_id.address=="None" or far_id.city=="None" or far_id.pincode=="None":
			msg="Please Edit your profile "
			return render(request,'profile_f.html',{'user':user_id,'far':far_id,'msg':msg})
		else:
			addto_id= faraddtocart.objects.filter(user_id=user_id)
			total_amount=0
			for i in addto_id:
				total_amount=total_amount+i.total_price
			return render(request,'addpayment_f.html',{'user':user_id,'far':far_id,'addtocart':addto_id,'totalamount':total_amount})
	else:
		return render(request,'login.html')

def initiate_payment_addf(request):
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
        addto_id= faraddtocart.objects.filter(user_id=user_id)
        for i in addto_id:
        	order_f(email,i.qty,i.p_id.id,address,city,pin,i.total_price,request)
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

def myorder_f(request):
	if 'email' in request.session:
		user_id=user.objects.get(email=request.session['email'])
		far_id=farmer_details.objects.get(user_id=user_id)
		or_id=order_cus.objects.filter(seller_id=request.session['email'])
		return render(request,'myorder_f.html',{'user':user_id,'far':far_id,'order':or_id})
	else:
		return render(request,'login.html')