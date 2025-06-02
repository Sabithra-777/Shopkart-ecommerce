from http.client import HTTPResponse
from django.http import JsonResponse
from django.shortcuts import redirect,render
from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})
def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,"shop/fav.html",{"fav":fav})
    else:
        return redirect("/")
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect("/")
def remove_fav(request,fid):
    item=Favourite.objects.get(id=fid)
    item.delete()
    return redirect("/favviewpage")  
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")  
def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user,product_id=product_id):
                     return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200) 
def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user,product_id=product_id):
                     return JsonResponse({'status':'Product Already in Favourite'},status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product Added to Favourite'},status=200) 
        else:
            return JsonResponse({'status':'Login to Add Favourite'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect("/")
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get("username")
            pwd=request.POST.get("password")
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect("/")
            else:
                 messages.error(request,"Invalid User Name or Password")
                 return redirect("/login")
        return render(request,"shop/login.html")  
    
def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You can Login Now..!")
            return redirect('/login')
    return render(request,"shop/register.html",{'form':form})
def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"shop/collections.html",{"catagory":catagory})
def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,"shop/products/index.html",{"products":products,"category_name":name})
    else:
        messages.warning(request,"No such Catagory Found")
        return redirect('collections')
def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_details.html",{"products":products})   
        else:
            messages.error(request,"No Such Product Found")
            return redirect('collections')
    else:
        messages.error(request,"No Such Catagory Found")
        return redirect('collections')

@login_required
def wallet_page(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    return render(request, "shop/wallet.html", {"balance": wallet.balance})

@login_required
def buy_now(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        data = json.load(request)
        product_qty = data.get('product_qty')
        product_id = data.get('pid')
        try:
            product = Product.objects.get(id=product_id)
            wallet, created = Wallet.objects.get_or_create(user=request.user)
            total_price = product.selling_price * product_qty
            if wallet.balance >= total_price:
                if product.quantity >= product_qty:
                    wallet.balance -= total_price
                    wallet.save()
                    # Optionally, create an order record here
                    return JsonResponse({'status': 'Order confirmed'}, status=200)
                else:
                    return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
            else:
                return JsonResponse({'status': 'Insufficient balance'}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'status': 'Product not found'}, status=404)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)

@login_required
def wallet_topup(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            try:
                amount = float(amount)
                if amount <= 0:
                    messages.error(request, "Amount must be positive.")
                else:
                    wallet, created = Wallet.objects.get_or_create(user=request.user)
                    wallet.balance += amount
                    wallet.save()
                    messages.success(request, f"Rs. {amount} added to your wallet successfully.")
            except ValueError:
                messages.error(request, "Invalid amount entered.")
        else:
            messages.error(request, "Amount is required.")
    return redirect('wallet')
