import asyncio
import aiohttp
import json
from dotenv import load_dotenv
import os
import time

load_dotenv()
set_api_key = os.getenv('OPENAI_API_KEY')


def getPrompts(searchQuery):
    p1 = f"Explain in informative terms to a non programmer in 300 words. {searchQuery}"
    p2 = f"Give a roadmap that is a series of instructions that someone should take to solve this question. {searchQuery} Include line breaks after each point. "
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
    async with aiohttp.ClientSession(headers={'authorization': f"Bearer {set_api_key}"}) as session:
        tasks = []
        for prompt in prompts:
            url = 'https://api.openai.com/v1/engines/text-davinci-002/completions'
            tasks.append(asyncio.ensure_future(get_text(session, url, prompt)))
        feedbacks = await asyncio.gather(*tasks)
    return feedbacks


from statistics import mean, median, mode, stdev, quantiles

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
searchQuery = "How do you write a class in Java?"

logTime = []

print("------AioHttp Test------")
for n in range(30):
    print(f"{n + 1}th Loop:")
    t2 = time.time()
    resps = asyncio.run(resultsAsync(searchQuery))
    t3 = time.time()
    print(t3 - t2)
    logTime.append(t3 - t2)
    print("\n")
print("------Results------")
quartiles = quantiles(logTime)
print("Mean: ", mean(logTime))
print("Q1: ", quartiles[0])
print("Median (Q2): ", quartiles[1])
print("Q3: ", quartiles[2])
print("Standard Deviation: ", stdev(logTime))