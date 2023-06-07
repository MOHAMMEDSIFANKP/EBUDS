from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.apply_coupon, name='apply_coupon'),
    path('admincoupon/', views.admincoupon, name="admincoupon"),
    path('addcoupon/', views.addcoupon, name="addcoupon"),
    path('edicoupon/<int:edit_id>/', views.edicoupon, name="edicoupon"),
    path('deletecoupon/<int:delete_id>/', views.deletecoupon, name="deletecoupon"),
    path('search_coupon/', views.search_coupon, name="search_coupon"),

]
