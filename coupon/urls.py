from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.apply_coupon, name='apply_coupon'),
    path('admincoupon/', views.admincoupon, name="admincoupon")

]
