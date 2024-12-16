from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import InjuryReport
from .forms import InjuryReportForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.mail import send_mail


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
    reports = InjuryReport.objects.exclude(status="Rejected").order_by('-date_reported')

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
    # Allow admins to edit any report, but non-admin users can only edit their own
    if request.user.is_staff:
        report = get_object_or_404(InjuryReport, id=report_id)
    else:
        report = get_object_or_404(InjuryReport, id=report_id, reported_by=request.user)

    if request.method == 'POST':
        form = InjuryReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "The report has been updated successfully!")
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
    if request.method == 'POST':
        admin_comment = request.POST.get('admin_comment', 'No specific reason provided by the admin.')
        report.status = "Rejected"
        report.admin_comment = admin_comment
        report.save()
        
        # Send Email to user
        if report.reported_by and report.reported_by.email:
            subject = "Your WildWatch Report Has Been Rejected"
            message = (
                f"Hello {report.reported_by.username},\n\n"
                f"Your report for '{report.species}' has been rejected by the admin.\n\n"
                f"Reason: {admin_comment}\n\n"
                f"You can edit your report here:\n"
                f"Click the link below to edit your report:\n"
                f"{request.build_absolute_uri(reverse('reports:edit_report', args=[report.id]))}\n\n"
                "Thank you for helping us protect wildlife.\n\n"
                "WildWatch Team"
            )
            send_mail(
                subject,
                message,
                'WildWatch <cborza83@gmail.com>',
                [report.reported_by.email],
                fail_silently=False,
            )

        messages.success(request, f"The report '{report.species}' has been rejected, and the user has been notified.")
        return redirect('reports:pending_reports')
    return render(request, 'reports/reject_report.html', {'report': report})

@user_passes_test(is_staff_user)
def pending_reports(request):

    pending_reports = InjuryReport.objects.filter(status="Pending").order_by('-date_reported')
    rejected_reports = InjuryReport.objects.filter(status="Rejected").order_by('-date_reported')

    # Filter logic
    status_filter = request.GET.get('filter_status')
    if status_filter == "Pending":
        rejected_reports = []
    elif status_filter == "Rejected":
        pending_reports = []

    return render(request, 'reports/pending_reports.html', {
        'pending_reports': pending_reports,
        'rejected_reports': rejected_reports,
    })
