from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count
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
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['total_users'] = EmployeeEmail.objects.count()
            context['total_equipment'] = Equipment.objects.count()
            context['pending_tickets'] = Ticket.objects.filter(status='new').count()
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
