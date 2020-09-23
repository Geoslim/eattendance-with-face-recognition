from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()
class UserAdmin(BaseUserAdmin):
    
    list_display = ('username', 'first_name', 'email')
    # list_filter = ('admin','active')
    fieldsets = (
        ('Account', {'fields': ('email', 'password','profile_image')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser','is_staff', 'is_active','groups')}),
    )
    
admin.site.register(User, UserAdmin)
admin.site.register(Profile)