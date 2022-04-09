from dataclasses import field
from django import forms
from .models import IdInfo


class IdInfoForm(forms.ModelForm):
    address = forms.CharField(max_length=100, help_text='100 characters max.', required=True,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))

    class Meta:
        model = IdInfo
        fields = [
            'first_name',
            'last_name',
            'position',
            'contact',
            'emergency_contact_name',
            'contact_number',
            'address',
            'blood_type',
            'birth_date',
            'image',
            'signature'
        ]
