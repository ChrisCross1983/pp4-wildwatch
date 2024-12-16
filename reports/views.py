from django.shortcuts import render, redirect, get_object_or_404
from .models import InjuryReport
from .forms import InjuryReportForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect

def is_staff_user(user):
    return user.is_staff

@login_required
def create_report(request):
    if request.method == 'POST':
        form = InjuryReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user
            report.status = "Pending"
            report.save()
            messages.success(request, "Your report has been successfully submitted!")
            return redirect('reports:all_reports')
    else:
        form = InjuryReportForm()
    return render(request, 'reports/create_report.html', {'form': form})

@login_required
def all_reports(request):
    reports = InjuryReport.objects.all().order_by('-date_reported')

    query = request.GET.get('query')
    species = request.GET.get('species')
    status = request.GET.get('status')

    if query:
        reports = reports.filter(
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(species__icontains=query) |
            Q(injury_condition__icontains=query) |
            Q(reported_by__username__icontains=query)
        )
    if species:
        reports = reports.filter(species=species)
    if status:
        reports = reports.filter(status=status)

    # Count results
    results_count = reports.count()

    # Pagination
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reports/all_reports.html', {
        'page_obj': page_obj,
        'query': query,
        'results_count': results_count,
    })

def report_detail(request, report_id):
    report = get_object_or_404(InjuryReport, id=report_id)
    return render(request, 'reports/report_detail.html', {'report': report})

@login_required
def my_reports(request):
    reports = InjuryReport.objects.filter(reported_by=request.user)
    return render(request, 'reports/my_reports.html', {'reports': reports})

@login_required
def edit_report(request, report_id):
    report = get_object_or_404(InjuryReport, id=report_id, reported_by=request.user)
    
    if request.method == 'POST':
        form = InjuryReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "Your report has been updated successfully!")
            return redirect('reports:report_detail', report_id=report.id)
    else:
        form = InjuryReportForm(instance=report)

    return render(request, 'reports/edit_report.html', {'form': form, 'report': report})

@login_required
@user_passes_test(is_staff_user)
def approve_report(request, report_id):
    report = get_object_or_404(InjuryReport, id=report_id)
    report.status = "Approved"
    report.save()
    messages.success(request, f"The report '{report.species}' has been approved.")
    return redirect('reports:pending_reports')

@login_required
@user_passes_test(is_staff_user)
def reject_report(request, report_id):
    report = get_object_or_404(InjuryReport, id=report_id)
    report.status = "Rejected"
    report.save()
    messages.success(request, f"The report '{report.species}' has been rejected.")
    return redirect('reports:pending_reports')

@login_required
@user_passes_test(is_staff_user)
def pending_reports(request):
    reports = InjuryReport.objects.filter(status="Pending").order_by('-date_reported')
    return render(request, 'reports/pending_reports.html', {'reports': reports})
