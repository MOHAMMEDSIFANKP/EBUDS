from django.urls import path, include
from django.urls import re_path
from .import views

urlpatterns = [
    path('', views.orders, name='orders'),
    path('ordercancel/', views.ordercancel, name='ordercancel'),
    path('orderdetails/', views.orderdetails, name='orderdetails'),
    path('changestatus/', views.changestatus, name='changestatus'),
    path('trackorder/', views.trackorder, name='trackorder'),
    # re_path(r'^myorders/user-order-track/(?P<order_id>[\w\-]+)/$', views.user_order_track, name='user_order_track'),
    path('search_orders/', views.search_orders, name='search_orders'),
    

]
