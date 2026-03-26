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
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        # Clamp page number to valid range
        try:
            page = int(request.GET.get('page', 1))
            if page < 1:
                from django.http import HttpResponseRedirect
                params = request.GET.copy()
                params['page'] = 1
                return HttpResponseRedirect(f"?{params.urlencode()}")
        except (ValueError, TypeError):
            pass
        return super().get(request, *args, **kwargs)

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

class EquipmentDeleteView(AdminRequiredMixin, DeleteView):
    model = Equipment
    template_name = 'inventory/equipment_confirm_delete.html'
    success_url = reverse_lazy('inventory:equipment_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Peralatan berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

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


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime

@login_required
def export_equipment_excel(request):
    """Export inventaris peralatan ke Excel"""
    if not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki akses untuk export data!')
        return redirect('inventory:equipment_list')
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Inventaris Peralatan"
    
    # Header style
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    # Headers
    headers = ['No', 'Nama', 'Kode Inventaris', 'Kategori', 'Spesifikasi', 'Pengguna', 'Status', 'Tanggal Pembelian', 'Garansi Sampai']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
    
    # Data
    equipment_list = Equipment.objects.select_related('category').all().order_by('-created_at')
    for row, equipment in enumerate(equipment_list, 2):
        ws.cell(row=row, column=1, value=row-1)
        ws.cell(row=row, column=2, value=equipment.name)
        ws.cell(row=row, column=3, value=equipment.inventory_code)
        ws.cell(row=row, column=4, value=equipment.category.name)
        ws.cell(row=row, column=5, value=equipment.specifications or '-')
        ws.cell(row=row, column=6, value=equipment.current_user or '-')
        ws.cell(row=row, column=7, value=equipment.get_status_display())
        ws.cell(row=row, column=8, value=equipment.purchase_date.strftime('%d/%m/%Y') if equipment.purchase_date else '-')
        ws.cell(row=row, column=9, value=equipment.warranty_until.strftime('%d/%m/%Y') if equipment.warranty_until else '-')
    
    # Adjust column widths
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 40
    ws.column_dimensions['F'].width = 20
    ws.column_dimensions['G'].width = 15
    ws.column_dimensions['H'].width = 18
    ws.column_dimensions['I'].width = 18
    
    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f'Inventaris_Peralatan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response['Content-Disposition'] = f'attachment; filename={filename}'
    
    wb.save(response)
    return response
