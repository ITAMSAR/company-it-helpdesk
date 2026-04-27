from django.db import models
from django.contrib.auth.models import User

class ATKCategory(models.Model):
    """Kategori ATK seperti Alat Tulis, Kertas, dll"""
    name = models.CharField(max_length=100, verbose_name='Nama Kategori')
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Kategori ATK'
        verbose_name_plural = 'Kategori ATK'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class ATKItem(models.Model):
    """Item ATK dengan stok"""
    UNIT_CHOICES = [
        ('pcs', 'Pieces'),
        ('box', 'Box'),
        ('pack', 'Pack'),
        ('rim', 'Rim'),
        ('roll', 'Roll'),
        ('bottle', 'Botol'),
        ('tube', 'Tube'),
        ('set', 'Set'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Nama ATK')
    category = models.ForeignKey(ATKCategory, on_delete=models.PROTECT, 
                                related_name='items', verbose_name='Kategori')
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pcs', verbose_name='Satuan')
    current_stock = models.IntegerField(default=0, verbose_name='Stok Saat Ini')
    minimum_stock = models.IntegerField(default=10, verbose_name='Stok Minimum')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, 
                                        verbose_name='Harga per Satuan')
    supplier = models.CharField(max_length=200, blank=True, verbose_name='Supplier')
    recipient = models.CharField(max_length=200, blank=True, verbose_name='Penerima')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Item ATK'
        verbose_name_plural = 'Item ATK'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.get_unit_display()})"
    
    @property
    def is_low_stock(self):
        """Cek apakah stok sudah menipis"""
        return self.current_stock <= self.minimum_stock
    
    @property
    def stock_status(self):
        """Status stok dalam bentuk text"""
        if self.current_stock == 0:
            return 'Habis'
        elif self.is_low_stock:
            return 'Menipis'
        else:
            return 'Aman'