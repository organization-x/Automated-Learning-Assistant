from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from bs4 import BeautifulSoup
from distutils.log import error
from pydoc import render_doc
from django.http import HttpResponse
import asyncio
import aiohttp
from dotenv import load_dotenv
import os
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.engines.yahoo import Search as YahooSearch
import nest_asyncio
from urllib.request import urlopen, FancyURLopener
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer

load_dotenv()
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
nest_asyncio.apply()
set_api_key = os.getenv('OPENAI_API_KEY')
responses = HttpResponse()
LANGUAGE = "english"
SENTENCES_COUNT = 10

#Get prompts for GPT-3
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

async def get_top_gpt_links(search_query):

    # returns a task that gets a list of tasks that grab links
    link_tasks = asyncio.run(get_link_handler(search_query, 1))

    # creating a list of tasks that grab the text from the links
    summaries_tasks = []

    # creating a list of links
    links = []


    # for each task that grabbed a list of links
    for task in link_tasks:
        # get the results of that task, which is a list of links
        result = task.result()

        # extend our list of links with the links from that task
        links.extend(result)

        # look through each link and create a task that generates a summary
        for link in result:
            summaries_tasks.append(get_text_summary(link))

    # wait for all the summaries to be generated
    # put each summary into a string with a number, to prompt gpt-3
    #summaries_prompt = ""
    summaries = [summaries_task for summaries_task in summaries_tasks]

    # for i in range(len(summaries_tasks)):
    # i = 0
    # while i < len(summaries_tasks):
    #     result = summaries_tasks[i].result()
    #     if result.strip() != "":
    #         summaries.append(result)
    #         summaries_prompt += str(i + 1) + ") \"" + result[:800] + "\"\n"
    #         i += 1
    #     else:
    #         links.remove(links[i])
    #         summaries_tasks.remove(summaries_tasks[i])

    # # prompt gpt-3 to choose the best 3 summaries
    # summaries_prompt += "Which 3 of these texts best answer the prompt " + search_query + "? Answer with only numerical digits. Example Response: \"1,7,9\" or \"2,3,4\""

    # prompt = {
    #     'prompt': summaries_prompt,
    #     'temperature': 0.7,
    #     'max_tokens': 256,
    #     'top_p': 1,
    #     'frequency_penalty': 0,
    #     'presence_penalty': 0
    # }

    # async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers={'authorization': f"Bearer {set_api_key}"}) as session:
    #     url = 'https://api.openai.com/v1/engines/text-davinci-002/completions'
    #     task = asyncio.ensure_future(get_text(session, url, prompt))
    #     nums = await task

    # # get the response from gpt-3
    # numbers = nums.strip().split(",")

    # # filtering out text just in case GPT-3 returns something weird
    # for num in numbers:
    #     num = "".join(filter(str.isdigit, num))

    # create a list of the links and summaries that gpt-3 chose
    final_links = [links[0], links[1], links[2]]
    final_summaries = [summaries[0], summaries[1], summaries[2]]


    return {'link1': final_links[0], 'link2': final_links[1], 'summary1': final_summaries[0], 'summary2': final_summaries[1]}

# this method handles creating different tasks to grab links from different search engines
# this method should probably be removed in the future, as we are only using the first page of google
async def get_link_handler(prompt, num_pages=1):
    tasks = []
    for i in range(1, num_pages + 1):
        tasks.append(asyncio.create_task(__get_links_from_search_engine(prompt, i)))
    await asyncio.gather(*tasks)

    return tasks

# this method gets links from the search engine - if google fails it defaults to yahoo
async def __get_links_from_search_engine(prompt, page_num):
    retry = 0
    results = None
    while retry < 3:
        try:
            results = GoogleSearch().search(prompt, page=page_num)
            break;
        except Exception as e:
            retry += 1
            if retry == 2:
                prompt = prompt[:-1]
    if results is None:
        retry = 0
        while retry < 3:
            try:
                results = YahooSearch().search(prompt, page=page_num)
                break;
            except Exception as e:
                retry += 1
    if results is None:
        return ""


    final_links = []

    results_links = results['links']
    for link in results_links:
        if link not in final_links and 'youtube' not in link:
            final_links.append(link)
    return final_links
#get all text from urls
def get_url_text(article_url):
    class AppURLopener(FancyURLopener):
        version = "Mozilla/5.0"

    # test code from stack overflow may or may not work
    opener = AppURLopener()
    html = opener.open(article_url)
    soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

        # get text
    text = soup.get_text()
        
        # # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
        # # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def get_text_summary(url):
    # gets the text of the url
    url_text = get_url_text(url)
    # summarizes the text using TF-IDF
    text = str(url_text)
    text = text.replace("\n", ". ")
    text = text.split(". ")
    filtered_text = []
    for i in range(len(text)-25):
        if len(text[i+2]) > 15:
            filtered_text.append(text[i+2])
            for j in list(text[i+2]):
                if j.isalpha() == False and j != " " and j != "." and j != "," and j != "!" and j != "?" and j.isnumeric() == False:
                    filtered_text.pop(-1)
                    break
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
    summary = [one[1], two[1], three[1]]
    return summary

#Asynchronous functions to call OpenAI API and get text from GPT-3
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