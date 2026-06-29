from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_code', 'title', 'reporter', 'priority', 'status', 'estimated_completion_at', 'created_at']
    list_filter = ['status', 'priority', 'estimated_completion_at', 'created_at']
    search_fields = ['ticket_code', 'title', 'reporter__username', 'description']
    readonly_fields = ['ticket_code', 'created_at', 'updated_at']
