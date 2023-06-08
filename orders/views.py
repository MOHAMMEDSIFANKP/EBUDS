from django.shortcuts import render, redirect
from checkout.models import Order, OrderItem
from product.models import Product, Variations
from .models import Orderreturn
from userprofile.models import Wallet, Address
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404


# Create your views here.

# Order
def orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    orderitems = OrderItem.objects.filter(order__in=orders).order_by('-order__update_at')

    context = {
        'orders': orders,
        'orderitems': orderitems,
    }
    return render(request, 'orders/orders.html', context)

# Order Cancell
def ordercancel(request):
    orderid = int(request.POST.get('order_id'))
    orderitem_id = request.POST.get('orderitem_id')
    orderitem = OrderItem.objects.filter(id=orderitem_id).first()
    
    order = Order.objects.filter(id=orderid).first()
    qty = orderitem.quantity
    pid = orderitem.variation.id
    variation = Variations.objects.filter(id=pid).first()
    
    if order.payment_mode == 'Razorpay':
        order = Order.objects.get(id=orderid)
        total_price = order.total_price

        try:
            wallet = Wallet.objects.get(user=request.user)
            wallet.wallet += total_price
            wallet.save()
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=request.user, wallet=total_price)
    # Update the product quantity
    variation.quantity = variation.quantity + qty
    variation.save()
    orderitem.quantity = 0
    orderitem.status = 'Cancelled'
    orderitem.save()
    return redirect('orders')

def vieworderdetail(request,orderitem_id):
    try:
        order_item = OrderItem.objects.get(id=orderitem_id)
    except OrderItem.DoesNotExist:
        messages.error(request, "The specified OrderItem does not exist.")
        return redirect('orders')
    address = int(order_item.order.address.id)
    cotext = {
        'address': Address.objects.get(id=address),
        'order_item' : order_item,
    }
    return render(request, 'orders/vieworder.html',cotext)

def orderreturn(request,return_id):
    if request.method == 'POST':
        print(return_id,'daxo')
        options = request.POST.get('options')
        reason = request.POST.get('reason')
# validation
        if options.strip() == '':
            messages.error(request, "enter valid Options")
            return redirect('vieworderdetail')
        try:
            orderitem_id = OrderItem.objects.get(id=return_id)
        except OrderItem.DoesNotExist:
            messages.error(request, "The specified OrderItem does not exist.")
            return redirect('orders')
        qty = orderitem_id.quantity
        pid = orderitem_id.variation.id
        order_id = Order.objects.get(id = orderitem_id.order.id)
        variation = Variations.objects.filter(id=pid).first()
        variation.quantity = variation.quantity + qty
        variation.save()
        orderitem_id.status = 'Return'
        total_p = orderitem_id.price
        print(total_p)
        orderitem_id.save()
        returnorder = Orderreturn.objects.create(user = request.user, order = order_id, options=options, reason=reason)
        try:
            wallet = Wallet.objects.get(user=request.user)
            wallet.wallet += total_p
            wallet.save()
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=request.user, wallet=total_p)
        orderitem_id.quantity = 0
        orderitem_id.price = 0
        orderitem_id.save()
        return redirect('vieworderdetail',return_id)

# Admin side Order View
def orderdetails(request):
    orders = Order.objects.all()
    orderitems = OrderItem.objects.filter(order__in=orders).order_by('-order__update_at')
    context = {
        'orders': orders,
        'orderitems': orderitems,
    }
    return render(request, 'orders/admin_orders.html',context)

# Admin side Order satus change
def changestatus(request):
    orderitem_id = request.POST.get('orderitem_id')
    order_status = request.POST.get('order_status')
    orderitems = OrderItem.objects.get(id = orderitem_id)

    orderitems.status = order_status
    orderitems.save()
    return JsonResponse({'status': "Updated"+ str(order_status) + "successfully"}) 

def trackorder(request):
    # print(order_id)
    # order = get_object_or_404(Order, id=order_id)
    

    # statusIndex = { 'Pending':1,
    #   'Processing':2,
    #   'Shipped':3,
    #   'Delivered':4,
    #   'Cancelled':5,
    #   }

    # trackIndex = 0
    # for value,idx in statusIndex.items():
    #       if value.lower() == order.status.lower():
    #         trackIndex = idx 
    
    # context = {
    #     'order': order,

    #     'trackIndex':trackIndex
    # }
    
    return render(request, 'orders/trackorder.html')

# admin side order search
def search_orders(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            Orders = Order.objects.filter(
                Q(tracking_no__icontains=keyword) |
                Q(id__icontains=keyword)
            ).order_by('id')
            if Orders.exists():
                context = {
                    'orderitems': OrderItem.objects.filter(order__in=Orders),
                }
                return render(request, 'orders/admin_orders.html', context)
            else:
                message = "not found."
                return render(request, 'orders/admin_orders.html', {'message': message})
        else:
            message = "Please enter a valid search keyword."
            return render(request, 'orders/admin_orders.html', {'message': message})
    else:
        return render(request, '404.html')