from django.shortcuts import render
from django import forms
from django.http import HttpRequest

# Create your views here.

def about(response):
    return render(response, 'aboutUs.html')

def results(response):
    return render(response, 'result.html')

def search(response):
    return render(response, 'index.html')

def query(request):
    if request.method == 'POST':
        q = request.POST['query']
        print(q)
        return render(request, 'result.html', {'query': q})