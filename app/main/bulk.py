from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import asyncio
import os
from distutils.log import error
from pydoc import render_doc
from urllib.request import FancyURLopener, urlopen
import aiohttp
import nest_asyncio
from bs4 import BeautifulSoup
from cleantext import clean
from django.http import HttpResponse
from dotenv import load_dotenv
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.engines.yahoo import Search as YahooSearch
from sklearn.feature_extraction.text import TfidfVectorizer
from spellchecker import SpellChecker

# initializes pyenchant object
load_dotenv()
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
nest_asyncio.apply()
set_api_key = os.getenv('OPENAI_API_KEY')
responses = HttpResponse()
LANGUAGE = "english"
SENTENCES_COUNT = 10

# Get prompts for GPT-3


def get_prompts(searchQuery):

    p1 = f"Explain in informative terms to a non programmer in 300 words. {searchQuery}"
    p2 = f"Give a roadmap that is a series of 5 steps that someone should take to solve this question. {searchQuery} The steps should be numbered as such: 1. First step, 2. Second step, 3. Third step, 4. Fourth step, 5. Fifth step."
    prompts = []
    explanation = {
        'prompt': p1,
        'temperature': 0.7,
        'max_tokens': 300,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }
    roadmap = {
        'prompt': p2,
        'temperature': 0.7,
        'max_tokens': 200,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }
    prompts.append(explanation)
    prompts.append(roadmap)
    return prompts


async def get_top_gpt_links(search_query, results):

    # returns a task that gets a list of tasks that grab links
    links = await __get_links_from_search_engine(search_query)

    # a check if links failed to be retrieved
    if links == "":
        return {'link1': "",
                'link2': "",
                'summary1': "ERROR: SUMMARY COULD NOT BE GENERATED",
                'summary2': "ERROR: SUMMARY COULD NOT BE GENERATED"}


    # print("Length of links: " + str(len(links)))

    # creating a list of tasks that grab the text from the links
    summaries_task = []

    # getting summary for links
    for link in links:

        summaries_task.append(asyncio.create_task(get_text_summary(link)))

    final_summaries = []
    final_links = []



    # done, pending = await asyncio.wait(asyncio.gather(*summaries_task), timeout=5)
    # print(done)

    # print(len(summaries_task))
    for num, task in enumerate(summaries_task):
        await task
        if task.done():
            if not(task.result() == ""):
                final_summaries.append(task.result())
                final_links.append(links[num])

            summaries_task.remove(task)

        if len(final_summaries) == results:
            break

        # print(final_summaries)
        # await asyncio.sleep(5)

    # print(len(final_summaries))
    # print(len(final_links))
    # print(results)
    # print(len(links))

    results = len(final_summaries)

    return final_links, final_summaries, results

#     if results == 1:
#         return f
#         {'link1': final_links[0]}, {'summary1': final_summaries[0]}
#     elif results == 2:
#         return {'link1': final_links[0],
#                 'link2': final_links[1]},
#                 {'summary1': final_summaries[0],
#                 'summary2': final_summaries[1]}
#     elif results == 3:
#         return {'link1': final_links[0],
#                 'link2': final_links[1],
#                 'link3': final_links[2]},{'summary1': final_summaries[0],
# 'summary2': final_summaries[1],
# 'summary3': final_summaries[2]}
#     return {'link1': final_links[0],
#             'link2': final_links[1],
#             'link3': final_links[2],
#             'link4': final_links[3]},
#             {'summary1': final_summaries[0],
#             'summary2': final_summaries[1],
#             'summary3': final_summaries[2],
#             'summary4': final_summaries[3]}

    # # create a list of the links and summaries
    # final_links = [links[0], links[1], links[2]]
    # final_summaries = [new_summaries[0], new_summaries[1], new_summaries[2]]

    # return {'link1': final_links[0], 'link2': final_links[1], 'summary1': final_summaries[0], 'summary2': final_summaries[1]}

# this method gets links from the search engine - if google fails it defaults to yahoo


async def __get_links_from_search_engine(prompt, page_num=1):
    retry = 0
    results = None

    # try to get links from google
    while retry < 3:
        try:
            results = GoogleSearch().search(prompt, page=page_num)
            break
        except Exception as e:
            retry += 1
            if retry == 2:
                # removing the last character from the prompt and trying again
                # sometimes end punctuation causes google to break
                prompt = prompt[:-1]

    # if google fails, try yahoo
    if results is None:
        retry = 0
        while retry < 3:
            try:
                results = YahooSearch().search(prompt, page=page_num)
                break
            except Exception as e:
                retry += 1

    # if both google and yahoo fail, return an empty list
    if results is None:
        return ""

    final_links = []
    results_links = results['links']

    for link in results_links:

        # ALL LINK FILTRATION SHOULD BE ADDED HERE
        if link not in final_links and 'youtube' not in link and not(link.endswith('.pdf')) and 'khanacademy' not in link and 'blog' not in link:
            final_links.append(link)

    return final_links
# get all text from urls
import urllib.request
user_agent = 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'
def get_url_text(url):

    try:

        request = urllib.request.Request(url)
        request.add_header('User-Agent', user_agent)
        html = urlopen(request, timeout=5).read()
    except:
        print("Error opening url:" + url)
        return ""

    # print("URL: " + url + " was opened successfully")
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    cleaned_text = clean(text=text,
                         fix_unicode=True,
                         to_ascii=True,
                         lower=False,
                         no_line_breaks=False,
                         no_urls=False,
                         no_emails=False,
                         no_phone_numbers=False,
                         no_numbers=False,
                         no_digits=False,
                         no_currency_symbols=False,
                         no_punct=False,
                         replace_with_punct="",
                         lang="en"
                         )
    cleaned_text = cleaned_text.split("\n")

    for i in range(len(cleaned_text)):
        if len(cleaned_text[i]) < 20:
            cleaned_text[i] = ""

    cleaned_text = list(filter(None, cleaned_text))
    cleaned_text = "\n".join(cleaned_text)

    return cleaned_text


async def get_text_summary(url):
    # gets the text of the url
    url_text = get_url_text(url)
    if url_text == "":
        return ""

    # summarizes the text using TF-IDF
    text = str(url_text)
    text = text.replace("\n", ". ")
    text = text.split(".")
    filtered_text = []
    spell = SpellChecker()
    for i in range(len(text)-20):
        words = text[i].split()
        for word in words:
            if word == spell.correction(word):
                    filtered_text.append(text[i])
                    break
        # for j in list(text[i]):
        #     if j.isalpha() == False and j != " " and j != "." and j != "," and j != "!" and j != "?" and j.isnumeric() == False:
        #         filtered_text.pop(-1)
        #         break

    tf_idf_model = TfidfVectorizer(stop_words='english')
    processed_text_tf = tf_idf_model.fit_transform(filtered_text)
    scores = processed_text_tf.toarray()
    one = [0, ""]
    two = [0, ""]
    three = [0, ""]
    for i in range(len(scores)):
        avg = sum(scores[i]) / len(scores[i])
        if avg > three[0]:
            if avg > two[0]:
                if avg > one[0]:
                    one = [avg, filtered_text[i]]
                else:
                    two = [avg, filtered_text[i]]
            else:
                three = [avg, filtered_text[i]]
    summary = one[1] + ". " + two[1] + ". " + three[1] + "."

    return summary

# Asynchronous functions to call OpenAI API and get text from GPT-3


async def get_text(session, url, params):
    async with session.post(url, json=params) as resp:
        text = await resp.json()
        return text['choices'][0]['text']


async def results_async(searchQuery):
    prompts = get_prompts(searchQuery)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers={'authorization': f"Bearer {set_api_key}"}) as session:
        tasks = []
        for prompt in prompts:
            url = 'https://api.openai.com/v1/engines/text-davinci-002/completions'
            tasks.append(asyncio.ensure_future(get_text(session, url, prompt)))
        feedbacks = await asyncio.gather(*tasks)
    step_one = feedbacks[1].split('\n')[2]
    step_two = feedbacks[1].split('\n')[3]
    step_three = feedbacks[1].split('\n')[4]
    step_four = feedbacks[1].split('\n')[5]
    step_five = feedbacks[1].split('\n')[6]

    return {'response': feedbacks[0], 'query': searchQuery, 'roadmap': feedbacks[1], 'one': step_one, 'two': step_two, 'three': step_three, 'four': step_four, 'five': step_five}
