from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('create/', views.create_report, name='create_report'),
    path('list/', views.list_reports, name='list_reports'),
    path('my-reports/', views.my_reports, name='my_reports'),
]
