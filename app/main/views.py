from django.shortcuts import render
from django import forms
from django.http import HttpResponse

# Create your views here.

def about(response):
    return render(response, 'aboutUs.html')

def results(response):
    return render(response, 'results.html')

def search(request):
    return render(request, 'index.html')