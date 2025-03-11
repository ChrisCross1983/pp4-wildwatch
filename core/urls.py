from django.urls import path
from users import views as user_views
from .views import robots_txt_view

urlpatterns = [
    path('', user_views.home, name='home'),
    path("robots.txt", robots_txt_view, name="robots_txt"),
]
