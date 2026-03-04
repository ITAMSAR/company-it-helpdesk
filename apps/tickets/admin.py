from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'reporter', 'priority', 'status', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['title', 'reporter__username', 'description']
