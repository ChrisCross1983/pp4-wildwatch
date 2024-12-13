from django.shortcuts import render, redirect
from .models import InjuryReport
from .forms import InjuryReportForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def create_report(request):
    if request.method == 'POST':
        form = InjuryReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'reports/report_success.html')
    else:
        form = InjuryReportForm()
    return render(request, 'reports/create_report.html', {'form': form})

def list_reports(request):
    reports = InjuryReport.objects.all()
    return render(request, 'reports/list_reports.html', {'reports': reports})

@login_required
def create_report(request):
    if request.method == 'POST':
        form = InjuryReportForm(request.POST, request.FILES)
        if form.is_valid():
            injury_report = form.save(commit=False)
            injury_report.reported_by = request.user
            injury_report.save()
            return render(request, 'reports/report_success.html')
    else:
        form = InjuryReportForm()
    return render(request, 'reports/create_report.html', {'form': form})

@login_required
def my_reports(request):
    reports = InjuryReport.objects.filter(reported_by=request.user)
    return render(request, 'reports/my_reports.html', {'reports': reports})