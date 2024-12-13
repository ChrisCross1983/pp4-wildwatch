from django import forms
from .models import InjuryReport

class InjuryReportForm(forms.ModelForm):
    class Meta:
        model = InjuryReport
        fields = ['species', 'gender', 'injury_condition', 'description', 'location', 'image']
