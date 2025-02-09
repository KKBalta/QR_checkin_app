from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Workplace, AttendanceLog, User, APIKey

# Register Workplace model
@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

# Register AttendanceLog model
@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ('employee', 'workplace', 'check_in_time', 'check_out_time')
    list_filter = ('workplace', 'check_in_time')

# Register the custom User model
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_checked_in')
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Register APIKey model
@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'created_at', 'is_active')
    search_fields = ('name', 'key')
    list_filter = ('is_active', 'created_at')
