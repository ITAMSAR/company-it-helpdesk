from django.db import models
from django.contrib.auth.models import User

class EquipmentCategory(models.Model):
    """Model untuk kategori peralatan yang bisa ditambah dinamis dengan hierarki"""
    name = models.CharField(max_length=100, db_index=True, verbose_name='Nama Kategori')
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name='Kategori Induk')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = 'Kategori Peralatan'
        verbose_name_plural = 'Kategori Peralatan'
        ordering = ['name']
        unique_together = ['name', 'parent']  # Nama unik per level
        indexes = [
            models.Index(fields=['parent', 'name'], name='equip_cat_parent_name_idx'),
        ]
    
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
    
    @property
    def code(self):
        """Generate kode kategori dari nama"""
        # Ambil kata pertama dari nama kategori dan jadikan uppercase
        # Contoh: "Komputer" -> "KOMPUTER", "Meja Kerja" -> "MEJA"
        return self.name.split()[0].upper()
    
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
    
    def get_total_equipment_count(self):
        """Menghitung total equipment termasuk dari sub-kategori"""
        # Equipment langsung di kategori ini
        direct_count = self.equipment.count()
        
        # Equipment di semua sub-kategori
        children_count = 0
        for child in self.children.all():
            children_count += child.get_total_equipment_count()
        
        return direct_count + children_count

class Equipment(models.Model):
    STATUS_CHOICES = [
        ('available', 'Tersedia'),
        ('borrowed', 'Dipinjam'),
        ('broken', 'Rusak'),
        ('service', 'Servis'),
    ]
    
    name = models.CharField(max_length=200, db_index=True, verbose_name='Nama Barang')
    inventory_code = models.CharField(max_length=100, unique=True, verbose_name='Kode Inventaris', blank=True)
    category = models.ForeignKey(EquipmentCategory, on_delete=models.PROTECT, 
                                 related_name='equipment', verbose_name='Kategori')
    specifications = models.TextField(blank=True, verbose_name='Spesifikasi')
    current_user = models.CharField(max_length=200, blank=True, verbose_name='Pengguna Saat Ini')
    location = models.CharField(max_length=200, blank=True, verbose_name='Lokasi/Tempat')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', db_index=True, verbose_name='Status')
    purchase_date = models.DateField(null=True, blank=True, verbose_name='Tanggal Pembelian')
    warranty_until = models.DateField(null=True, blank=True, verbose_name='Garansi Sampai')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Peralatan'
        verbose_name_plural = 'Peralatan'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'status'], name='equip_category_status_idx'),
            models.Index(fields=['status', '-created_at'], name='equip_status_created_idx'),
        ]

    def __str__(self):
        return f"{self.name} ({self.inventory_code})"
    
    def generate_inventory_code(self):
        """Generate kode inventaris otomatis berdasarkan kategori"""
        if not self.category:
            return None
            
        # Format: APM/KATEGORI/XXX
        prefix = "APM"
        category_code = self.category.code  # Menggunakan property code
        
        # Cari nomor urut terakhir untuk kategori ini
        last_equipment = Equipment.objects.filter(
            category=self.category,
            inventory_code__startswith=f"{prefix}/{category_code}/"
        ).order_by('-inventory_code').first()
        
        if last_equipment:
            # Ambil nomor urut dari kode terakhir
            try:
                last_number = int(last_equipment.inventory_code.split('/')[-1])
                next_number = last_number + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        
        # Format nomor dengan 3 digit (001, 002, dst)
        return f"{prefix}/{category_code}/{next_number:03d}"
    
    def save(self, *args, **kwargs):
        # Auto-generate kode inventaris jika belum ada
        if not self.inventory_code:
            self.inventory_code = self.generate_inventory_code()
        super().save(*args, **kwargs)


class EquipmentDeletionLog(models.Model):
    equipment_name = models.CharField(max_length=200, verbose_name='Nama Barang')
    inventory_code = models.CharField(max_length=100, db_index=True, verbose_name='Kode Inventaris')
    category_name = models.CharField(max_length=200, verbose_name='Kategori')
    status = models.CharField(max_length=50, verbose_name='Status Terakhir')
    current_user = models.CharField(max_length=200, blank=True, verbose_name='Pengguna Terakhir')
    location = models.CharField(max_length=200, blank=True, verbose_name='Lokasi Terakhir')
    reason = models.TextField(verbose_name='Alasan Penghapusan')
    attachment = models.FileField(upload_to='inventory/deletion-logs/', null=True, blank=True, verbose_name='Lampiran Penghapusan')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipment_deletion_logs', verbose_name='Dihapus Oleh')
    deleted_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Tanggal Penghapusan')

    class Meta:
        verbose_name = 'Log Penghapusan Aset'
        verbose_name_plural = 'Log Penghapusan Aset'
        ordering = ['-deleted_at']

    def __str__(self):
        return f"{self.inventory_code} dihapus oleh {self.deleted_by or '-'}"

    @classmethod
    def from_equipment(cls, equipment, *, reason, attachment=None, deleted_by=None):
        return cls.objects.create(
            equipment_name=equipment.name,
            inventory_code=equipment.inventory_code,
            category_name=equipment.category.full_path,
            status=equipment.get_status_display(),
            current_user=equipment.current_user,
            location=equipment.location,
            reason=reason,
            attachment=attachment,
            deleted_by=deleted_by,
        )
