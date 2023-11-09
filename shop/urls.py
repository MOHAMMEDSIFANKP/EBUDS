from django.urls import path
from .import views
from .views import *

urlpatterns = [
    path('',views.shop, name='shop'),
    path('category/<slug:category_slug>/',views.shop, name='product_by_category'),
    path('brand/<slug:brand_slug>/',views.shop, name='product_by_brand'),
    path('Productdetalis/<int:var_id>/',signle.as_view(), name='single'),
    path('search/',views.search, name='search'),
    
]
