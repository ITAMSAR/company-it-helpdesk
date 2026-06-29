from django.contrib import admin
from .models import Equipment, EquipmentCategory, EquipmentDeletionLog

@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'inventory_code', 'category', 'status', 'current_user', 'purchase_date']
    list_filter = ['status', 'category', 'purchase_date']
    search_fields = ['name', 'inventory_code', 'current_user__username']


@admin.register(EquipmentDeletionLog)
class EquipmentDeletionLogAdmin(admin.ModelAdmin):
    list_display = ['inventory_code', 'equipment_name', 'category_name', 'deleted_by', 'deleted_at']
    list_filter = ['deleted_at', 'category_name']
    search_fields = ['inventory_code', 'equipment_name', 'reason', 'deleted_by__username']
    readonly_fields = ['deleted_at']
