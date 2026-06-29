from django.contrib import admin
from .models import Division, EmployeeEmail, UserProfile

@admin.register(EmployeeEmail)
class EmployeeEmailAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'employee_id', 'primary_email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['full_name', 'employee_id', 'primary_email']


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'division', 'updated_at']
    list_filter = ['division']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'division__name']
