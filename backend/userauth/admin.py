from django.contrib import admin
from userauth.models import CustomUser,Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','full_name','created_at']
    
admin.site.register(CustomUser)
admin.site.register(Profile,ProfileAdmin)
