from django.shortcuts import render, redirect
from dashboard.models import brand
from dashboard.models import banner
from product.models import Product, Variations
from category.models import category
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render
from dashboard.models import Contact_us
from django.contrib import messages


# Create your views here.

def home(request):
    Banner = banner.objects.all()
    categories = category.objects.all()
    Brands = brand.objects.all()
    print(banner,'sifan')
    dict_banner = {
        'banner' : Banner,
        'category' : categories,
        'user' : User.objects.all(),
        'brand' : Brands,
        'Variations' : Variations.objects.all().order_by('id')
    }
    return render(request,'user/index.html',dict_banner)

# Contact Us
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact_us = Contact_us.objects.create(name=name,email=email,text=message)
        contact_us.save()
        messages.success(request,"Thank you for Your information")
        return redirect('contact')
    return render(request,'contact_us/contact.html')
# admin contact us
def admin_contact(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    contact = Contact_us.objects.all()
    context = {
        'contact':contact,
    }
    return render(request,'contact_us/contact_us.html',context)

def search_contact(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            users = Contact_us.objects.filter(name__icontains=keyword).order_by('id')
            if users.exists():
                context = {
                    'contact': users,
                }
                return render(request, 'contact_us/contact_us.html', context)
            else:
                message = "User not found."
                return render(request, 'contact_us/contact_us.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'contact_us/contact_us.html', {'message': message})
    else:
        return render(request, 'error/index.html')
def error_404_view(request,exception):
    return render(request,'error/index.html')