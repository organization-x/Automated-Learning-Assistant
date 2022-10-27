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
from spellchecker import SpellChecker

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
    search_query = responses.get('query')
    if search_query is None or error == "True":
        print(f"\n\nError Here\n\n")
        return redirect('search')
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
            links_summary = loop.create_task(bulk.get_top_gpt_links(search_query, results=numResults))
            loop.run_until_complete(asyncio.gather(GPT_3_Summary, links_summary))

            GPT_3_Summary = GPT_3_Summary.result()
            links_summary, links = links_summary.result()

            # combining the links and the gpt-3 summary
            print(GPT_3_Summary, links)

            #GPT_3_Summary.update(links_summary)


            # Get HTML Code Generated
            # Get HTML Code Generated
            htmlCodes = []
            # for n in range(len(links_summary)):
            for n in range(numResults):
                template = f'<div class="row d-xl-flex justify-content-xl-center" style="margin-right: 0px;margin-left: 0px;">\n' \
                           f'<div class="col-md-12 col-xl-12">\n' \
                           f'<h3 style="text-align: center;">Result No. {n+1}</h3>' \
                           f'<p style="text-align: left;">Summary:<br>{links_summary[n] }</p>\n' \
                           f'<div class="row"><div class="col" style="text-align: center">\n' \
                           f'<button class="btn btn-primary" onclick="window.open(\'{ links[n] }\', \'_blank\')" target="_blank" type="button">' \
                           f'Link</button></div></div>\n</div>\n</div>'
                # if (n + 1) != len(links_summary):
                if (n+1) != numResults:
                    htmlCodes.append(template.replace('{', '{{').replace('}', '}}') + '\n<br>')
                else:
                    htmlCodes.append(template.replace('{', '{{').replace('}', '}}'))
            upload = {'resultsList': '\n'.join(htmlCodes)}
            GPT_3_Summary.update(upload)
            print(f"\n\n{GPT_3_Summary['response']}\n\n")
            resultsdb.query_results[search_query] = [GPT_3_Summary['response'], GPT_3_Summary['one'], GPT_3_Summary['two'], GPT_3_Summary['three'], GPT_3_Summary['four'], GPT_3_Summary['five'], GPT_3_Summary['resultsList']]
                                                                        
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
            error = "False"
            spell = SpellChecker()
            list_q = q.split()
            margin=0
            for i in range(len(list_q)):
                if list_q[i] == spell.correction(list_q[i]):
                    margin+=1
            if margin/len(list_q) < 0.5:
                print(margin/len(list_q))
                error = "True"
                responses.headers['error'] = error
                print(f"\n\nError\n\n")
                return redirect('search')
            else:
                responses.headers['error'] = error
                responses.headers['query'] = q
                print(f"\n\nWorks\n\n")
                return redirect('loading')
