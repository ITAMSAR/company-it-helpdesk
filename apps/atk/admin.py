from django.contrib import admin
from .models import ATKCategory, ATKItem

@admin.register(ATKCategory)
class ATKCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']

@admin.register(ATKItem)
class ATKItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'current_stock', 'minimum_stock', 'unit', 'stock_status']
    list_filter = ['category', 'unit']
    search_fields = ['name']
    list_editable = ['current_stock', 'minimum_stock']
    
    def stock_status(self, obj):
        return obj.stock_status
    stock_status.short_description = 'Status Stok'