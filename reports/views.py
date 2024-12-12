from django.shortcuts import render, redirect
from .forms import InjuryReportForm

def create_report(request):
    if request.method == 'POST':
        form = InjuryReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'reports/success.html')  # Erfolgsseite
    else:
        form = InjuryReportForm()
    return render(request, 'reports/create_report.html', {'form': form})
