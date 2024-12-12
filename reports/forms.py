from django import forms
from .models import AnimalReport

class ReportForm(forms.ModelForm):
    class Meta:
        model = AnimalReport
        fields = ['species', 'location', 'status']