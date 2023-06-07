from django.shortcuts import render, redirect
from checkout.models import Order, OrderItem
from product.models import Product, Variations
from userprofile.models import Wallet
from django.http.response import JsonResponse
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
    orderitem.save()
    order.status = 'Cancelled'
    order.save()
    return redirect('orders')

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
    order_id = request.POST.get('order_id')
    order_status = request.POST.get('order_status')
    order = Order.objects.get(id = order_id)
    order.status = order_status
    order.save()
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