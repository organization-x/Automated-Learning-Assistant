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
import time

load_dotenv()
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
nest_asyncio.apply()
responses = HttpResponse()
LANGUAGE = "english"
SENTENCES_COUNT = 10

def buildTemplate(search_query, numResults, roadmap, tilting, primaryColors, secondaryColors, textColors, links_summary:list, links:list, GPT_3_Summary):
    headingColors = textColors
    # Get HTML Code Generated
    htmlCodes = []
    # Summary
    if tilting == "true":
        htmlCodes.append(
            f'<div class="card d-flex d-sm-flex d-md-flex d-xl-flex justify-content-center align-items-center justify-content-sm-center align-items-sm-center justify-content-md-center align-items-md-center justify-content-xl-center align-items-xl-center" id="Explanation" style="background: transparent; border-width: 0px;border-left-width: 0px;">\n' \
            f'<div class="card-body d-flex d-xxl-flex flex-column align-items-center align-items-sm-center align-items-lg-center justify-content-xxl-center align-items-xxl-center col-xl-5 col-md-12 contentText" id="body_explanation" name="body" style="background: {secondaryColors};border-top-width: 2px;border-top-left-radius: 16px;border-bottom-right-radius: 16px;border-top-right-radius: 16px;border-bottom-left-radius: 16px;margin-bottom: 16px;max-width: 60vw;" data-tilt="data-tilt">\n' \
            f'<h3 class="textHeading" name="title" id="title_explanation" style="text-align: center; color: {headingColors};">{ search_query }</h3>\n' \
            f'<p name="text" id="textExplanation" style="text-align: center; color: {textColors};"> { GPT_3_Summary["response"] } <br></p>\n' \
            f'</div>\n</div>\n'
        )
        # Roadmap
        if roadmap == "true":
            template = f'<div class="card d-flex d-sm-flex d-md-flex d-xl-flex justify-content-center align-items-center justify-content-sm-center align-items-sm-center justify-content-md-center align-items-md-center justify-content-xl-center align-items-xl-center" id="Roadmap" style="background: transparent; border-width: 0px;border-left-width: 0px;">\n' \
                       f'<div class="card-body d-flex d-xxl-flex flex-column align-items-sm-center align-items-lg-center justify-content-xxl-center align-items-xxl-center col-xl-5 col-md-12 contentText" id="body_roadmap" name="body" style="background: {secondaryColors};border-top-width: 2px;border-top-left-radius: 16px;border-bottom-right-radius: 16px;border-top-right-radius: 16px;border-bottom-left-radius: 16px;margin-bottom: 16px;max-width: 60vw;" data-tilt="data-tilt">\n' \
                       f'<h3 name="title" id="title_roadmap" class="textHeading" style="text-align: center; color: {headingColors};">Roadmap</h3>\n' \
                       f'<p name="text" id="textRoadmap" style="text-align: left; color: {textColors};">{ GPT_3_Summary["one"] }<br>{ GPT_3_Summary["two"] }<br>{ GPT_3_Summary["three"] }<br>{ GPT_3_Summary["four"] }<br>{ GPT_3_Summary["five"] }</p>\n' \
                       f'</div>\n</div>\n'
            htmlCodes.append(template)
        # Results + Relevant Links
        for n in range(numResults):
            template = f'<div class="card d-flex d-sm-flex d-md-flex d-xl-flex justify-content-center align-items-center justify-content-sm-center align-items-sm-center justify-content-md-center align-items-md-center justify-content-xl-center align-items-xl-center" style="background: transparent; border-width: 0px;border-left-width: 0px;">\n' \
                       f'<div class="card-body d-flex d-xxl-flex flex-column align-items-sm-center align-items-lg-center justify-content-xxl-center align-items-xxl-center col-xl-5 col-md-12 resultList contentText" id="body_{n}" name="body" style="background: {secondaryColors};border-top-width: 2px;border-top-left-radius: 16px;border-bottom-right-radius: 16px;border-top-right-radius: 16px;border-bottom-left-radius: 16px;margin-bottom: 16px;max-width: 60vw;" data-tilt="data-tilt">\n' \
                       f'<h3 name="title" id="title_{n}" class="textHeading" style="text-align: center; color: {headingColors};">Result No. {n + 1}<br></h3>\n' \
                       f'<p name="text" id="textSummary_{n}" style="text-align: left; color: {textColors};"><br>Summary:<br>{links_summary[n]}<br></p>\n' \
                       f'<a id="button_{n}" name="button" href={links[n]} target="_blank"><button class="btn btn-primary textHeading" onclick="window.open(\'{links[n]}\', \'_blank\')" target="_blank" type="button">Link</button></a>\n' \
                       f'</div>\n</div>'
            # if (n + 1) != len(links_summary):
            if (n + 1) != numResults:
                htmlCodes.append(template + '\n<br>')
            else:
                htmlCodes.append(template)
    else:
        htmlCodes.append(
            f'<div class="card d-flex d-sm-flex d-md-flex d-xl-flex justify-content-center align-items-center justify-content-sm-center align-items-sm-center justify-content-md-center align-items-md-center justify-content-xl-center align-items-xl-center" id="Explanation" style="background: transparent; border-width: 0px;border-left-width: 0px;">\n' \
            f'<div class="card-body d-flex d-xxl-flex flex-column align-items-center align-items-sm-center align-items-lg-center justify-content-xxl-center align-items-xxl-center col-xl-5 col-md-12" id="body_explanation" name="body" style="background: {secondaryColors};border-top-width: 2px;border-top-left-radius: 16px;border-bottom-right-radius: 16px;border-top-right-radius: 16px;border-bottom-left-radius: 16px;margin-bottom: 16px;max-width: 60vw;">\n' \
            f'<h3 name="title" id="title_explanation" style="text-align: center; color: {headingColors};">{ search_query }</h3>\n' \
            f'<p name="text" id="textExplanation" style="text-align: center; color: {textColors};"> { GPT_3_Summary["response"] } <br></p>\n' \
            f'</div>\n</div>\n'
        )
        # Roadmap
        if roadmap == "true":
            template = f'<div class="card d-flex d-sm-flex d-md-flex d-xl-flex justify-content-center align-items-center justify-content-sm-center align-items-sm-center justify-content-md-center align-items-md-center justify-content-xl-center align-items-xl-center" id="Roadmap" style="background: transparent; border-width: 0px;border-left-width: 0px;">\n' \
                       f'<div class="card-body d-flex d-xxl-flex flex-column align-items-sm-center align-items-lg-center justify-content-xxl-center align-items-xxl-center col-xl-5 col-md-12" id="body_roadmap" name="body" style="background: {secondaryColors};border-top-width: 2px;border-top-left-radius: 16px;border-bottom-right-radius: 16px;border-top-right-radius: 16px;border-bottom-left-radius: 16px;margin-bottom: 16px;max-width: 60vw;">\n' \
                       f'<h3 name="title" id="title_roadmap" style="text-align: center; color: {headingColors};">Roadmap</h3>\n' \
                       f'<p name="text" id="textRoadmap" style="text-align: left; color: {textColors};">{ GPT_3_Summary["one"] }<br>{ GPT_3_Summary["two"] }<br>{ GPT_3_Summary["three"] }<br>{ GPT_3_Summary["four"] }<br>{ GPT_3_Summary["five"] }</p>\n' \
                       f'</div>\n</div>\n'
            htmlCodes.append(template)
        # Results + Relevant Links
        for n in range(numResults):
            template = f'<div class="card d-flex d-sm-flex d-md-flex d-xl-flex justify-content-center align-items-center justify-content-sm-center align-items-sm-center justify-content-md-center align-items-md-center justify-content-xl-center align-items-xl-center" style="background: transparent; border-width: 0px;border-left-width: 0px;">\n' \
                       f'<div class="card-body d-flex d-xxl-flex flex-column align-items-sm-center align-items-lg-center justify-content-xxl-center align-items-xxl-center col-xl-5 col-md-12 resultList" id="body_{n}" name="body" style="background: {secondaryColors};border-top-width: 2px;border-top-left-radius: 16px;border-bottom-right-radius: 16px;border-top-right-radius: 16px;border-bottom-left-radius: 16px;margin-bottom: 16px;max-width: 60vw;">\n' \
                       f'<h3 id="title_{n}" name="title" style="text-align: center; color: {headingColors};">Result No. {n + 1}<br></h3>\n' \
                       f'<p name="text" id="textSummary_{n}" style="text-align: left; color: {textColors};"><br>Summary:<br>{links_summary[n]}<br></p>\n' \
                       f'<a id="button_{n}" name="button" href={links[n]} target="_blank"><button class="btn btn-primary" onclick="window.open(\'{links[n]}\', \'_blank\')" target="_blank" type="button">Link</button></a>\n' \
                       f'</div>\n</div>'
            # if (n + 1) != len(links_summary):
            if (n + 1) != numResults:
                htmlCodes.append(template + '\n<br>')
            else:
                htmlCodes.append(template)
    return {'resultsList': '\n'.join([entry.replace('{', '{{').replace('}', '}}') for entry in htmlCodes]), 'numResults': numResults}

#Results page
def results(response):
    error = responses.get('error')
    search_query = responses.get('query')
    if search_query is None or error == "True":
        return redirect('search')
    else:
        search_query = responses.get('query')
        numResults = int(responses.get('numResults'))
        roadmap = responses.get('roadmap')
        tilting = responses.get('tilting')
        # Get colors
        primaryColors = responses.get('primaryColors')
        secondaryColors = responses.get('secondaryColors')
        textColors = responses.get('textColors')
        print(f"primaryColors: {primaryColors}, secondaryColors: {secondaryColors}, textColors: {textColors}")
        # checking if the results are cached and that at least the first link is valid and not an error
        try:
            start_time = time.time()
            if search_query in resultsdb.query_results and numResults <= resultsdb.query_results[search_query]['numResults']:
                results = resultsdb.query_results[search_query]
                if results['numResults'] > numResults:
                    results['resultsList'] = buildTemplate(search_query, numResults, roadmap, tilting, primaryColors, secondaryColors, textColors, results['links_summary'], results['links'], results)
                return render(response, 'result.html', results)
            else:
                loop = asyncio.new_event_loop()
                GPT_3_Summary = loop.create_task(bulk.results_async(search_query))
                links_summary = loop.create_task(bulk.get_summaries_and_links(search_query, num_results=numResults))
                loop.run_until_complete(asyncio.gather(GPT_3_Summary, links_summary))

                GPT_3_Summary = GPT_3_Summary.result()
                links, links_summary, numResults = links_summary.result()

                # Get HTML Code Generated
                GPT_3_Summary.update(buildTemplate(search_query, numResults, roadmap, tilting, primaryColors, secondaryColors, textColors, links_summary, links, GPT_3_Summary))

                GPT_3_Summary['links_summary'] = links_summary
                GPT_3_Summary['links'] = links
                resultsdb.query_results[search_query] = GPT_3_Summary
                                
                print(f"Time taken: {time.time() - start_time}")

                return render(response, 'result.html', GPT_3_Summary)

        except Exception as e:
            print(e)
            loop = asyncio.new_event_loop()
            GPT_3_Summary = loop.create_task(bulk.results_async(search_query))
            links_summary = loop.create_task(bulk.get_summaries_and_links(search_query, num_results=numResults))
            loop.run_until_complete(asyncio.gather(GPT_3_Summary, links_summary))

            GPT_3_Summary = GPT_3_Summary.result()
            links, links_summary, numResults = links_summary.result()

            GPT_3_Summary.update(
                buildTemplate(search_query, numResults, roadmap, tilting, primaryColors, secondaryColors, textColors, links_summary, links, GPT_3_Summary))

            resultsdb.query_results[search_query] = [GPT_3_Summary['response'], GPT_3_Summary['resultsList']]

            return render(response, 'result.html', GPT_3_Summary)

#About us page
def about(response):
    return render(response, 'loading.html')

#Search page
def search(response):
    return render(response, 'index.html')

#Loading page
def loading(response):
    return render(response, 'loading.html')

#Query view to get query from search page (PLEASE ADVISE IF BETTER WAY)
def query(request):
    print(f"Start of query: {time.time()}")
    error = False
    if request.method == 'POST':
        if 'numResults' in request.POST:
            numResults = request.POST['numResults']
            responses.headers['numResults'] = numResults
        if 'roadmap' in request.POST:
            roadmap = request.POST['roadmap']
            responses.headers['roadmap'] = roadmap
        if 'tilting' in request.POST:
            tilting = request.POST['tilting']
            responses.headers['tilting'] = tilting
        if 'primaryColors' in request.POST:
            primaryColors = request.POST['primaryColors']
            responses.headers['primaryColors'] = primaryColors
        if 'secondaryColors' in request.POST:
            secondaryColors = request.POST['secondaryColors']
            responses.headers['secondaryColors'] = secondaryColors
        if 'textColors' in request.POST:
            textColors = request.POST['textColors']
            responses.headers['textColors'] = textColors
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
                # print(margin/len(list_q))
                error = "True"
                responses.headers['error'] = error
                print(f"\n\nError\n\n")
                return redirect('search')
            else:
                responses.headers['error'] = error
                responses.headers['query'] = q
                print(f"End of query: {time.time()}")
                return redirect('loading')
