from django.urls import path, include
from .import views
urlpatterns = [
    path('', views.categories, name='categories'),
    path('search_category/', views.search_category, name='search_category'),
    path('createcategory/', views.createcategory, name='createcategory'),
    path('editcategory/<slug:editcategory_id>', views.editcategory, name='editcategory'),
    path('deletecategory/<slug:deletecategory_id>', views.deletecategory, name='deletecategory'),
]