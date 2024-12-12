from django.shortcuts import render, get_object_or_404
from .models import AnimalReport

# List view for all reports
def report_list(request):
    reports = AnimalReport.objects.all().order_by('-created_at')
    return render(request, 'reports/report_list.html', {'reports': reports})

# Detail view for a individual report
def report_detail(request, report_id):
    report = get_object_or_404(AnimalReport, id=report_id)
    return render(request, 'reports/report_detail.html', {'report': report})
