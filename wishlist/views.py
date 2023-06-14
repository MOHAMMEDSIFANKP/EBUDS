from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http.response import JsonResponse
from product.models import Product, Variations
from .models import Wishlist
# Create your views here.

# Wishlist
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user = request.user)
    context = {
        'wishlist' : wishlist,
    }
    return render(request, 'wishlist/wishlist.html',context)

# Add to wishlist
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('prod_id')
            variation_id =  request.POST.get('variation_id')
            product_check = Product.objects.get(id = prod_id)
            Variation_check = Variations.objects.get(id = variation_id)
            if(product_check):
                if(Wishlist.objects.filter(user = request.user, product = product_check, variation = Variation_check)):
                    return JsonResponse({'status' : "Product already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product = product_check, variation = Variation_check)
                    return JsonResponse({'status' : "Product Added to in wishlist"})
            else:
                JsonResponse({'status' : "No such product"})

        else:
            return JsonResponse({'status' : "Login to continue"})
    else:
        return JsonResponse('something went wrong, reload page',safe=False)
    
# Remove wishlist
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def deletewishlist(request):
    if request.method == 'POST':
        variant_id = int(request.POST.get('variant_id'))
        wishlist = Wishlist.objects.filter(user=request.user, variation=variant_id)
        if wishlist.exists():
            wishlist.delete()
    return redirect('wishlist')