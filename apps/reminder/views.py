from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import NetworkCheckLog

@login_required
def reminder_view(request):
    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        NetworkCheckLog.objects.create(checked_by=request.user, notes=notes)
        messages.success(request, 'Pengecekan jaringan berhasil dicatat!')
        return redirect('reminder:reminder')
    
    logs = NetworkCheckLog.objects.all()[:10]
    return render(request, 'reminder/reminder.html', {'logs': logs})
