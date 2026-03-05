from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate
import json
from .models import EmployeeEmail
from apps.inventory.models import Equipment
from apps.tickets.models import Ticket

def is_admin(user):
    return user.is_staff or user.is_superuser

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'dashboard.html'
    context_object_name = 'recent_tickets'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()[:5]
        return Ticket.objects.filter(reporter=self.request.user)[:5]
    
    def get_context_data(self, **kwargs):
        from django.utils import timezone
        from django.db.models import Count
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now()
        if self.request.user.is_staff:
            # Total counts
            context['total_users'] = EmployeeEmail.objects.count()
            context['total_equipment'] = Equipment.objects.count()
            context['pending_tickets'] = Ticket.objects.filter(status='new').count()
            
            # Email status breakdown
            context['email_active'] = EmployeeEmail.objects.filter(is_active=True).count()
            context['email_inactive'] = EmployeeEmail.objects.filter(is_active=False).count()
            
            # Equipment status breakdown
            context['equipment_available'] = Equipment.objects.filter(status='available').count()
            context['equipment_borrowed'] = Equipment.objects.filter(status='borrowed').count()
            context['equipment_broken'] = Equipment.objects.filter(status='broken').count()
            context['equipment_service'] = Equipment.objects.filter(status='service').count()
            
            # Ticket status breakdown
            context['ticket_new'] = Ticket.objects.filter(status='new').count()
            context['ticket_in_progress'] = Ticket.objects.filter(status='in_progress').count()
            context['ticket_completed'] = Ticket.objects.filter(status='completed').count()
            context['ticket_cancelled'] = Ticket.objects.filter(status='cancelled').count()
        else:
            context['my_tickets'] = Ticket.objects.filter(reporter=self.request.user).count()
        return context

# Email Management Views
class EmployeeEmailListView(AdminRequiredMixin, ListView):
    model = EmployeeEmail
    template_name = 'users/email_list.html'
    context_object_name = 'emails'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                full_name__icontains=search
            ) | queryset.filter(
                primary_email__icontains=search
            ) | queryset.filter(
                employee_id__icontains=search
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(is_active=(status == 'active'))
        
        return queryset

class EmployeeEmailCreateView(AdminRequiredMixin, CreateView):
    model = EmployeeEmail
    template_name = 'users/email_form.html'
    fields = ['full_name', 'employee_id', 'primary_email', 'email_password', 
              'recovery_email', 'recovery_phone', 'is_active']
    success_url = reverse_lazy('users:email_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Email karyawan berhasil ditambahkan!')
        return super().form_valid(form)

class EmployeeEmailUpdateView(AdminRequiredMixin, UpdateView):
    model = EmployeeEmail
    template_name = 'users/email_form.html'
    fields = ['full_name', 'employee_id', 'primary_email', 'email_password', 
              'recovery_email', 'recovery_phone', 'is_active']
    success_url = reverse_lazy('users:email_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Email karyawan berhasil diupdate!')
        return super().form_valid(form)

class EmployeeEmailDeleteView(AdminRequiredMixin, DeleteView):
    model = EmployeeEmail
    template_name = 'users/email_confirm_delete.html'
    success_url = reverse_lazy('users:email_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Email karyawan berhasil dihapus!')
        return super().delete(request, *args, **kwargs)


@require_POST
@login_required
def verify_admin_password(request):
    """Verify admin password untuk melihat password email"""
    try:
        data = json.loads(request.body)
        password = data.get('password')
        
        # Authenticate user
        user = authenticate(username=request.user.username, password=password)
        
        if user is not None and user.is_staff:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Password salah'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime

@login_required
def export_emails_excel(request):
    """Export email karyawan ke Excel (tanpa password)"""
    if not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki akses untuk export data!')
        return redirect('users:email_list')
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Email Karyawan"
    
    # Header style
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    # Headers
    headers = ['No', 'Nama Lengkap', 'NIK', 'Email Utama', 'Recovery Email', 'Recovery Phone', 'Status', 'Tanggal Dibuat']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
    
    # Data
    emails = EmployeeEmail.objects.all().order_by('-created_at')
    for row, email in enumerate(emails, 2):
        ws.cell(row=row, column=1, value=row-1)
        ws.cell(row=row, column=2, value=email.full_name)
        ws.cell(row=row, column=3, value=email.employee_id)
        ws.cell(row=row, column=4, value=email.primary_email)
        ws.cell(row=row, column=5, value=email.recovery_email or '-')
        ws.cell(row=row, column=6, value=email.recovery_phone or '-')
        ws.cell(row=row, column=7, value='Aktif' if email.is_active else 'Nonaktif')
        ws.cell(row=row, column=8, value=email.created_at.strftime('%d/%m/%Y %H:%M'))
    
    # Adjust column widths
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 30
    ws.column_dimensions['E'].width = 30
    ws.column_dimensions['F'].width = 15
    ws.column_dimensions['G'].width = 10
    ws.column_dimensions['H'].width = 20
    
    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f'Email_Karyawan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response['Content-Disposition'] = f'attachment; filename={filename}'
    
    wb.save(response)
    return response
