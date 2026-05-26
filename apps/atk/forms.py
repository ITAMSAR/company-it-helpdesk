from django import forms

from .models import ATKRequest


class ATKRequestForm(forms.ModelForm):
    class Meta:
        model = ATKRequest
        fields = ['purpose']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purpose'].widget.attrs.update({'rows': 4})
