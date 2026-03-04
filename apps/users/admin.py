from django.contrib import admin
from .models import EmployeeEmail

@admin.register(EmployeeEmail)
class EmployeeEmailAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'employee_id', 'primary_email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['full_name', 'employee_id', 'primary_email']
