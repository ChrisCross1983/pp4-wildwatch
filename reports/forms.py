from django import forms
from .models import InjuryReport

class InjuryReportForm(forms.ModelForm):
    class Meta:
        model = InjuryReport
        fields = ['description', 'species', 'gender', 'injury_condition', 'location', 'image']
