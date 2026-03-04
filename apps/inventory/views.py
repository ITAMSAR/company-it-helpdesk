from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Equipment, EquipmentCategory
from apps.users.views import AdminRequiredMixin

class EquipmentListView(LoginRequiredMixin, ListView):
    model = Equipment
    template_name = 'inventory/equipment_list.html'
    context_object_name = 'equipment_list'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(inventory_code__icontains=search)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EquipmentCategory.objects.all()
        context['status_choices'] = Equipment.STATUS_CHOICES
        return context

class EquipmentCreateView(AdminRequiredMixin, CreateView):
    model = Equipment
    template_name = 'inventory/equipment_form.html'
    fields = ['name', 'inventory_code', 'category', 'specifications', 'current_user', 
              'status', 'purchase_date', 'warranty_until']
    success_url = reverse_lazy('inventory:equipment_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Peralatan berhasil ditambahkan!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EquipmentCategory.objects.all()
        return context

class EquipmentUpdateView(AdminRequiredMixin, UpdateView):
    model = Equipment
    template_name = 'inventory/equipment_form.html'
    fields = ['name', 'inventory_code', 'category', 'specifications', 'current_user', 
              'status', 'purchase_date', 'warranty_until']
    success_url = reverse_lazy('inventory:equipment_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Peralatan berhasil diupdate!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EquipmentCategory.objects.all()
        return context

# Category Management Views
class CategoryListView(AdminRequiredMixin, ListView):
    model = EquipmentCategory
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20

class CategoryCreateView(AdminRequiredMixin, CreateView):
    model = EquipmentCategory
    template_name = 'inventory/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('inventory:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Kategori berhasil ditambahkan!')
        return super().form_valid(form)

class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = EquipmentCategory
    template_name = 'inventory/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('inventory:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Kategori berhasil diupdate!')
        return super().form_valid(form)

class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    model = EquipmentCategory
    template_name = 'inventory/category_confirm_delete.html'
    success_url = reverse_lazy('inventory:category_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Kategori berhasil dihapus!')
        return super().delete(request, *args, **kwargs)
