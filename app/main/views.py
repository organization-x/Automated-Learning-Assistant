from django.shortcuts import render
from django.http import HttpResponse
import asyncio
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
set_api_key = os.getenv('OPENAI_API_KEY')
responses = HttpResponse()


def getPrompts(searchQuery):
    p1 = f"Explain in informative terms to a non programmer in 300 words. {searchQuery}"
    p2 = f"Give a roadmap that is a series of instructions that someone should take to solve this question. {searchQuery}"
    p3 = f"Return a link with a summary of well formatted code that solves this problem: {searchQuery}"
    prompts = []
    explanation = {
        'prompt': p1,
        'temperature': 0.7,
        'max_tokens': 500,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }
    roadmap = {
        'prompt': p2,
        'temperature': 0.7,
        'max_tokens': 500,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }
    prompts.append(explanation)
    prompts.append(roadmap)
    return prompts


async def get_text(session, url, params):
    async with session.post(url, json=params) as resp:
        text = await resp.json()
        return text['choices'][0]['text']


async def resultsAsync(searchQuery):
    prompts = getPrompts(searchQuery)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers={'authorization': f"Bearer {set_api_key}"}) as session:
        tasks = []
        for prompt in prompts:
            url = 'https://api.openai.com/v1/engines/text-davinci-002/completions'
            tasks.append(asyncio.ensure_future(get_text(session, url, prompt)))
        feedbacks = await asyncio.gather(*tasks)
    return {'response': feedbacks[0], 'query': searchQuery, 'roadmap': feedbacks[1]}


def results(response):
    searchQuery = responses.get('query')
    numResults = 2
    resps = asyncio.run(resultsAsync(searchQuery))
    return render(response, 'result.html', resps)

def about(response):
    return render(response, 'aboutUs.html')

def search(response):
    return render(response, 'index.html')

def query(request):
    if request.method == 'POST':
        if 'query' in request.POST:
            q = str(request.POST['query'])
            responses.headers['query'] = q