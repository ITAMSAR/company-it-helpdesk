from django.contrib import admin
from .models import ATKCategory, ATKDivisionStock, ATKItem, ATKRequest, ATKRequestLine

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


@admin.register(ATKDivisionStock)
class ATKDivisionStockAdmin(admin.ModelAdmin):
    list_display = ['division', 'item', 'current_stock', 'minimum_stock', 'updated_at']
    list_filter = ['division', 'item__category']
    search_fields = ['division__name', 'item__name']
    list_editable = ['current_stock', 'minimum_stock']


@admin.register(ATKRequest)
class ATKRequestAdmin(admin.ModelAdmin):
    list_display = ['display_item_name', 'requester', 'total_quantity', 'status', 'created_at', 'reviewed_by']
    list_filter = ['status', 'created_at', 'reviewed_at']
    search_fields = ['custom_item_name', 'item__name', 'requester__username', 'purpose']
    readonly_fields = ['created_at', 'updated_at', 'reviewed_at']


@admin.register(ATKRequestLine)
class ATKRequestLineAdmin(admin.ModelAdmin):
    list_display = ['request', 'display_item_name', 'quantity', 'created_at']
    search_fields = ['custom_item_name', 'item__name', 'request__requester__username']
