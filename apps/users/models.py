from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet, InvalidToken
import base64
import hashlib


def _password_cipher():
    digest = hashlib.sha256(settings.EMAIL_PASSWORD_SECRET.encode('utf-8')).digest()
    return Fernet(base64.urlsafe_b64encode(digest))

class EmployeeEmail(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='Nama Lengkap')
    employee_id = models.CharField(max_length=50, unique=True, verbose_name='NIK/ID Karyawan')
    primary_email = models.TextField(verbose_name='Email Utama')  # Changed to TextField for multiple emails
    email_password = models.TextField(verbose_name='Password Email')
    recovery_email = models.EmailField(blank=True, null=True, verbose_name='Email Recovery')
    recovery_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='No HP Recovery')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Status Aktif')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Tanggal Dibuat')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Email Karyawan'
        verbose_name_plural = 'Email Karyawan'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', '-created_at'], name='email_active_created_idx'),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"

    def _is_encrypted_password(self):
        return isinstance(self.email_password, str) and self.email_password.startswith('fernet:')

    def get_plain_email_password(self):
        if not self.email_password:
            return ''
        if not self._is_encrypted_password():
            return self.email_password
        try:
            token = self.email_password.removeprefix('fernet:').encode('utf-8')
            return _password_cipher().decrypt(token).decode('utf-8')
        except (InvalidToken, ValueError):
            return ''

    def save(self, *args, **kwargs):
        if self.email_password and not self._is_encrypted_password():
            encrypted = _password_cipher().encrypt(self.email_password.encode('utf-8')).decode('utf-8')
            self.email_password = f'fernet:{encrypted}'
        super().save(*args, **kwargs)
    
    def get_email_list(self):
        """Return list of emails"""
        return [e.strip() for e in self.primary_email.split(',') if e.strip()]

