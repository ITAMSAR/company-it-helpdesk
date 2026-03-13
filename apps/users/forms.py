from django import forms
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
