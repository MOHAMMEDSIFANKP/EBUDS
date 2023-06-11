from django.urls import path, include
from .import views

urlpatterns = [
    path('adminsignin/',views.adminsignin, name='adminsignin'),
    path('adminsignup/',views.adminsignup, name='adminsignup'),
    path('',views.dashboard, name='dashboard'),
    path('user/',views.user, name='user'),
    path('searchuser/',views.searchuser, name='searchuser'),
    path('brands/', views.brands, name='brands'),
    path('search_brand/', views.search_brand, name='search_brand'),
    path('createbrands/', views.createbrands, name='createbrands'),
    path('editbrands/<slug:editbrands_id>', views.editbrands, name='editbrands'),
    path('deletebrands/<slug:deletebrands_id>', views.deletebrands, name='deletebrands'),
    path('blockuser/<int:user_id>', views.blockuser, name="blockuser"),
    path('banner/', views.banner, name='banner'),
    path('search_banner/', views.search_banner, name='search_banner'),
    path('createbanner/', views.createbanner, name='createbanner'),
    path('editbanner/<int:banner_id>/', views.editbanner, name='editbanner'),
    path('deletebanner/<int:banner_id>/', views.deletebanner, name='deletebanner'),
    path('Adminoffer/',views.adminoffer, name="adminoffer"),
    path('addoffer/',views.addoffer, name="addoffer"),
    path('editoffer/<int:offer_id>/',views.editoffer, name="editoffer"),
    path('deleteoffer/<int:delete_id>/',views.deleteoffer, name="deleteoffer"),
    path('search_offer/',views.search_offer, name="search_offer"),
    path('salesreport/',views.salesreport, name="salesreport"),
]
