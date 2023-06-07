from django.contrib import admin
from .models import category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('categories',)}

admin.site.register(category,CategoryAdmin)