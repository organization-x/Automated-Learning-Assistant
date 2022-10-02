from django.shortcuts import render
from django.http import HttpResponse
import openai
import os

# Create your views here.

responses = HttpResponse()

def about(response):
    return render(response, 'aboutUs.html')

def results(response):
    query = responses.get('query')
    openai.api_key = "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"
    p = f"Explain in informative terms to a non programmer in 300 words. {query}"
    resp = openai.Completion.create(
        model="text-davinci-002",
        prompt= p,
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
)
    resps = {'response': resp["choices"][0]["text"], 'query': query}
    return render(response, 'result.html', resps)

def search(response):
    return render(response, 'index.html')

def query(request):
    if request.method == 'POST':
        q = str(request.POST['query'])
        print(q)
        responses.headers['query'] = q