from django.shortcuts import render
from .models import Coupon, Usercoupon
from django.http.response import JsonResponse
# Create your views here.

def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        grand_total = float(request.POST.get('grand_total', 0))  # Convert to float
        
        if coupon_code.strip() == '':
            return JsonResponse({'status': 'Field is blank'})
        
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code, active=True)
        except Coupon.DoesNotExist:
            return JsonResponse({'status': 'Coupon does not exist'})
        
        if Usercoupon.objects.filter(user=request.user, coupon__coupon_code=coupon_code).exists():
            return JsonResponse({'status': 'Coupon already used!'})
        
        if grand_total > coupon.min_value:
            coupon_discount = coupon.discount
            grand_total = grand_total - (grand_total * (coupon.discount / 100))
            usercoupon = Usercoupon.objects.create(user=request.user, coupon=coupon, used=True, total_price = grand_total)
            usercoupon.save()
            print(grand_total,'hiii')
            return JsonResponse({'status': 'Coupon added successfully', 'coupon_discount': coupon_discount, 'grand_total': grand_total,})
        else:
            return JsonResponse({'status': 'You are not eligible for this coupon'})
            
    return JsonResponse({'status': 'Invalid request'})

def admincoupon(request):
    context = {
        'coupon' : Coupon.objects.all()
    }
    return render (request,'coupon/coupon.html',context)
            
