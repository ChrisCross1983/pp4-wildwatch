from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to WildWatch")

def robots_txt_view(request):
    return HttpResponse("User-agent: *\nDisallow:", content_type="text/plain")