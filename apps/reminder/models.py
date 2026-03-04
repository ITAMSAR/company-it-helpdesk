from django.db import models
from django.contrib.auth.models import User

class NetworkCheckLog(models.Model):
    checked_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Dicek Oleh')
    checked_at = models.DateTimeField(auto_now_add=True, verbose_name='Waktu Pengecekan')
    notes = models.TextField(blank=True, verbose_name='Catatan')

    class Meta:
        verbose_name = 'Log Pengecekan Jaringan'
        verbose_name_plural = 'Log Pengecekan Jaringan'
        ordering = ['-checked_at']

    def __str__(self):
        return f"Cek oleh {self.checked_by.username} pada {self.checked_at}"
