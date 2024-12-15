from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('create/', views.create_report, name='create_report'),
    path('all/', views.all_reports, name='all_reports'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('<int:report_id>/', views.report_detail, name='report_detail'),
]
