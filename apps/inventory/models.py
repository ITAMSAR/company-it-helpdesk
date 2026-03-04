from django.db import models
from django.contrib.auth.models import User

class EquipmentCategory(models.Model):
    """Model untuk kategori peralatan yang bisa ditambah dinamis"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Nama Kategori')
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Kategori Peralatan'
        verbose_name_plural = 'Kategori Peralatan'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Equipment(models.Model):
    STATUS_CHOICES = [
        ('available', 'Tersedia'),
        ('borrowed', 'Dipinjam'),
        ('broken', 'Rusak'),
        ('service', 'Servis'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Nama Barang')
    inventory_code = models.CharField(max_length=100, unique=True, verbose_name='Kode Inventaris')
    category = models.ForeignKey(EquipmentCategory, on_delete=models.PROTECT, 
                                 related_name='equipment', verbose_name='Kategori')
    specifications = models.TextField(blank=True, verbose_name='Spesifikasi')
    current_user = models.CharField(max_length=200, blank=True, verbose_name='Pengguna Saat Ini')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='Status')
    purchase_date = models.DateField(null=True, blank=True, verbose_name='Tanggal Pembelian')
    warranty_until = models.DateField(null=True, blank=True, verbose_name='Garansi Sampai')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Peralatan'
        verbose_name_plural = 'Peralatan'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.inventory_code})"
