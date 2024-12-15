from django import forms
from .models import InjuryReport

class InjuryReportForm(forms.ModelForm):
    class Meta:
        model = InjuryReport
        fields = ['species', 'gender', 'injury_condition', 'description', 'location', 'image']
        labels = {
            'species': 'Species',
            'description': 'Description of the animal and injury',
            'location': 'Location (e.g., city or GPS coordinates)',
            'injury_condition': 'Condition',
            'image': 'Upload an image (optional)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
