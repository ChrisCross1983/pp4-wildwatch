from django.urls import path
from users import views as user_views

urlpatterns = [
    path('', user_views.home, name='home'),
]