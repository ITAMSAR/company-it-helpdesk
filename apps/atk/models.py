from django.db import models
from django.contrib.auth.models import User

class ATKCategory(models.Model):
    """Kategori ATK seperti Alat Tulis, Kertas, dll"""
    name = models.CharField(max_length=100, db_index=True, verbose_name='Nama Kategori')
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
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
    
    name = models.CharField(max_length=200, db_index=True, verbose_name='Nama ATK')
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
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Item ATK'
        verbose_name_plural = 'Item ATK'
        ordering = ['name']
        indexes = [
            models.Index(fields=['category', 'name'], name='atk_item_category_name_idx'),
        ]
    
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


class ATKRequest(models.Model):
    """Pengajuan kebutuhan ATK dari user ke admin."""
    STATUS_CHOICES = [
        ('pending', 'Menunggu Persetujuan'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='atk_requests', verbose_name='Pemohon')
    item = models.ForeignKey(
        ATKItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requests',
        verbose_name='Item ATK'
    )
    custom_item_name = models.CharField(max_length=200, blank=True, verbose_name='Nama Item Lainnya')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Jumlah')
    purpose = models.TextField(verbose_name='Keperluan')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True, verbose_name='Status')
    admin_notes = models.TextField(blank=True, verbose_name='Catatan Admin')
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_atk_requests',
        verbose_name='Direview Oleh'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Review')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Tanggal Pengajuan')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pengajuan ATK'
        verbose_name_plural = 'Pengajuan ATK'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['requester', 'status', '-created_at'], name='atk_req_requester_status_idx'),
            models.Index(fields=['status', '-created_at'], name='atk_req_status_created_idx'),
        ]

    def __str__(self):
        return f"{self.display_item_name} - {self.requester.username}"

    @property
    def display_item_name(self):
        lines = list(self.lines.all()[:2])
        if lines:
            first_name = lines[0].display_item_name
            extra_count = self.lines.count() - 1
            if extra_count > 0:
                return f"{first_name} +{extra_count} item"
            return first_name
        return self.item.name if self.item else self.custom_item_name

    @property
    def total_quantity(self):
        lines = list(self.lines.all())
        if lines:
            return sum(line.quantity for line in lines)
        return self.quantity


class ATKRequestLine(models.Model):
    """Baris item dalam satu pengajuan ATK."""
    request = models.ForeignKey(ATKRequest, on_delete=models.CASCADE, related_name='lines', verbose_name='Pengajuan')
    item = models.ForeignKey(
        ATKItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='request_lines',
        verbose_name='Item ATK'
    )
    custom_item_name = models.CharField(max_length=200, blank=True, verbose_name='Nama Item Lainnya')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Jumlah')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Item Pengajuan ATK'
        verbose_name_plural = 'Item Pengajuan ATK'
        ordering = ['id']

    def __str__(self):
        return f"{self.display_item_name} x {self.quantity}"

    @property
    def display_item_name(self):
        return self.item.name if self.item else self.custom_item_name
