"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django .conf .urls .static import static
from django .conf import settings
from django.views.static import serve

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('account/',include('registration.urls')),
    path('category/',include('category.urls')),
    path('shop/',include('shop.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('product/',include('product.urls')),
    path('cart/',include('carts.urls')),
    path('checkout/',include('checkout.urls')),
    path('profile/',include('userprofile.urls')),
    path('orders/',include('orders.urls')),
    path('wishlist/',include('wishlist.urls')),
    path('coupon/',include('coupon.urls')),
    path('api/', include("apis.urls"))


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = 'home.views.error_404_view'
