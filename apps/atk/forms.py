from django import forms

from .models import (
    ATKDivisionStock,
    ATKItem,
    ATKRequest,
    get_stock_pool_division,
)


class ATKItemForm(forms.ModelForm):
    class Meta:
        model = ATKItem
        fields = ['name', 'category', 'description', 'unit', 'recipient']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pool_division = get_stock_pool_division()
        self.divisions = [pool_division] if pool_division else []
        stock_map = {}
        if self.instance and self.instance.pk:
            stock_map = {
                stock.division_id: stock
                for stock in self.instance.division_stocks.all()
            }

        for division in self.divisions:
            stock = stock_map.get(division.id)
            self.fields[f'division_stock_{division.id}'] = forms.IntegerField(
                required=False,
                min_value=0,
                initial=stock.current_stock if stock else 0,
                label=f'Stok {division.name}',
                widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Stok'})
            )
            self.fields[f'division_minimum_{division.id}'] = forms.IntegerField(
                required=False,
                min_value=0,
                initial=stock.minimum_stock if stock else 0,
                label=f'Minimum {division.name}',
                widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Min'})
            )
        self.division_stock_fields = [
            {
                'division': division,
                'stock': self[f'division_stock_{division.id}'],
                'minimum': self[f'division_minimum_{division.id}'],
            }
            for division in self.divisions
        ]

    def save(self, commit=True):
        item = super().save(commit=False)
        if commit:
            item.save()
            self.save_division_stocks(item)
            item.sync_global_stock_from_divisions()
        return item

    def save_division_stocks(self, item):
        for division in self.divisions:
            stock_value = self.cleaned_data.get(f'division_stock_{division.id}') or 0
            minimum_value = self.cleaned_data.get(f'division_minimum_{division.id}') or 0
            ATKDivisionStock.objects.update_or_create(
                item=item,
                division=division,
                defaults={
                    'current_stock': stock_value,
                    'minimum_stock': minimum_value,
                }
            )


class ATKRequestForm(forms.ModelForm):
    class Meta:
        model = ATKRequest
        fields = ['purpose']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purpose'].widget.attrs.update({'rows': 4})
