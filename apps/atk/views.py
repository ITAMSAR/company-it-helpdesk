from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.db.models import Count, F, Q
from .forms import ATKItemForm, ATKRequestForm
from .models import (
    ATKDivisionStock,
    ATKItem,
    ATKCategory,
    ATKRequest,
    ATKRequestLine,
    get_stock_pool_division,
)
from apps.users.models import Division
from apps.users.views import AdminRequiredMixin


def _stock_lines_for_request(atk_request):
    stock_lines = [line for line in atk_request.lines.all() if line.item_id]
    if not stock_lines and atk_request.item:
        stock_lines = [atk_request]
    return stock_lines


def _request_has_custom_lines(atk_request):
    return atk_request.lines.filter(item__isnull=True).exists() or (
        not atk_request.lines.exists() and not atk_request.item_id
    )


def _transfer_stock_to_division(stock_lines, target_division):
    source_division = get_stock_pool_division()
    if not source_division:
        return False, 'Divisi Administrator sebagai sumber stok belum tersedia.'

    for line in stock_lines:
        item = ATKItem.objects.select_for_update().get(pk=line.item_id)
        if source_division and source_division != target_division:
            source_stock, _ = ATKDivisionStock.objects.select_for_update().get_or_create(
                item=item,
                division=source_division,
                defaults={'current_stock': 0, 'minimum_stock': 0}
            )
            if source_stock.current_stock < line.quantity:
                return False, f'Stok Admin untuk {item.name} tidak cukup. Tandai sebagai Perlu Pembelian atau update stok Admin dulu.'

    for line in stock_lines:
        item = ATKItem.objects.select_for_update().get(pk=line.item_id)
        target_stock, _ = ATKDivisionStock.objects.select_for_update().get_or_create(
            item=item,
            division=target_division,
            defaults={'current_stock': 0, 'minimum_stock': 0}
        )

        if source_division and source_division != target_division:
            source_stock = ATKDivisionStock.objects.select_for_update().get(
                item=item,
                division=source_division,
            )
            source_stock.current_stock -= line.quantity
            source_stock.save(update_fields=['current_stock', 'updated_at'])

        target_stock.current_stock += line.quantity
        target_stock.save(update_fields=['current_stock', 'updated_at'])
        item.sync_global_stock_from_divisions()

    return True, ''


# ATK Item Views
class ATKItemListView(LoginRequiredMixin, ListView):
    model = ATKItem
    template_name = 'atk/item_list.html'
    context_object_name = 'items'
    paginate_by = 20

    def _get_user_division(self):
        if not hasattr(self, '_user_division'):
            profile = getattr(self.request.user, 'profile', None)
            self._user_division = profile.division if profile else None
        return self._user_division

    def _get_selected_division(self):
        if hasattr(self, '_selected_division'):
            return self._selected_division

        if not self.request.user.is_staff:
            selected_division = self._get_user_division()
        else:
            selected_division_id = self.request.GET.get('division')
            selected_division = (
                Division.objects.filter(pk=selected_division_id).first()
                if selected_division_id
                else get_stock_pool_division()
            )

        self._selected_division = selected_division
        return selected_division

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_division = self._get_selected_division()
        if not selected_division:
            return queryset.none()

        stock_filter = Q(division_stocks__division=selected_division)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        stock_status = self.request.GET.get('stock_status')
        if stock_status == 'low':
            stock_filter &= Q(
                division_stocks__current_stock__gt=0,
                division_stocks__current_stock__lte=F('division_stocks__minimum_stock'),
            )
        elif stock_status == 'empty':
            stock_filter &= Q(division_stocks__current_stock=0)
        
        return queryset.filter(stock_filter).select_related('category').prefetch_related(
            'division_stocks__division'
        ).annotate(
            approved_request_count=Count(
                'request_lines',
                filter=Q(request_lines__request__status='approved'),
                distinct=True,
            ),
            pending_request_count=Count(
                'request_lines',
                filter=Q(request_lines__request__status='pending'),
                distinct=True,
            ),
        ).order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ATKCategory.objects.all()
        context['user_division'] = self._get_user_division()
        selected_division = self._get_selected_division()

        context['selected_scope'] = 'division'
        context['selected_division'] = selected_division
        context['has_stock_scope'] = bool(selected_division)
        context['division_stock_cards'] = self._build_division_stock_cards(
            allowed_division=context['user_division'] if not self.request.user.is_staff else None
        )

        for item in context['items']:
            stock_map = {stock.division_id: stock for stock in item.division_stocks.all()}
            item.current_division_stock = stock_map.get(context['user_division'].id) if context['user_division'] else None
            item.division_stock_summary = list(item.division_stocks.all()[:3])
            item.selected_stock = item.current_stock
            item.selected_minimum = item.minimum_stock
            item.selected_stock_label = 'Tidak tersedia'
            item.selected_stock_status = item.stock_status
            if selected_division:
                selected_stock = stock_map.get(selected_division.id)
                item.selected_stock_label = selected_division.name
                if selected_stock:
                    item.selected_stock = selected_stock.current_stock
                    item.selected_minimum = selected_stock.minimum_stock
                    item.selected_stock_status = selected_stock.stock_status
                else:
                    item.selected_stock = 0
                    item.selected_minimum = 0
                    item.selected_stock_status = 'Habis'
        return context

    def _build_division_stock_cards(self, allowed_division=None):
        cards = []
        divisions = Division.objects.all().order_by('name')
        if allowed_division:
            divisions = divisions.filter(pk=allowed_division.pk)
        elif not self.request.user.is_staff:
            divisions = divisions.none()

        for division in divisions:
            stocks = list(ATKDivisionStock.objects.filter(division=division))
            stock_values = [
                (stock.current_stock, stock.minimum_stock)
                for stock in stocks
            ]

            safe_count = sum(1 for current_stock, minimum_stock in stock_values if current_stock > minimum_stock)
            low_count = sum(1 for current_stock, minimum_stock in stock_values if current_stock > 0 and current_stock <= minimum_stock)
            empty_count = sum(1 for current_stock, minimum_stock in stock_values if current_stock == 0)
            cards.append({
                'division': division,
                'item_count': len(stocks),
                'safe_count': safe_count,
                'low_count': low_count,
                'empty_count': empty_count,
            })
        return cards


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
        source_division = get_stock_pool_division()
        items = (
            ATKItem.objects
            .select_related('category')
            .filter(division_stocks__division=source_division)
            .prefetch_related('division_stocks')
            .order_by('name')
            if source_division
            else ATKItem.objects.none()
        )
        for item in items:
            source_stock = next(
                (
                    stock
                    for stock in item.division_stocks.all()
                    if stock.division_id == source_division.id
                ),
                None,
            )
            item.request_stock = source_stock.current_stock if source_stock else 0
        context['atk_items'] = items
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requester_profile = getattr(self.object.requester, 'profile', None)
        request_division = requester_profile.division if requester_profile else None
        context['request_division'] = request_division
        source_division = get_stock_pool_division()
        for line in self.object.lines.all():
            line.fulfillment_stock_label = source_division.name if source_division else 'Administrator'
            line.fulfillment_stock = line.item.current_stock if line.item else None
            if line.item and source_division:
                division_stock = line.item.division_stocks.filter(division=source_division).first()
                if division_stock:
                    line.fulfillment_stock = division_stock.current_stock
        if self.request.user.is_staff:
            context['atk_items'] = ATKItem.objects.select_related('category').order_by('name')
        return context


class ATKItemDetailView(AdminRequiredMixin, DetailView):
    model = ATKItem
    template_name = 'atk/item_detail.html'
    context_object_name = 'item'

    def get_queryset(self):
        return ATKItem.objects.select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_lines = (
            ATKRequestLine.objects
            .filter(item=self.object)
            .select_related('request__requester', 'request__reviewed_by')
            .order_by('-request__created_at')
        )
        context['request_lines'] = request_lines
        context['approved_count'] = request_lines.filter(request__status='approved').count()
        context['pending_count'] = request_lines.filter(request__status='pending').count()
        context['purchase_count'] = request_lines.filter(request__status='needs_purchase').count()
        context['total_approved_quantity'] = sum(line.quantity for line in request_lines if line.request.status == 'approved')
        context['division_stocks'] = self.object.division_stocks.select_related('division')
        return context


@login_required
def link_atk_request_line(request, pk, line_pk):
    atk_request = get_object_or_404(
        ATKRequest.objects.prefetch_related('lines__item'),
        pk=pk
    )

    if not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki akses untuk menghubungkan item ATK.')
        return redirect('atk:request_detail', pk=pk)

    if request.method != 'POST':
        return redirect('atk:request_detail', pk=pk)

    line = get_object_or_404(ATKRequestLine, pk=line_pk, request=atk_request)
    item = get_object_or_404(ATKItem, pk=request.POST.get('item'))

    line.item = item
    line.custom_item_name = ''
    line.save(update_fields=['item', 'custom_item_name'])

    if not atk_request.item_id:
        atk_request.item = item
        atk_request.custom_item_name = ''
        atk_request.save(update_fields=['item', 'custom_item_name', 'updated_at'])

    messages.success(request, f'Item pengajuan berhasil dihubungkan ke stok {item.name}.')
    return redirect('atk:request_detail', pk=pk)


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

    if action not in ['approved', 'needs_purchase', 'rejected']:
        messages.error(request, 'Status pengajuan tidak valid.')
        return redirect('atk:request_detail', pk=pk)

    if atk_request.status not in ['pending', 'needs_purchase']:
        messages.warning(request, 'Pengajuan ini sudah pernah diproses.')
        return redirect('atk:request_detail', pk=pk)

    with transaction.atomic():
        if action == 'approved':
            stock_lines = _stock_lines_for_request(atk_request)
            if _request_has_custom_lines(atk_request):
                messages.error(request, 'Ada item yang belum tersedia di stok. Tandai sebagai Perlu Pembelian dulu.')
                return redirect('atk:request_detail', pk=pk)

            requester_profile = getattr(atk_request.requester, 'profile', None)
            requester_division = requester_profile.division if requester_profile else None
            if not requester_division:
                messages.error(request, 'Pemohon belum punya divisi. Set divisi user dulu sebelum menyetujui ATK.')
                return redirect('atk:request_detail', pk=pk)

            success, error_message = _transfer_stock_to_division(stock_lines, requester_division)
            if not success:
                messages.error(request, error_message)
                return redirect('atk:request_detail', pk=pk)

        atk_request.status = action
        atk_request.admin_notes = notes
        atk_request.reviewed_by = request.user
        atk_request.reviewed_at = timezone.now()
        update_fields = ['status', 'admin_notes', 'reviewed_by', 'reviewed_at', 'updated_at']
        if action == 'approved':
            atk_request.stock_applied_at = timezone.now()
            atk_request.stock_applied_division = requester_division
            update_fields.extend(['stock_applied_at', 'stock_applied_division'])
        atk_request.save(update_fields=update_fields)

    status_text = {
        'approved': 'disetujui',
        'needs_purchase': 'ditandai perlu pembelian',
        'rejected': 'ditolak',
    }[action]
    messages.success(request, f'Pengajuan ATK berhasil {status_text}.')
    return redirect('atk:request_detail', pk=pk)

class ATKItemCreateView(AdminRequiredMixin, CreateView):
    model = ATKItem
    form_class = ATKItemForm
    template_name = 'atk/item_form.html'
    success_url = reverse_lazy('atk:item_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Item ATK berhasil ditambahkan!')
        return super().form_valid(form)

class ATKItemUpdateView(AdminRequiredMixin, UpdateView):
    model = ATKItem
    form_class = ATKItemForm
    template_name = 'atk/item_form.html'
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
