from django.shortcuts import render, get_object_or_404, redirect
from .models import InjuryReport, Location, ReportStatus, Animal, Species, Gender, InjuryCondition
from .forms import ReportForm

# Create a new animal injury report
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('reports:report_list')
    else:
        form = ReportForm()
    return render(request, 'reports/create_report.html', {'form': form})

# List all injury reports
def report_list(request):
    reports = InjuryReport.objects.all().order_by('-date_reported')
    return render(request, 'reports/report_list.html', {'reports': reports})

# Detail view for a specific report
def report_detail(request, report_id):
    report = get_object_or_404(InjuryReport, id=report_id)
    return render(request, 'reports/report_detail.html', {'report': report})

