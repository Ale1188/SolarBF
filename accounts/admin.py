from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'role')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'team')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
