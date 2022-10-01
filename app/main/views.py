from django.shortcuts import render
from django import forms
from django.http import HttpResponse

# Create your views here.

responses = HttpResponse()

def about(response):
    return render(response, 'aboutUs.html')

def results(response):
    query = responses.get('query')
    return render(response, 'result.html', {'query': query})

def search(response):
    return render(response, 'index.html')

def query(request):
    if request.method == 'POST':
        q = str(request.POST['query'])
        print(q)
        responses.headers['query'] = q