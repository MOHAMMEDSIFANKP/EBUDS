from django.urls import path,include
from django .contrib .staticfiles .urls import staticfiles_urlpatterns
from django .conf .urls .static import static
from django .conf import settings
from .import views

urlpatterns = [
    path('',views.signin, name='signin'),
    path('signup/',views.signup, name='signup'),
    path('forgotpassword/', views.forgot_password, name="forgot_password"),
    path('resetpassword/' , views.reset, name = 'reset'),
    path('logout/',views.logout, name='logout'),
    
]
