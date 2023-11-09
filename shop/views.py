from django.shortcuts import render,get_object_or_404, redirect
from category.models import category
from dashboard.models import brand
from product.models import Product, Color, Variations, PriceFilter
from django.http import Http404
from django.contrib import messages
from django.http.response import JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import *
# Create your views here.

#  Shop view
def shop(request,category_slug=None):
    categories = None
    products = None
    brand_id = request.GET.get('brand')
    filters = request.GET.get('filters')
    sort = request.GET.get('sort')
    color = request.GET.get('color')

    # Brand filter
    if brand_id:
        variation = Variations.objects.filter(product__brand = brand_id)
        paginator = Paginator(variation, 6)
    # Price range
    elif filters:
        variation = Variations.objects.filter(product__brand = brand_id)
        products = Product.objects.filter(price_range=filters)
        if not products:
            message = "No item available in this Price range."
            return render(request, 'user/shop.html', {'message': message})
        for product in products:
            product_id = product.id
            variation = Variations.objects.filter(product = product_id).order_by('id')
            paginator = Paginator(variation, 6)

    # Category filter
    elif category_slug is not None:
        categories = get_object_or_404(category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        if not products:
            message = "No item available in this category ."
            return render(request, 'user/shop.html', {'message': message})
        for product in products:
            product_id = product.id
            variation = Variations.objects.filter(product = product_id).order_by('id')
            paginator = Paginator(variation, 6)
    # Sorted by AtoZ
    elif sort == 'atoz':            
        variation = Variations.objects.all().order_by('product__product_name')
        paginator = Paginator(variation, 6)
    # Sorted by BtoZ
    elif sort == 'ztoa':
        variation = Variations.objects.all().order_by('-product__product_name')
        paginator = Paginator(variation, 6)
    # Sorted by Low to High
    elif sort == 'ltoh':
        variation = Variations.objects.all().order_by('product__product_price')
        paginator = Paginator(variation, 6)
    # Sorted by High to Low   
    elif sort == 'htol':
        variation = Variations.objects.all().order_by('-product__product_price')
        paginator = Paginator(variation, 6)
    elif color:
        variation = Variations.objects.filter(color=color)
        if not variation:
            message = "No item available in this Color."
            return render(request, 'user/shop.html', {'message': message})
        print(variation,'daxooo')
        paginator = Paginator(variation, 6)

    else:
    
    # All Products
        variation = Variations.objects.all().order_by('id')
        paginator = Paginator(variation, 6)
    page = request.GET.get('page')
    paged_variation = paginator.get_page(page)
    variation_count = variation.count()
    categories = category.objects.all()
    brands = brand.objects.all()
    dict_products = {
        'variations': paged_variation,
        'cate' : categories,
        'productcount' : variation_count,
        'brands' : brands,
        'PriceFilter' : PriceFilter.objects.all(),
    }
    return render(request, 'user/shop.html', dict_products)

#  view Single images
class signle(View):

    template_name = 'user/single_product.html'

    def get(self,request, var_id):
        try:
            variation = Variations.objects.get(id=var_id)
            variation_list = Variations.objects.filter(product=variation.product.id)
            context = {
                'color': Color.objects.all(),   
                'variation': variation,
                'variation_list' : variation_list,
            }
            return render(request, self.template_name, context)
        except Variations.DoesNotExist:
            return render(self,request, 'error/index.html')
        
    def post(self,request,var_id):
        color_id = request.POST.get('colors')
        prod_id = request.POST.get('prod_id')
        variation = Variations.objects.get(color=color_id, product=prod_id)
        variation_quantity = variation.quantity
        return JsonResponse({'variation_id':variation.id, 'variation_quantity':variation_quantity})
    

# Search
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('id').filter(product_name__icontains=keyword)
            if products.exists():
                product_ids = products.values_list('id', flat=True)
                variation = Variations.objects.filter(product__in=product_ids).order_by('id')
                products_count = variation.count()
                context = {
                    'variations': variation,
                    'cate': category.objects.all(),
                    'productcount': products_count,
                }
                return render(request, 'user/shop.html',context)
            else:
                message = "Product not found."
                return render(request, 'user/shop.html', {'message': message})
        else:
            message = "Please enter a valid search keyword."
            return render(request, 'user/shop.html', {'message': message})
    else:
        return render(request, '404.html')

