from django.contrib import admin
from .models import brand,banner,Contact_us
# Register your models here.

class brandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand_name',)}


admin.site.register(brand,brandAdmin)
admin.site.register(banner)
admin.site.register(Contact_us)
