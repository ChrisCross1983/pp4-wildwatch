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
            report.publication_status = "Pending"
            report.status = "Open"
            report.save()
            
            send_mail(
                "New Report Submitted - Review Required",
                f"A new report titled '{report.title}' has been submitted by {request.user.username}.\n\n"
                "Please review it in the pending reports section.",
                'WildWatch Admin <cborza83@gmail.com>',
                ['cborza83@gmail.com'],
                fail_silently=False,
            )

            if request.user.email:
                subject = "Your WildWatch Report is Pending"
                message = (
                    f"Hello {request.user.username},\n\n"
                    f"Thank you for submitting your report titled '{report.title}'.\n\n"
                    "Your report is currently under review by our team. "
                    "We will notify you once it has been approved or if further information is required.\n\n"
                    "Thank you for helping us protect wildlife.\n\n"
                    "WildWatch Team"
                )
                send_mail(
                    subject,
                    message,
                    'WildWatch Admin <cborza83@gmail.com>',
                    [request.user.email],
                    fail_silently=False,
                )

            messages.success(request, "Your report has been successfully submitted!")
            return redirect('reports:my_reports')
    else:
        form = InjuryReportForm()
    return render(request, 'reports/create_report.html', {'form': form})

@login_required
def all_reports(request):

    reports = InjuryReport.objects.filter(publication_status="Approved", status__in=["Open", "In Progress"]).order_by('-date_reported')

    query = request.GET.get('query', '').strip()
    species = request.GET.get('species')
    injury_condition = request.GET.get('injury_condition')
    report_status = request.GET.get('status_filter')
    user_filter = request.GET.get('user')

    if query:
        reports = reports.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(species__icontains=query) |
            Q(injury_condition__icontains=query) |
            Q(reported_by__username__icontains=query)
        )

    if species:
        reports = reports.filter(species=species)

    if injury_condition:
        reports = reports.filter(injury_condition=injury_condition)

    if report_status:
        reports = reports.filter(status=report_status)

    if user_filter == "self":
        reports = reports.filter(reported_by=request.user)

    results_count = reports.count()

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
    reports = InjuryReport.objects.filter(reported_by=request.user).order_by('-date_reported')
    return render(request, 'reports/my_reports.html', {'reports': reports})

@login_required
def edit_report(request, report_id):
    if request.user.is_staff:
        report = get_object_or_404(InjuryReport, id=report_id)
    else:
        report = get_object_or_404(InjuryReport, id=report_id, reported_by=request.user)

    old_data = {field.name: getattr(report, field.name) for field in report._meta.fields}

    if request.method == 'POST':
        form = InjuryReportForm(request.POST, request.FILES, instance=report)

        if form.is_valid():
            updated_fields = {}
            for field in form.changed_data:
                old_value = old_data.get(field, "N/A")
                new_value = form.cleaned_data.get(field, "N/A")
                updated_fields[field] = (old_value, new_value)

            changes = "\n".join([f"Field '{field}' changed from '{old}' to '{new}'"
                                 for field, (old, new) in updated_fields.items()])

            # Resubmission logic: Change status to pending and notify admin
            if report.publication_status == "Rejected":
                report.publication_status = "Pending"
                report.add_to_history(request.user, f"User resubmitted the report after rejection:\n{changes}")
                messages.success(request, "The report has been resubmitted for approval.")

                # Notify Admin
                send_mail(
                    "Report Resubmitted for Approval",
                    f"Report '{report.title}' has been resubmitted by {request.user.username}.\n\n"
                    "Please review it in the pending reports section.",
                    'WildWatch <cborza83@gmail.com>',
                    ['cborza83@gmail.com'],
                    fail_silently=False,
                )

            # General edit: Add changes to history only if fields were updated
            elif updated_fields:
                report.add_to_history(request.user, f"Report edited:\n{changes}")

            # Notify Admin for a new submission (or resubmit, covered above)
            if report.publication_status == "Pending" and not report.id:
                send_mail(
                    "New Report Submitted - Review Required",
                    f"A new report titled '{report.title}' has been submitted by {request.user.username}.\n\n"
                    "Please review it in the pending reports section.",
                    'WildWatch Admin <cborza83@gmail.com>',
                    ['cborza83@gmail.com'],
                    fail_silently=False,
                )

            # Notify User (on successful resubmission or edit)
            if report.publication_status == "Pending" and report.reported_by.email:
                send_mail(
                    "Your WildWatch Report Was Resubmitted",
                    f"Hello {report.reported_by.username},\n\n"
                    f"Your report titled '{report.title}' has been resubmitted and is now pending approval.\n\n"
                    "Thank you for your patience.\n\n"
                    "WildWatch Team",
                    'WildWatch Admin <cborza83@gmail.com>',
                    [report.reported_by.email],
                    fail_silently=False,
                )

            # Save the form
            form.save()

            return redirect('reports:my_reports')

    else:
        form = InjuryReportForm(instance=report)

    return render(request, 'reports/edit_report.html', {'form': form, 'report': report})

@login_required
@user_passes_test(is_staff_user)
def approve_report(request, report_id):
    report = get_object_or_404(InjuryReport, id=report_id)
    report.publication_status = "Approved"
    if report.status == "Pending":
        report.status = "Open"
    report.save()

    if report.reported_by.email:
        subject = "Your WildWatch Report was Approved"
        message = (
            f"Hello {report.reported_by.username},\n\n"
            f"Your updated report titled '{report.title}' has been approved.\n\n"
            "Thank you for your contribution to protecting wildlife.\n\n"
            "WildWatch Team"
        )
        send_mail(
            subject,
            message,
            'WildWatch Admin <cborza83@gmail.com>',
            [report.reported_by.email],
            fail_silently=False,
        )

    messages.success(request, f"The report '{report.title}' has been approved.")
    return redirect('reports:pending_reports')

@login_required
@user_passes_test(is_staff_user)
def reject_report(request, report_id):
    report = get_object_or_404(InjuryReport, id=report_id)
    
    if request.method == 'POST':
        admin_comment = request.POST.get('admin_comment', '').strip()
        if not admin_comment:
            messages.error(request, "A comment is required to reject a report.")
            return redirect('reports:reject_report', report_id=report.id)
        
        # Set publication_status to Rejected
        report.publication_status = "Rejected"
        report.add_to_history(request.user, f"Admin rejected: {admin_comment}")
        report.admin_comment = admin_comment
        report.save()
        
        if report.reported_by and report.reported_by.email:
            subject = "Your WildWatch Report Has Been Rejected"
            message = (
                f"Hello {report.reported_by.username},\n\n"
                f"Your report for '{report.title}' has been rejected by the admin.\n\n"
                f"Reason: {admin_comment}\n\n"
                "You can edit your report to provide more accurate details and resubmit it.\n"
                f"Click the link below to edit your report:\n"
                f"{request.build_absolute_uri(reverse('reports:edit_report', args=[report.id]))}\n\n"
                "Thank you for helping us protect wildlife.\n\n"
                "WildWatch Team"
            )
            send_mail(
                subject,
                message,
                'WildWatch Admin <cborza83@gmail.com>',
                [report.reported_by.email],
                fail_silently=False,
            )

        messages.success(request, f"The report '{report.title}' has been rejected, and the user has been notified.")
        return redirect('reports:pending_reports')
    
    return render(request, 'reports/reject_report.html', {'report': report})

@user_passes_test(is_staff_user)
def pending_reports(request):

    pending_reports = InjuryReport.objects.filter(publication_status="Pending").order_by('-date_reported')
    rejected_reports = InjuryReport.objects.filter(publication_status="Rejected").order_by('-date_reported')

    status_filter = request.GET.get('filter_status')
    if status_filter == "Pending":
        rejected_reports = []
    elif status_filter == "Rejected":
        pending_reports = []

    return render(request, 'reports/pending_reports.html', {
        'pending_reports': pending_reports,
        'rejected_reports': rejected_reports,
    })

@login_required
def take_care_of_report(request, report_id):
    report = get_object_or_404(InjuryReport, id=report_id)
    if report.status == "Open":
        report.set_status("In Progress", user=request.user)
        messages.success(request, "You are now taking care of this report.")
        
        if report.reported_by and report.reported_by.email:
            send_mail(
                "WildWatch: Help for your case",
                f"Hello {report.reported_by.username},\n\n"
                f"The user {request.user.username} has agreed to help with your reported case ('{report.title}').\n"
                "Thank you for your support in protecting the animals!\n\n"
                "WildWatch Team",
                "WildWatch <cborza83@gmail.com>",
                [report.reported_by.email],
            )
    else:
        messages.error(request, "This case can no longer be accepted.")

    return redirect('reports:all_reports')

@login_required
def delete_report(request, report_id):
    report = get_object_or_404(InjuryReport, id=report_id)
    
    if request.user == report.reported_by or request.user.is_staff:
        report.delete()
        messages.success(request, "The report has been successfully deleted.")
    else:
        messages.error(request, "You are not authorized to delete this report.")
    
    return redirect('reports:my_reports')

@login_required
def close_report(request, report_id):
    report = get_object_or_404(InjuryReport, id=report_id)

    if request.user == report.helper or request.user.is_staff:
        if request.method == "POST":
            report.set_status("Completed")
            messages.success(request, "The report has been marked as completed.")

            if report.reported_by and report.reported_by.email:
                send_mail(
                    "WildWatch: Report closed",
                    f"Hello {report.reported_by.username},\n\n"
                    f"The report titled '{report.title}' has been successfully completed by "
                    f"{request.user.username}.\n\n"
                    "Thank you for your continued support in protecting wildlife!\n\n"
                    "WildWatch Team",
                    "WildWatch <cborza83@gmail.com>",
                    [report.reported_by.email],
                )

            if report.helper and report.helper.email:
                send_mail(
                    "WildWatch: Report successfully closed",
                    f"Hello {report.helper.username},\n\n"
                    f"You have successfully completed the report titled '{report.title}'.\n\n"
                    "Thank you for your efforts in protecting wildlife!\n\n"
                    "WildWatch Team",
                    "WildWatch <cborza83@gmail.com>",
                    [report.helper.email],
                )
            return redirect('reports:my_reports')

        return render(request, 'reports/close_report.html', {'report': report})

    messages.error(request, "You are not authorized to close this report.")
    return redirect('reports:my_reports')


@login_required
def help_report(request, report_id):
    report = get_object_or_404(InjuryReport, id=report_id)
    if report.status == "Open" and not report.helper:
        report.helper = request.user
        report.status = "In Progress"
        report.save()

        # Optional: Mail to report creater
        if report.reported_by and report.reported_by.email:
            send_mail(
                "WildWatch: Help for your case",
                f"Hallo {report.reported_by.username},\n\n"
                f"The user {request.user.username} has agreed to help with your reported case ('{report.title}').\n"
                "Thank you for your support in protecting the animals!\n\n"
                "WildWatch Team",
                "WildWatch <cborza83@gmail.com>",
                [report.reported_by.email],
                fail_silently=False,
            )

        messages.success(request, f"You are now helping with this report.")
    else:
        messages.error(request, "This report is no longer available for help.")
    return redirect('reports:all_reports')
