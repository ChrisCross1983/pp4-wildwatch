from django import forms
from .models import InjuryReport

class InjuryReportForm(forms.ModelForm):
    class Meta:
        model = InjuryReport
        fields = ['title', 'species', 'gender', 'injury_condition', 'description', 'location', 'image']
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
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("The title must be at least 5 characters long.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description.split()) < 10:
            raise forms.ValidationError("The description must be at least 10 words.")
        return description
