from django.contrib import admin
from .models import NetworkCheckLog

@admin.register(NetworkCheckLog)
class NetworkCheckLogAdmin(admin.ModelAdmin):
    list_display = ['checked_by', 'checked_at', 'notes']
    list_filter = ['checked_at']
    search_fields = ['checked_by__username', 'notes']
