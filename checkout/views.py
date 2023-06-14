from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from carts.models import Cart
from userprofile.models import Address, Wallet
from django.contrib import messages
from product.models import Product, Variations
from checkout.models import Order, OrderItem
from coupon.models import Usercoupon, Coupon
from django.shortcuts import render, redirect
import random

# Create your views here.

# Checkout
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def checkout(request):
    drowcart = Cart.objects.filter(user = request.user)
    for item in drowcart:
        if item.product_qty > item.variation.quantity:
            error_message = 'Only few quantity not allowed ' + str(item.product_qty) + ' quantity'
            return JsonResponse({'error_message': error_message})
            
    cartitems = Cart.objects.filter(user = request.user)
    coupon_code = request.POST.get('coupon_code')
    total_price = 0
    grand_total = 0
    tax = 0  
    for item in cartitems:
        if item.product.offer == None:
            total_price = total_price + item.product.product_price * item.product_qty
            tax = total_price * 0.18
            grand_total = total_price + tax
        else:
            total_price = total_price + item.product.product_price * item.product_qty
            total_price = total_price - item.product.offer.discount_amount
            tax = total_price * 0.18
            grand_total = total_price + tax
    address = Address.objects.filter(user = request.user)
    usercoupon = Usercoupon.objects.filter(user=request.user).last()
    coupons = Coupon.objects.all()
    context = {
        'cartitems' : cartitems,
        'total_price' : total_price,
        'grand_total' : grand_total,
        'address' : address,
        'usercoupon': usercoupon,
        'coupons'  :coupons,
    }
    return render(request,'checkout/checkout.html',context)

# Place order
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def placeorder(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.user
        address_id = request.POST.get('address')
        if address_id is None:
            messages.error(request, 'Address fields is mandatory!')
            return redirect('checkout')
        address = Address.objects.get(id=address_id)
        neworder.address = address
        neworder.payment_mode = request.POST.get('payment_method')
        neworder.payment_id = request.POST.get('payment_id')
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        tax = 0
        for item in cart:
            if item.product.offer == None:
                cart_total_price += item.product.product_price * item.product_qty
                tax = cart_total_price * 0.18
                cart_total_price +=tax
            else:
                cart_total_price += item.product.product_price * item.product_qty
                cart_total_price -= item.product.offer.discount_amount
                tax = cart_total_price * 0.18
                cart_total_price +=tax
        payment = request.POST.get('payment_method')
        if (payment == "wallet"):
            try:
                wallet = Wallet.objects.get(user=request.user)
            except Wallet.DoesNotExist:
                wallet = Wallet.objects.create(user=request.user, wallet=0)

            if wallet.wallet >= cart_total_price:
                wallet.wallet = wallet.wallet - cart_total_price
                wallet.save()
            else:
                messages.error(request, 'Your wallet amount is very low')
                return redirect('checkout')

        if Usercoupon.objects.filter(user = request.user).exists():
            usercoupon = Usercoupon.objects.get(user = request.user)
            neworder.total_price = usercoupon.total_price
            usercoupon.delete()
        else:
            neworder.total_price = cart_total_price
        trackno = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.product_price,
                quantity=item.product_qty,
                variation = item.variation,
            )

            # To decrease the product quantity from available stock
        variation = Variations.objects.filter(id=item.variation.id).first()
        variation.quantity = variation.quantity - item.product_qty
        variation.save()
        payment_mode = request.POST.get('payment_method')
        if (payment_mode == "Razorpay"):
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse({'status' : "Yout order has been placed successfully"})
# To clear user Cart
        Cart.objects.filter(user=request.user).delete()

    return redirect('checkout')

# Add Checkout Addres
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def addcheckoutaddr(request):
    if request.method == 'POST':
        address = Address()
        address.user = request.user
        address.first_name = request.POST.get('firstname')
        address.last_name = request.POST.get('lastname')
        address.country = request.POST.get('country')
        address.address = request.POST.get('address')
        address.city = request.POST.get('city')
        address.pincode = request.POST.get('pincode')
        address.phone = request.POST.get('phone')
        address.email = request.POST.get('email')
        address.state = request.POST.get('state')
        address.order_note = request.POST.get('ordernote')
        address.payment_mode = request.POST.get('payment_method')
        address.save()

        return redirect('checkout')
    return redirect('checkout')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def deleteaddresscheckout(request,delete_id):
    address = Address.objects.filter(id=delete_id)
    address.delete()
    return redirect('placeorder')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def razarypaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        if item.product.offer == None:
            total_price = total_price + item.product.product_price * item.product_qty
            tax = total_price * 0.18
            grand_total += total_price+tax
        else:
            total_price += item.product.product_price * item.product_qty
            total_price -= item.product.offer.discount_amount
            tax = total_price * 0.18
            total_price +=tax
    return JsonResponse({'total_price': total_price})

