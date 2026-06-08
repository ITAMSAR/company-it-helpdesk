from django.conf import settings
from django.db import migrations
from cryptography.fernet import Fernet
import base64
import hashlib


def _cipher():
    secret = getattr(settings, 'EMAIL_PASSWORD_SECRET', settings.SECRET_KEY)
    digest = hashlib.sha256(secret.encode('utf-8')).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def encrypt_existing_passwords(apps, schema_editor):
    EmployeeEmail = apps.get_model('users', 'EmployeeEmail')
    cipher = _cipher()

    for employee_email in EmployeeEmail.objects.exclude(email_password=''):
        password = employee_email.email_password
        if not password or password.startswith('fernet:'):
            continue
        encrypted = cipher.encrypt(password.encode('utf-8')).decode('utf-8')
        employee_email.email_password = f'fernet:{encrypted}'
        employee_email.save(update_fields=['email_password'])


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_employeeemail_created_at_and_more'),
    ]

    operations = [
        migrations.RunPython(encrypt_existing_passwords, migrations.RunPython.noop),
    ]
