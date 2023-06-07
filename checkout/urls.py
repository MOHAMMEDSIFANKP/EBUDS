from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('placeorder/',views.placeorder, name='placeorder'),
    path('addcheckoutaddr/',views.addcheckoutaddr, name='addcheckoutaddr'),
    path('deleteaddresscheckout/<int:delete_id>/',views.deleteaddresscheckout, name='deleteaddresscheckout'),
    path('proceedtopay/', views.razarypaycheck, name = 'razarypaycheck'),
    
    
    
]