from django.contrib import admin
from .models import Equipment, EquipmentCategory, EquipmentDeletionLog, EquipmentPhoto

class EquipmentPhotoInline(admin.TabularInline):
    model = EquipmentPhoto
    extra = 1
    fields = ['image', 'position', 'caption', 'order']

@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'inventory_code', 'category', 'status', 'current_user', 'purchase_date']
    list_filter = ['status', 'category', 'purchase_date']
    search_fields = ['name', 'inventory_code', 'current_user__username']
    inlines = [EquipmentPhotoInline]


@admin.register(EquipmentDeletionLog)
class EquipmentDeletionLogAdmin(admin.ModelAdmin):
    list_display = ['inventory_code', 'equipment_name', 'category_name', 'deleted_by', 'deleted_at']
    list_filter = ['deleted_at', 'category_name']
    search_fields = ['inventory_code', 'equipment_name', 'reason', 'deleted_by__username']
    readonly_fields = ['deleted_at']

@admin.register(EquipmentPhoto)
class EquipmentPhotoAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'position', 'caption', 'order', 'uploaded_at']
    list_filter = ['position', 'uploaded_at']
    search_fields = ['equipment__name', 'caption']
    list_editable = ['order']

