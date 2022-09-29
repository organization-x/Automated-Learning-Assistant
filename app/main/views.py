from django.shortcuts import render
from django.http import HttpResponse
from .models import ToDo, Item

# Create your views here.

def home(response):
    return render(response, 'home.html')

def about(response):
    return render(response, 'aboutUs.html')

def results(response):
    return render(response, 'home.html')