from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import EmployeeEmail


class EmployeeEmailForm(forms.ModelForm):
    class Meta:
        model = EmployeeEmail
        fields = ['full_name', 'employee_id', 'primary_email', 'email_password', 
                  'recovery_email', 'recovery_phone', 'is_active']
        widgets = {
            'primary_email': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Masukkan satu atau beberapa email (pisahkan dengan koma)\nContoh: user@example.com, user.work@company.com'
            }),
        }
    
    def clean_primary_email(self):
        """Validate multiple emails separated by comma"""
        emails_text = self.cleaned_data.get('primary_email', '')
        
        if not emails_text:
            raise ValidationError('Email tidak boleh kosong')
        
        # Split by comma and validate each email
        email_list = [e.strip() for e in emails_text.split(',') if e.strip()]
        
        if not email_list:
            raise ValidationError('Minimal harus ada satu email yang valid')
        
        # Validate each email
        invalid_emails = []
        for email in email_list:
            try:
                validate_email(email)
            except ValidationError:
                invalid_emails.append(email)
        
        if invalid_emails:
            raise ValidationError(
                f'Email tidak valid: {", ".join(invalid_emails)}'
            )
        
        # Return cleaned emails (joined back with comma)
        return ', '.join(email_list)


class AccountCreateForm(UserCreationForm):
    email = forms.EmailField(required=False, label='Email')
    first_name = forms.CharField(required=False, max_length=150, label='Nama Depan')
    last_name = forms.CharField(required=False, max_length=150, label='Nama Belakang')
    is_staff = forms.BooleanField(required=False, label='Administrator')
    is_active = forms.BooleanField(required=False, initial=True, label='Aktif')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'is_staff',
            'is_active',
        ]


class AccountUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label='Password Baru',
        help_text='Kosongkan jika tidak ingin mengganti password.'
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label='Konfirmasi Password Baru'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise ValidationError('Konfirmasi password tidak sama.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
