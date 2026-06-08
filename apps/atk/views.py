from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.db.models import F
from .forms import ATKRequestForm
from .models import ATKItem, ATKCategory, ATKRequest, ATKRequestLine
from apps.users.views import AdminRequiredMixin

# ATK Item Views
class ATKItemListView(LoginRequiredMixin, ListView):
    model = ATKItem
    template_name = 'atk/item_list.html'
    context_object_name = 'items'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('atk:request_list')
        return super().dispatch(request, *args, **kwargs)

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
            queryset = queryset.filter(current_stock__gt=0, current_stock__lte=F('minimum_stock'))
        elif stock_status == 'empty':
            queryset = queryset.filter(current_stock=0)
        
        return queryset.select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ATKCategory.objects.all()
        return context


class ATKRequestListView(LoginRequiredMixin, ListView):
    model = ATKRequest
    template_name = 'atk/request_list.html'
    context_object_name = 'requests'
    paginate_by = 20

    def get_queryset(self):
        queryset = ATKRequest.objects.select_related('requester', 'item', 'reviewed_by').prefetch_related('lines__item')

        if not self.request.user.is_staff:
            queryset = queryset.filter(requester=self.request.user)

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        return queryset


class ATKRequestCreateView(LoginRequiredMixin, CreateView):
    model = ATKRequest
    form_class = ATKRequestForm
    template_name = 'atk/request_form.html'
    success_url = reverse_lazy('atk:request_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['atk_items'] = ATKItem.objects.select_related('category').order_by('name')
        return context

    def form_valid(self, form):
        lines = self._get_request_lines()
        if not lines:
            form.add_error(None, 'Minimal isi satu item ATK yang diajukan.')
            return self.form_invalid(form)

        form.instance.requester = self.request.user
        response = super().form_valid(form)
        ATKRequestLine.objects.bulk_create([
            ATKRequestLine(
                request=self.object,
                item=line['item'],
                custom_item_name=line['custom_item_name'],
                quantity=line['quantity'],
            )
            for line in lines
        ])
        messages.success(self.request, 'Pengajuan ATK berhasil dikirim ke admin.')
        return response

    def _get_request_lines(self):
        item_ids = self.request.POST.getlist('item')
        custom_names = self.request.POST.getlist('custom_item_name')
        quantities = self.request.POST.getlist('quantity')
        item_map = {
            str(item.id): item
            for item in ATKItem.objects.filter(id__in=[item_id for item_id in item_ids if item_id])
        }
        lines = []

        for index in range(max(len(item_ids), len(custom_names), len(quantities))):
            item_id = item_ids[index] if index < len(item_ids) else ''
            custom_name = custom_names[index].strip() if index < len(custom_names) else ''
            raw_quantity = quantities[index] if index < len(quantities) else ''

            if not item_id and not custom_name:
                continue

            try:
                quantity = int(raw_quantity)
            except (TypeError, ValueError):
                quantity = 0

            if quantity < 1:
                continue

            if item_id and item_id not in item_map:
                continue

            lines.append({
                'item': item_map.get(item_id),
                'custom_item_name': custom_name if not item_id else '',
                'quantity': quantity,
            })

        return lines


class ATKRequestDetailView(LoginRequiredMixin, DetailView):
    model = ATKRequest
    template_name = 'atk/request_detail.html'
    context_object_name = 'atk_request'

    def get_queryset(self):
        queryset = ATKRequest.objects.select_related('requester', 'item', 'reviewed_by').prefetch_related('lines__item')
        if not self.request.user.is_staff:
            queryset = queryset.filter(requester=self.request.user)
        return queryset


@login_required
def review_atk_request(request, pk):
    atk_request = get_object_or_404(
        ATKRequest.objects.select_related('item').prefetch_related('lines__item'),
        pk=pk
    )

    if not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki akses untuk memproses pengajuan ATK.')
        return redirect('atk:request_detail', pk=pk)

    if request.method != 'POST':
        return redirect('atk:request_detail', pk=pk)

    action = request.POST.get('action')
    notes = request.POST.get('admin_notes', '')

    if action not in ['approved', 'rejected']:
        messages.error(request, 'Status pengajuan tidak valid.')
        return redirect('atk:request_detail', pk=pk)

    if atk_request.status != 'pending':
        messages.warning(request, 'Pengajuan ini sudah pernah diproses.')
        return redirect('atk:request_detail', pk=pk)

    with transaction.atomic():
        if action == 'approved':
            stock_lines = [line for line in atk_request.lines.all() if line.item_id]
            if not stock_lines and atk_request.item:
                stock_lines = [atk_request]

            for line in stock_lines:
                item = ATKItem.objects.select_for_update().get(pk=line.item_id)
                if item.current_stock < line.quantity:
                    messages.error(request, f'Stok {item.name} tidak cukup untuk menyetujui pengajuan ini.')
                    return redirect('atk:request_detail', pk=pk)

            for line in stock_lines:
                item = ATKItem.objects.select_for_update().get(pk=line.item_id)
                item.current_stock -= line.quantity
                item.recipient = atk_request.requester.get_full_name() or atk_request.requester.username
                item.save(update_fields=['current_stock', 'recipient', 'updated_at'])

        atk_request.status = action
        atk_request.admin_notes = notes
        atk_request.reviewed_by = request.user
        atk_request.reviewed_at = timezone.now()
        atk_request.save(update_fields=['status', 'admin_notes', 'reviewed_by', 'reviewed_at', 'updated_at'])

    status_text = 'disetujui' if action == 'approved' else 'ditolak'
    messages.success(request, f'Pengajuan ATK berhasil {status_text}.')
    return redirect('atk:request_detail', pk=pk)

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
