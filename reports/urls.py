from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Default page (redirect to all_reports)
    path('', views.all_reports, name='home'), 
    path('all/', views.all_reports, name='all_reports'),

    # Report management paths
    path('create/', views.create_report, name='create_report'),
    path('<int:report_id>/', views.report_detail, name='report_detail'),
    path('<int:report_id>/edit/', views.edit_report, name='edit_report'),
    path('<int:report_id>/delete/', views.delete_report, name='delete_report'),

    # Admin actions
    path('approve/<int:report_id>/', views.approve_report, name='approve_report'),
    path('reject/<int:report_id>/', views.reject_report, name='reject_report'),
    path('pending-reports/', views.pending_reports, name='pending_reports'),

    # Helper actions
    path('<int:report_id>/help/', views.help_report, name='help_report'),
    path('<int:report_id>/cancel_help/', views.cancel_help, name='cancel_help'),

    # Closing reports
    path('<int:report_id>/close/', views.close_report, name='close_report'),

    # User-specific reports
    path('my-reports/', views.my_reports, name='my_reports'),
]
