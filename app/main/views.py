# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from distutils.log import error
from pydoc import render_doc
from django.shortcuts import render, redirect
from django.http import HttpResponse
import asyncio
import aiohttp
from dotenv import load_dotenv
import os
import nest_asyncio
from nltk.corpus import words

from . import resultsdb
from . import bulk

load_dotenv()
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
nest_asyncio.apply()
responses = HttpResponse()
LANGUAGE = "english"
SENTENCES_COUNT = 10

#Results page
def results(response):
    error = responses.get('error')
    if error == "True":
        return render(response, 'error.html')
    else:
        search_query = responses.get('query')
        numResults = 2

        # checking if the results are cached and that at least the first link is valid and not an error
        if search_query in resultsdb.query_results and resultsdb.query_results[search_query][6] != "":
            results = resultsdb.query_results[search_query]
            return render(response, 'result.html', {'response': results[0], 'query': search_query, 'one': results[1], 'two': results[2], 'three': results[3], 'four': results[4], 'five': results[5], "link1": results[6], "link2": results[7], "summary1": results[8], "summary2": results[9]})
        else:

            loop = asyncio.new_event_loop()
            GPT_3_Summary = loop.create_task(bulk.results_async(search_query))
            links_summary = loop.create_task(bulk.get_top_gpt_links(search_query))
            loop.run_until_complete(asyncio.gather(GPT_3_Summary, links_summary))

            GPT_3_Summary = GPT_3_Summary.result()
            links_summary = links_summary.result()

            # combining the links and the gpt-3 summary
            GPT_3_Summary.update(links_summary)
 
            resultsdb.query_results[search_query] = [GPT_3_Summary['response'], GPT_3_Summary['one'], GPT_3_Summary['two'], GPT_3_Summary['three'], GPT_3_Summary['four'], GPT_3_Summary['five'], GPT_3_Summary['link1'], GPT_3_Summary['link2'], GPT_3_Summary['summary1'], GPT_3_Summary['summary2']]
                                                                        
            return render(response, 'result.html', GPT_3_Summary)

#About us page
def about(response):
    #return render(response, 'aboutUs.html')
    return render(response, 'loading.html')

#Search page
def search(response):
    return render(response, 'index.html')

#Loading page
def loading(response):
    return render(response, 'loading.html')

#Query view to get query from search page (PLEASE ADVISE IF BETTER WAY)
def query(request):
    error = False
    if request.method == 'POST':
        if 'query' in request.POST:
            q = str(request.POST['query'])
            error = False
            if "?" in q:
                responses.headers['query'] = q
            else:
                error = True
            responses.headers['error'] = error
        return redirect('results')
