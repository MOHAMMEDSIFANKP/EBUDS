from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Address, Wallet
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def profile(request):     
    dict_user={
        'address' : Address.objects.filter(user = request.user),
        'user' : User.objects.get(username = request.user),
        'wallets' : Wallet.objects.filter(user = request.user)
    }
    return render(request,'userprofile/userprofile.html',dict_user)
# Add Address
def addaddress(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        state = request.POST.get('state')
        order_note = request.POST.get('ordernote')

        if request.user is None:
            return 
        if first_name.strip() == '' or last_name.strip() == '':
            messages.error(request, 'First name or Last name is empty!')
            return redirect('profile')
        if country.strip() =='':
            messages.error(request, 'Country is empty!')
            return redirect('profile')
        if city.strip() =='':
            messages.error(request, 'City is empty!')
            return redirect('profile')
        if address.strip() =='':
            messages.error(request, 'Address is empty!')
            return redirect('profile')
        if pincode.strip() =='':
            messages.error(request, 'Pincode is empty!')
            return redirect('profile')
        if phone.strip() =='':
            messages.error(request, 'Phone is empty!')
            return redirect('profile')
        if email.strip() =='':
            messages.error(request, 'Email is empty!')
            return redirect('profile')
        if state.strip() =='':
            messages.error(request, 'State is empty!')
            return redirect('profile')
        
        adrs = Address()
        adrs.user = request.user
        adrs.first_name = first_name
        adrs.last_name = last_name
        adrs.country = country
        adrs.address = address
        adrs.city = city
        adrs.pincode = pincode
        adrs.phone = phone
        adrs.email = email
        adrs.state = state
        adrs.order_note = order_note
        adrs.save()

        return redirect('profile')
# edit Userprofiles
def editprofiles(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Validation
        if username == '':
            messages.error(request, 'Username is empty')
            return redirect('profile')
        if first_name == '' or last_name == '':
            messages.error(request, 'First or Lastname is empty')
            return redirect('profile')

        try:
            user = User.objects.get(username=request.user)
            print(user)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except ObjectDoesNotExist:
            messages.error(request, 'User does not exist')
        return redirect('profile')
    
# Change Password 
def changepassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
#  Validation
        if new_password != confirm_new_password:
            messages.error(request,'Password did not match')
            return redirect('profile')
        user = User.objects.get(username = request.user)
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, 'Password updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid old password')
            return redirect('profile')
    return redirect('profile')

# delete Address
def deleteaddress(request,delete_id):
    address = Address.objects.get(id = delete_id)
    address.delete()
    return redirect('profile')