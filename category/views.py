from django.shortcuts import render, redirect
import logging
from .models import category
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

# Create your views here.


# category
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminsignin')
def categories(request):
    category_data = category.objects.all().order_by('id')
    return render(request, 'category/category.html',{'category' : category_data})

# Crete category
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminsignin')
def createcategory(request):
    if request.method == 'POST':
        image = request.FILES.get('image', None)
        name = request.POST['categories']
        discrption = request.POST['categories_discription']
# validation
        if name.strip() =='':
            messages.error(request,'Image Not Fount')
            return redirect('categories')
        if not image:
            messages.error(request, "Image not uploaded")
            return redirect('categories')
# Save
        categr = category(categories=name,categories_discription = discrption,categories_image=image)
        categr.save()
        return redirect('categories')
    

# Edit Category
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminsignin')
def editcategory(request, editcategory_id):
    if request.method == 'POST':
        name = request.POST['categories']
        discrption = request.POST['categories_discription']

# validation
        try:
            caterg = category.objects.get(id=editcategory_id)
            image = request.FILES.get('image')
            if image:
                caterg.categories_image = image
                caterg.save()
        except category.DoesNotExist:
            messages.error(request,'Image Not Fount')
            return redirect('categories')
        if name.strip() == '':
            messages.error(request,'Name field is empty')
            return redirect('categories')
        
        categr = category.objects.get(id=editcategory_id)
        categr.categories = name
        categr.categories_discription = discrption
        categr.save()
        return redirect ('categories')

# Delete Category
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminsignin')
def deletecategory(request,deletecategory_id):
    categre = category.objects.get(id=deletecategory_id)
    categre.delete()
    return redirect('categories')

# Search Category
def search_category(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            cate = category.objects.filter(categories__icontains=keyword).order_by('id')
            if cate.exists():
                context = {
                    'category': cate,
                }
                return render(request, 'category/category.html', context)
            else:
                message = "Category not found"
                return render(request, 'category/category.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'category/category.html', {'message': message})
    else:
        return render(request, '404.html')