from django.urls import path
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('contact/',views.contact, name='contact'),
    path('admin_contact/',views.admin_contact, name='admin_contact'),
    path('search_contact/',views.search_contact, name='search_contact'),
    path('blog/',views.blog, name='blog'),
]