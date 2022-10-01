from urllib import request
from django.shortcuts import render
from django import forms
from django.http import HttpRequest

# Create your views here.

def about(response):
    return render(response, 'aboutUs.html')

def results(request):
    return render(request, 'result.html')

def search(request):
    return render(request, 'index.html')

def query(request):
    if request.method == 'POST':
        q = request.POST['query']
        print(q)
        request.session['q'] = q