from django.shortcuts import render
from django import forms
from django.http import HttpResponse

# Create your views here.

def about(response):
    return render(response, 'aboutUs.html')

def results(response):
    return render(response, 'result.html')

def search(request):
    return render(request, 'index.html')

def query(request):
    if request.method == 'POST':
        print(request.POST)