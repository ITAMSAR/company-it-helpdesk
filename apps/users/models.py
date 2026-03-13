from django.db import models
from django.contrib.auth.models import User

class EmployeeEmail(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='Nama Lengkap')
    employee_id = models.CharField(max_length=50, unique=True, verbose_name='NIK/ID Karyawan')
    primary_email = models.TextField(verbose_name='Email Utama')  # Changed to TextField for multiple emails
    email_password = models.CharField(max_length=255, verbose_name='Password Email')
    recovery_email = models.EmailField(blank=True, null=True, verbose_name='Email Recovery')
    recovery_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='No HP Recovery')
    is_active = models.BooleanField(default=True, verbose_name='Status Aktif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Dibuat')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Email Karyawan'
        verbose_name_plural = 'Email Karyawan'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"
    
    def get_email_list(self):
        """Return list of emails"""
        return [e.strip() for e in self.primary_email.split(',') if e.strip()]

