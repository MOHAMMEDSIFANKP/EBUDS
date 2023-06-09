from django.shortcuts import render
from dashboard.models import brand
from dashboard.models import banner
from product.models import Product, Variations
from category.models import category
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render


# Create your views here.

def home(request):
    Banner = banner.objects.all()
    categories = category.objects.all()
    Brands = brand.objects.all()
    print(banner,'daxo')
    dict_banner = {
        'banner' : Banner,
        'category' : categories,
        'user' : User.objects.all(),
        'brand' : Brands,
        'Variations' : Variations.objects.all().order_by('id')
    }
    return render(request,'user/index.html',dict_banner)

def error_404_view(request,exception):
    return render(request,'error/index.html')