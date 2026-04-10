from django.db import models
from django.contrib.auth.models import User

class EquipmentCategory(models.Model):
    """Model untuk kategori peralatan yang bisa ditambah dinamis dengan hierarki"""
    name = models.CharField(max_length=100, verbose_name='Nama Kategori')
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name='Kategori Induk')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Kategori Peralatan'
        verbose_name_plural = 'Kategori Peralatan'
        ordering = ['name']
        unique_together = ['name', 'parent']  # Nama unik per level
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    @property
    def full_path(self):
        """Mengembalikan path lengkap kategori"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name
    
    @classmethod
    def get_root_categories(cls):
        """Mengembalikan kategori level teratas (tanpa parent)"""
        return cls.objects.filter(parent=None)
    
    def get_children(self):
        """Mengembalikan sub-kategori"""
        return self.children.all()
    
    def has_children(self):
        """Cek apakah kategori memiliki sub-kategori"""
        return self.children.exists()

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
    location = models.CharField(max_length=200, blank=True, verbose_name='Lokasi/Tempat')
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
