from django.contrib import admin
from .models import Equipment, EquipmentCategory

@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'inventory_code', 'category', 'status', 'current_user', 'purchase_date']
    list_filter = ['status', 'category', 'purchase_date']
    search_fields = ['name', 'inventory_code', 'current_user__username']
