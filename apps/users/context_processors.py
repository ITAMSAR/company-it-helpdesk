def notification_counts(request):
    if not request.user.is_authenticated:
        return {}

    from apps.atk.models import ATKRequest
    from apps.tickets.models import Ticket

    if request.user.is_staff:
        return {
            'nav_pending_atk_requests': ATKRequest.objects.filter(status='pending').count(),
            'nav_new_tickets': Ticket.objects.filter(status='new').count(),
        }

    return {
        'nav_pending_atk_requests': ATKRequest.objects.filter(
            requester=request.user,
            status='pending'
        ).count(),
        'nav_new_tickets': Ticket.objects.filter(
            reporter=request.user,
            status__in=['new', 'in_progress']
        ).count(),
    }
