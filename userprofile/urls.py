from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('addaddress/', views.addaddress, name='addaddress'),
    path('editprofiles/', views.editprofiles, name='editprofiles'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('deleteaddress/<int:delete_id>', views.deleteaddress, name='deleteaddress'),

]
