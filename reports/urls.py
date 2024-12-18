from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('create/', views.create_report, name='create_report'),
    path('all/', views.all_reports, name='all_reports'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('<int:report_id>/', views.report_detail, name='report_detail'),
    path('<int:report_id>/edit/', views.edit_report, name='edit_report'),
    path('approve/<int:report_id>/', views.approve_report, name='approve_report'),
    path('reject/<int:report_id>/', views.reject_report, name='reject_report'),
    path('pending-reports/', views.pending_reports, name='pending_reports'),
    path('help/<int:report_id>/', views.help_report, name='help_report'),
    path('reports/<int:report_id>/cancel_help/', views.cancel_help, name='cancel_help'),
    path('<int:report_id>/close/', views.close_report, name='close_report'),
    path('<int:report_id>/delete/', views.delete_report, name='delete_report'),
]
