from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart
from wishlist.models import Wishlist
from product.models import Product, Variations
from django.http.response import JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

# Create your views here.

# Add to cart
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def add_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            variation_id = request.POST.get('variation_id')
            prod_id = request.POST.get('prod_id')
            try:
                product_check = Product.objects.get(id=prod_id)
                variation_check = Variations.objects.get(id = variation_id )

            except Product.DoesNotExist:
                return JsonResponse({'status': 'No such product found'})

            if Cart.objects.filter(user=request.user, product_id=prod_id, variation = variation_check).exists():
                return JsonResponse({'status': 'Product already in Cart'})
            else:
                prod_qty = int(request.POST.get('product_qty'))
                if variation_check.quantity >= prod_qty:
                    Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty,  variation = variation_check)
                    try:
                        if Wishlist.objects.filter(user = request.user, product = prod_id, variation= variation_check).exists():
                            wishlist = Wishlist.objects.filter(user = request.user, product = prod_id, variation= variation_check)
                            wishlist.delete()
                    except:
                        pass
                    return JsonResponse({'status': 'Product added successfully'})
                else:
                    return JsonResponse({'status': "Only"+ str(variation_check.quantity) + "quantity available"})
        else:
            return JsonResponse({'status': 'Login to continue'})
    return redirect('single')

# Cart
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def cart(request):
    cart = Cart.objects.filter(user = request.user).order_by('id')
    total_price = 0
    tax = 0
    grand_total =0
    single_product_total = [0]
    for item in cart:
        total_price = total_price + item.product.product_price * item.product_qty
        single_product_total.append(item.product.product_price * item.product_qty)
        tax = total_price * 0.18
        grand_total = total_price + tax


    context = {
        'cart' : cart,
        'total_price' : total_price,
        'tax' : tax,
        'grand_total' : grand_total,
        'single_product_total':single_product_total,
    }
    return render(request,'cart/cart.html',context)

# Update cart quantity
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def update_cart(request):
    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        if (Cart.objects.filter(user=request.user, variation=variant_id)):
            prod_qty = request.POST.get('product_qty')
            cart = Cart.objects.get(variation=variant_id, user=request.user)
            cartes = cart.variation.quantity
            if int(cartes) >= int(prod_qty):
                cart.product_qty = prod_qty
                cart.save()

                carts = Cart.objects.filter(user = request.user).order_by('id')
                total_price = 0
                for item in carts:
                    total_price = total_price + item.product.product_price * item.product_qty

                return JsonResponse({'status': 'Updated successfully','sub_total':total_price,'product_price':cart.product.product_price,'quantity':prod_qty})
            else:
                return JsonResponse({'status': 'Not quantity'})
    return JsonResponse('something went wrong, reload page',safe=False)

# Deletecart
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def deletecartitem(request):
    if request.method == 'POST':
        variant_id = int(request.POST.get('variant_id'))
        cart_items = Cart.objects.filter(user=request.user, variation=variant_id)
        if cart_items.exists():
            cart_items.delete()
    return redirect('cart')


        

