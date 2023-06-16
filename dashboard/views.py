from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from category.models import category
from .models import brand, banner as banners
from product.models import Offer
from checkout.models import *
from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.db.models import DateField
from django.db.models.functions import Cast
from datetime import datetime,timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout

# verification email
from registration.models import UserOTP
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from django.core.exceptions import ValidationError

def adminsignin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        # Validation
        if email.strip() == '' or password.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('adminsignin')

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('dashboard')
            else:
                messages.error(request, "You are not a superuser")
                return redirect('adminsignin')

        messages.error(request, "Invalid email or password")
        return redirect('adminsignin')

    return render(request, 'admin/adminsignin.html')

# validations
def validateEmail(email):
    from django.core.validators import validate_email
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False
    
def validate_name(value):
    if not re.match(r'^[a-zA-Z\s]*$', value):
        return 'Name should only contain alphabets and spaces'
    
    elif value.strip() == '':
        return 'Name field cannot be empty or contain only spaces' 
    elif User.objects.filter(username=value).exists():
        return 'Usename already exist'
    else:
        return False
    
    

# Create your views here.


# Signup
def adminsignup(request):
    # OTP VERIFICATION

    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_email = request.POST.get('email')
            usr = User.objects.get(email=get_email)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.is_superuser = True
                usr.save()  # Save the changes to the user object
                auth.login(request, usr)
                messages.success(request, f'Account is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('dashboard')
            else:
                messages.warning(request, 'You Entered a wrong OTP')
                return render(request, 'admin/adminsignup.html', {'otp': True, 'usr': usr})

        # User registration validation
        else:
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            # Null values checking
            check = [email, password1, password2]
            for value in check:
                if value == '':
                    context = {
                        'pre_email': email,
                        'pre_password1': password1,
                        'pre_password2': password2,
                    }
                    messages.info(request, 'Some fields are empty')
                    return render(request, 'admin/adminsignup.html', context)

            result = validateEmail(email)
            if not result:
                context = {
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2,
                }
                messages.info(request, 'Enter a valid email')
                return render(request, 'admin/adminsignup.html', context)

            Pass = ValidatePassword(password1)
            if not Pass:
                context = {
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2,
                }
                messages.info(request, 'Enter a strong password')
                return render(request, 'admin/adminsignup.html', context)

            if password1 == password2:
                try:
                    User.objects.get(email=email)
                except User.DoesNotExist:
                    usr = User.objects.create_user(username=email, email=email, password=password1)
                    usr.is_active = False
                    usr.is_superuser = True
                    usr.save()
                    
                    user_otp = random.randint(100000, 999999)
                    UserOTP.objects.create(user=usr, otp=user_otp)
                    mess = f'Hello {usr.username},\nYour OTP to verify your account for EBUDS is {user_otp}\nThanks!'
                    send_mail(
                        "Welcome to EBUDS: Verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                    return render(request, 'admin/adminsignup.html', {'otp': True, 'usr': usr})
                else:
                    context = {
                        'pre_email': email,
                        'pre_password1': password1,
                        'pre_password2': password2,
                    }
                    messages.error(request, 'Email already exists')
                    return render(request, 'admin/adminsignup.html', context)
            else:
                context = {
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2,
                }
                messages.error(request, 'Password mismatch')
                return render(request, 'admin/adminsignup.html', context)
    else:
        return render(request, 'admin/adminsignup.html')


# Create your views here.
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')

    delivered_items = OrderItem.objects.filter(status='Delivered')

    revenue = 0
    for item in delivered_items:
        revenue += item.order.total_price

    top_selling = OrderItem.objects.annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').distinct()[:5]

    recent_sale = OrderItem.objects.all().order_by('-id')[:5]

    today = datetime.today()
    date_range = 7

    four_days_ago = today - timedelta(days=date_range)

    orders = Order.objects.filter(created_at__gte=four_days_ago, created_at__lte=today)

    sales_by_day = orders.annotate(day=TruncDay('created_at')).values('day').annotate(total_sales=Sum('total_price')).order_by('day')
    sales_dates = Order.objects.annotate(sale_date=Cast('created_at', output_field=DateField())).values('sale_date').distinct()

    context = {
        'total_users':User.objects.count(),
        'sales':OrderItem.objects.count(),
        'revenue':revenue,
        'top_selling':top_selling,
        'recent_sales':recent_sale,
        'sales_by_day':sales_by_day,
    }
    return render(request,'admin/dashboard.html',context)

# user
def user(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    user_data = User.objects.all().order_by('id')
    return render(request,'admin/user.html',{'users': user_data})


# Block User
def blockuser(request,user_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('user')

# brand

def brands(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    brand_data = brand.objects.all().order_by('id')
    return render(request, 'brand/brand.html',{'brand' : brand_data})

# Crete brand
def createbrands(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if request.method == 'POST':
        cname = request.POST.get('brand_name', '')
        eimage = request.FILES.get('brand_image', None)
        address = request.POST['brand_address']
        cdescription = request.POST['brand_discription']

        # Validation
        if cname.strip() == '':
            messages.error(request, "Name Field empty")
            return redirect('brands')

        if not eimage:
            messages.error(request, "Image not uploaded")
            return redirect('brands')

        bran = brand(
            brand_name=cname,
            brand_image=eimage,
            brand_address=address,
            brand_discription=cdescription,
        )
        bran.save()
        return redirect('brands')

    return render(request, 'brand/createbrands.html')


# Edit Brand
def editbrands(request, editbrands_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if request.method == 'POST':
        cname = request.POST['brand_name']
        address = request.POST['brand_address']
        cdescription = request.POST['brand_discription']
# validation
        if cname.strip() == '':
            messages.error(request, "Name Field empty")
            return redirect('brands')

        try:
            cat = brand.objects.get(id=editbrands_id)
            eimage = request.FILES['brand_image']
            cat.brand_image = eimage
            cat.save()
        except:
            pass 

        cat = brand.objects.get(id=editbrands_id)
        cat.brand_name = cname
        cat.brand_address = address
        cat.brand_discription = cdescription
        cat.save()
        return redirect('brands')
    cate = brand.objects.filter(slug=editbrands_id)       
    return render(request, 'brand/editbrands.html', {'catego': cate})

# Delete brand
def deletebrands(request,deletebrands_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    bran = brand.objects.get(id=deletebrands_id)
    bran.delete()
    return redirect('brands')

# Banner
def banner(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    dict_banner={
        'banner' : banners.objects.all(),
        'category' : category.objects.all(),
    }
    return render(request,'banner/banner.html',dict_banner)

# Create Banner
def createbanner(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if request.method == 'POST':
        name = request.POST['banner_name']
        description = request.POST['banner_discription']
        categories = request.POST['categories']
        image = request.FILES.get('image', None)

        # Validation
        if name.strip() == '':
            messages.error(request, "Name Field empty")
            return redirect('banner')

        if not image:
            messages.error(request, "Image not uploaded")
            return redirect('banner')

        cat = category.objects.get(slug = categories)
        ban = banners(
        banners_image = image,
        banner_name = name,
        banner_discription = description,
        category = cat,
        )
        ban.save()  
    return redirect ('banner')

#  Edit Banner
def editbanner(request,banner_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if request.method == 'POST':
        name = request.POST['banner_name']
        description = request.POST['banner_discription']
        categories = request.POST['categories']
# validation
    if name.strip() == '':
        messages.error(request, "Name Field empty")
        return redirect('banner')

    try:
        ban = banners.objects.get(id=banner_id)
        image = request.FILES['image']
        ban.banners_image = image
        ban.save()
    except:
        pass 
    cat = category.objects.get(slug = categories)
    ban = banners.objects.get(id=banner_id)
    ban.banner_name = name
    ban.banner_discription = description
    ban.category = cat
    ban.save()      
    return redirect('banner')

# Delete Banner
def deletebanner(request,banner_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    ban = banners.objects.get(id = banner_id)
    ban.delete()
    return redirect('banner')

# offer
def adminoffer(request):
    context = {
        'offer' : Offer.objects.all()
    }

    return render (request,'offer/offer.html',context)

def addoffer(request):
    if request.method =='POST':
        ordername = request.POST.get('ordername')
        discount = request.POST.get('discount')
        if ordername.strip() == '':
            messages.error(request, "Can't blank order name")
            return redirect('adminoffer')
        if discount.strip() =='':
            messages.error(request, "Can't blank Discount")
            return redirect('adminoffer')
        offer = Offer.objects.create(offer_name=ordername,discount_amount=discount)
        offer.save()
        return redirect('adminoffer')
    
def editoffer(request,offer_id):
  if request.method == 'POST':
    orfername = request.POST.get('orfername')
    discount = request.POST.get('discount')
    if orfername.strip() == '':
        messages.error(request, "Order name cannot be blank.")
        return redirect('adminoffer')
    if discount.strip() == '':
        messages.error(request, "Can't blank Offer field")
        return redirect('adminoffer')
    try:
        if Offer.objects.filter(id=offer_id,offer_name = orfername).exists():
            pass
        else:
            offer = Offer.objects.get(id=offer_id)
            offer.offer_name = orfername
            offer.save()
            messages.success(request, "Offer name updated successfully.")
    except Offer.DoesNotExist:
        messages.error(request, "The specified offer does not exist.")
        return redirect('adminoffer')

    try:
        if Offer.objects.filter(id=offer_id,discount_amount = discount).exists():
            pass
        else:
            offer = Offer.objects.get(id=offer_id)
            offer.discount_amount = discount
            offer.save()
            messages.success(request, "Offer Discount updated successfully.")
        return redirect('adminoffer')
    except Offer.DoesNotExist:
        messages.error(request, "The specified offer does not exist.")
        return redirect('adminoffer')

def deleteoffer(request,delete_id):
    try:
        offer = Offer.objects.filter(id = delete_id)
        offer.delete()
        return redirect('adminoffer')
    except Offer.DoesNotExist:
        messages.error(request, "The specified offer does not exist.")
        return redirect('adminoffer')
# Search User
def searchuser(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            users = User.objects.filter(username__icontains=keyword).order_by('id')
            if users.exists():
                context = {
                    'users': users,
                }
                return render(request, 'admin/user.html', context)
            else:
                message = "User not found."
                return render(request, 'admin/user.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'admin/user.html', {'message': message})
    else:
        return render(request, 'error/index.html')
    
# Aearch Brand
def search_brand(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            Brand = brand.objects.filter(brand_name__icontains=keyword).order_by('id')
            if Brand.exists():
                context = {
                    'brand': Brand,
                }
                return render(request, 'brand/brand.html', context)
            else:
                message = "Brand not found."
                return render(request, 'brand/brand.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'brand/brand.html', {'message': message})
    else:
        return render(request, 'error/index.html')
    
# Search Banner
def search_banner(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            banner = banners.objects.filter(banner_name__icontains=keyword).order_by('id')
            if banner.exists():
                context = {
                    'banner': banner,
                }
                return render(request, 'banner/banner.html', context)
            else:
                message = "Brand not found."
                return render(request, 'banner/banner.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'banner/banner.html', {'message': message})
    else:
        return render(request, 'error/index.html')

# Search Offer
def search_offer(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            offer = Offer.objects.filter(offer_name__icontains=keyword).order_by('id')
            if offer.exists():
                context = {
                    'offer': offer,
                }
                return render(request, 'offer/offer.html', context)
            else:
                message = "Offer not found."
                return render(request, 'offer/offer.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'offer/offer.html', {'message': message})
    else:
        return render(request, 'error/index.html')

# Sales reprt
from datetime import datetime
def salesreport(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    context = {}
    if request.method == 'POST':
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        
        if start_date == '' or end_date == '':
            messages.error(request, 'Give date first')
            return redirect(salesreport)
            
        if start_date == end_date:
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            order_items = OrderItem.objects.filter(order__created_at__date=date_obj.date())
            if order_items:
                context.update(sales=order_items, s_date=start_date, e_date=end_date)
                return render(request, 'admin/salesreport.html', context)
            else:
                messages.error(request, 'No data found')
            return redirect(salesreport)

        order_items = OrderItem.objects.filter(order__created_at__date__gte=start_date, order__created_at__date__lte=end_date)

        if order_items:
            context.update(sales=order_items, s_date=start_date, e_date=end_date)
        else:
            messages.error(request, 'No data found')
    return render(request, 'admin/salesreport.html', context)

import csv

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['user', 'total_price', 'payment_mode', 'tracking_no'])

    expenses = Order.objects.all()
    for expense in expenses:
        writer.writerow([expense.user, expense.total_price, expense.payment_mode,expense.tracking_no])

    return response
