from django.db import models
from django.contrib.auth.models import User
from apps.inventory.models import Equipment

class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi'),
        ('urgent', 'Darurat'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Baru'),
        ('in_progress', 'Sedang Dikerjakan'),
        ('completed', 'Selesai'),
        ('cancelled', 'Tidak Selesai'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Judul Tiket')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets', verbose_name='Pelapor')
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='tickets', verbose_name='Barang Terkait')
    description = models.TextField(verbose_name='Deskripsi Masalah')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name='Prioritas')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Status')
    notes = models.TextField(blank=True, verbose_name='Catatan', help_text='Catatan saat tiket selesai atau tidak selesai')
    attachment = models.FileField(upload_to='tickets/', null=True, blank=True, verbose_name='Lampiran')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Dibuat')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Selesai')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tiket'
        verbose_name_plural = 'Tiket'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.reporter.username}"

