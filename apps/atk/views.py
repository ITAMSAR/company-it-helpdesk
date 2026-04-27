from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ATKItem, ATKCategory
from apps.users.views import AdminRequiredMixin

# ATK Item Views
class ATKItemListView(LoginRequiredMixin, ListView):
    model = ATKItem
    template_name = 'atk/item_list.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        stock_status = self.request.GET.get('stock_status')
        if stock_status == 'low':
            # Filter items with low stock
            low_stock_items = []
            for item in queryset:
                if item.is_low_stock:
                    low_stock_items.append(item.id)
            queryset = queryset.filter(id__in=low_stock_items)
        elif stock_status == 'empty':
            queryset = queryset.filter(current_stock=0)
        
        return queryset.select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ATKCategory.objects.all()
        return context

class ATKItemCreateView(AdminRequiredMixin, CreateView):
    model = ATKItem
    template_name = 'atk/item_form.html'
    fields = ['name', 'category', 'description', 'unit', 'current_stock', 
              'minimum_stock', 'recipient']
    success_url = reverse_lazy('atk:item_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Item ATK berhasil ditambahkan!')
        return super().form_valid(form)

class ATKItemUpdateView(AdminRequiredMixin, UpdateView):
    model = ATKItem
    template_name = 'atk/item_form.html'
    fields = ['name', 'category', 'description', 'unit', 'current_stock', 
              'minimum_stock', 'recipient']
    success_url = reverse_lazy('atk:item_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Item ATK berhasil diupdate!')
        return super().form_valid(form)

class ATKItemDeleteView(AdminRequiredMixin, DeleteView):
    model = ATKItem
    template_name = 'atk/item_confirm_delete.html'
    success_url = reverse_lazy('atk:item_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Item ATK berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

# ATK Category Views
class ATKCategoryListView(AdminRequiredMixin, ListView):
    model = ATKCategory
    template_name = 'atk/category_list.html'
    context_object_name = 'categories'

class ATKCategoryCreateView(AdminRequiredMixin, CreateView):
    model = ATKCategory
    template_name = 'atk/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('atk:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Kategori ATK berhasil ditambahkan!')
        return super().form_valid(form)