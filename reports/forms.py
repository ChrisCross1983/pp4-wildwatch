from django import forms
from .models import InjuryReport

class ReportForm(forms.ModelForm):
    class Meta:
        model = InjuryReport
        fields = [
            'description',
            'reported_by',
            'animal',
            'report_status',
            'location',
            'comments',
            'image',
        ]
