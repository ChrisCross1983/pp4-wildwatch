from django.shortcuts import render, redirect, get_object_or_404
from .models import InjuryReport
from .forms import InjuryReportForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

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

def all_reports(request):
    reports = InjuryReport.objects.all().order_by('-date_reported')


    species = request.GET.get('species')
    status = request.GET.get('status')
    if species:
        reports = reports.filter(species=species)
    if status:
        reports = reports.filter(injury_condition=status)

    # Pagination
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reports/all_reports.html', {'page_obj': page_obj})

def report_detail(request, report_id):
    report = get_object_or_404(InjuryReport, id=report_id)
    return render(request, 'reports/report_detail.html', {'report': report})

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
