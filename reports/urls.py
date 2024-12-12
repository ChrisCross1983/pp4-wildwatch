from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('create/', views.create_report, name='create_report'),
    path('', views.report_list, name='report_list'),
    path('<int:pk>/', views.report_detail, name='report_detail'),
]
