from django.urls import path,include
from django .contrib .staticfiles .urls import staticfiles_urlpatterns
from django .conf .urls .static import static
from django .conf import settings
from .import views
from .views import *

urlpatterns = [
    path('',signin.as_view(), name='signin'),
    path('signup/',signup.as_view(), name='signup'),
    path('forgotpassword/', views.forgot_password, name="forgot_password"),
    path('resetpassword/' , views.reset, name = 'reset'),
    path('logout/',logout.as_view(), name='logout'),
    
]
