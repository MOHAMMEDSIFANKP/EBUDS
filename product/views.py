from django.shortcuts import render,redirect
from category.models import category
from django.contrib import messages
from .models import Product as products, Variations, Color, PriceFilter
from dashboard.models import brand
import logging

# Create your views here.

# Product
def product(reqeust):
    prodec = products.objects.all().order_by('id')
    dict_list={
        'prod' : prodec,
        'category' : category.objects.all(),
        'brand': brand.objects.all(),
        'price_range' : PriceFilter.objects.all()
    }
    return render(reqeust ,'product/product.html',dict_list)

# Add Product
def createproduct(request):
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['product_price']
        description = request.POST['product_description']
        brandname = request.POST.get('brand')
        category_id = request.POST.get('category')
        price_range = request.POST.get('price_range')

# Validaiton
        if products.objects.filter(product_name=name).exists():
            messages.error(request, 'Product name already exists')
            return redirect('product')
        try:
            is_availables = request.POST.get('checkbox', False)
            if is_availables == 'on':
                is_availables = True
            else:
                is_availables = False
        except:
            is_availables = False

        if name == '' or price =='' :
            messages.error(request, "Name or Price field are empty")
            return redirect('product')

        categeryid  = category.objects.get(id=category_id)
        brandid = brand.objects.get(brand_name=brandname)
        prange = PriceFilter.objects.get(id=price_range)


# Save        
        produc = products(
            product_name=name,
            product_price=price,
            product_description = description,
            is_available = is_availables,
            brand = brandid,
            category = categeryid,
            price_range =prange,
        )
        
        produc.save()
        return redirect('product')
    return render(request, 'product/product.html' )


# Edit Product
def editproduct(request,editproduct_id):
    if request.method == 'POST':
        pname = request.POST['product_name']
        pprice = request.POST['product_price']
        cdescription = request.POST['product_description']
        brandname = request.POST.get('brand')
        category_id = request.POST.get('category')
        price_range = request.POST.get('price_range')
# validation
        try:
            is_availables = request.POST.get('checkbox', False)
            if is_availables == 'on':
                is_availables = True
            else:
                is_availables = False
        except:
            is_availables = False

        if pname == '' or pprice =='' :
            messages.error(request, "Name or Price field are empty")
            return redirect('product')
        
        cates = category.objects.get(id=category_id)
        produc = brand.objects.get(brand_name=brandname)
        prange = PriceFilter.objects.get(id=price_range)
# Save       
        cat = products.objects.get(slug=editproduct_id)
        cat.product_name = pname
        cat.price_range = prange
        cat.product_price = pprice
        cat.product_description = cdescription
        cat.is_available = is_availables
        cat.brand = produc
        cat.category = cates
        cat.save()
        return redirect('product')

# Edit Delete
def deleteproduct(reqeust,deleteproduct_slug):
    pro = products.objects.get(slug=deleteproduct_slug)
    pro.delete()
    return redirect('product')
# Variations
def variations(request):
    dict_list={
        'prodect' : products.objects.all(),
        'color' : Color.objects.all(),
        'variation' : Variations.objects.all()
    }
    return render(request, 'product/variations.html',dict_list)

# Add Variations
def createvariations(request):
    if request.method == 'POST':
        product_id = request.POST['product']
        color = request.POST['color']
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        image3 = request.FILES.get('image3', None)
        quantity = request.POST.get('qty')

#  Validation
        product = products.objects.get(id=product_id)
        colors = Color.objects.get(color=color)
        if Variations.objects.filter(product = product, color=colors).exists():
            messages.error(request, 'This variant already EXIST')
            return redirect('variations')
        if not image1:
            messages.error(request, 'Image 1 not upload')
        if not image2:
            messages.error(request, 'Image 2 not upload')
        if not image3:
            messages.error(request, 'Image 3 not upload')
        if quantity == '':
            messages.error(request,'Quantity is blank')
            return redirect('variations')
            # Check if all images are uploaded
        if image1 and image2 and image3:
            variation = Variations()
            variation.image1 = image1
            variation.image2 = image2
            variation.image3 = image3
            variation.product = product
            variation.color = colors
            variation.quantity = quantity
            variation.save()

        return redirect('variations')


# Edit Variations
def editvariations(request, edit_id):
    if request.method == 'POST':
        product = request.POST['product']
        color = request.POST['color']
        quantity = request.POST.get('qty')
# validation
        try:
            variation = Variations.objects.get(id=edit_id)
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            try:
                image1 = request.FILES['image1']
                variation.image1 = image1
                variation.save()
            except:
                pass 
            try:
                image2 = request.FILES['image2']
                variation.image2 = image2
                variation.save()
            except:
                pass 
            try:
                image3 = request.FILES['image3']
                variation.image3 = image3
                variation.save()
            except:
                pass 
        except Variations.DoesNotExist:
            messages.error(request, "Image not found")
            return redirect('variations')
        if quantity == '':
            messages.error(request,'Quantity is blank')
            return redirect('variations')

        product = products.objects.get(id=product)
        colors = Color.objects.get(color=color)
# Save       
        variation = Variations.objects.get(id=edit_id)
        variation.product = product
        variation.color = colors
        variation.quantity = quantity
        variation.save()
        return redirect('variations')

# Delete Variations
def deletevariations(request, delet_id):
    variation = Variations.objects.get(id = delet_id)
    variation.delete()
    return redirect('variations')

# Search Product
def search_product(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            Prod = products.objects.filter(product_name__icontains=keyword).order_by('id')
            if Prod.exists():
                context = {
                    'prod': Prod,
                }
                return render(request, 'product/product.html',context)
            else:
                message = "Product not found."
                return render(request,'product/product.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'product/product.html', {'message': message})
    else:
        return render(request, '404.html')
    
# Search Variations
def search_variations(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            variation = Variations.objects.filter(product__icontains=keyword).order_by('id')
            if variation.exists():
                context = {
                    'variation': variation,
                }
                return render(request, 'product/variations.html',context)
            else:
                message = "Variation not found."
                return render(request,'product/variations.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'product/variations.html', {'message': message})
    else:
        return render(request, '404.html')
