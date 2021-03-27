import urllib.request as libreq
import feedparser
import time
import itertools
import pandas as pd
import json
import os

# Base api query url
base_url = 'http://export.arxiv.org/api/query?'

'''
 Metodo per scaricare dati tramite API
 Parametri usati:
 - base_url: url base dell'API
 - start: punto di inizio per i dati
 - max_result: punto di fine per i dati
 - search_query: parametri di ricerca
'''
def arXiv_query(start, max_result, search_query):
    # Dichiarazione della query
    query = 'search_query=%s&start=%i&max_results=%i' % (search_query,
                                                     start,
                                                     max_result)
    # I metadati di "opensearch" come <totalResults>, <startIndex> e <itemsPerPage>
    # sono attivi nel namespace "opensearch". Alcuni metatadi risiedono nello spazio dei nomi arXiv.
    # Esponiamo entrambi i namespaces.
    feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
    feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

    # Effettiamo una richiesta GET usando base_url + query
    response = libreq.urlopen(base_url+query).read()

    # Parsing del risultato della GET
    feed = feedparser.parse(response)

    # Stampa dei risultati generali
    # print('Feed title: %s' % feed.feed.title)
    # print('Feed last updated: %s' % feed.feed.updated)

    # Stampa dei metadati presenti in opensearch
    # print('totalResults for this query: %s' % feed.feed.opensearch_totalresults)
    # print('itemsPerPage for this query: %s' % feed.feed.opensearch_itemsperpage)
    # print('startIndex for this query: %s'   % feed.feed.opensearch_startindex)
    
    list_dict = []

    # Per ogni entry del risultato della GET salviamo le informazioni (e le stampiamo per debug)
    for entry in feed.entries:
        # ----- TITOLO DELL'ARTICOLO
        title = entry.title
        # print('Title:  %s' % title)
        
        # ----- PRIMO AUTORE
        author_string = entry.author
        # print('Last Author:  %s' % author_string)

        # ----- LISTA DEGLI AUTORI
        try:
            authors =[]
            for author in entry.authors:
                authors.append(author.name)
            # print("Autori :" )
            # print(autori)
        except AttributeError:
            pass
        
        # ----- CATEGORIA PRIMARIA
        primary = entry.tags[0]['term']
        #print('Primary Category: %s' % primary)
        
        # ----- LISTA DELLE CATEGORIE      
        all_categories = [t['term'] for t in entry.tags]
        categories = []
        for category in all_categories:
            categories.append(category)

        # print('All Categories: %s' % (', ').join(all_categories))
        
        # Creiamo il dizionario con i dati
        dictionary = {"Scrapy_key_id": search_query[4:],"Title": title, "Last_Author": author_string, "Authors": authors, "Primary_Category":primary, "Categories":categories}
        
        list_dict.append(dictionary)
    return list_dict

'''
    Creo la lista di chiavi su cui chiamare la query
    - cond-mat: "condensed matter" parola chiave per riferire gli argomenti relativi 
                a solidi e liquidi (superconduttivita', elettroni fortemente correlati, meccanica statistica, gas quantistici)
    - gr-qc: "general relativity and quantum cosmology" 
    - math-ph: "Mathematical physics"
    - quant-ph: "quantum physics"
    
'''
list_key = ["cond-mat", "gr-qc", "math-ph", "quant-ph"]
list_search_query = []
for i in list_key:
    query = "cat:" + i
    list_search_query.append(query)
# Effettuo le query, attendendo 10 secondi tra ogni richiesta per evitare
# di sovraccaricare il sistema con accessi "illeciti"
list_dictionary=[]
for search_query in list_search_query:
    id_dictionary = []
    print("***********************************")
    print("Crawling con key  = " + str(search_query[4:]))
    print("Iterazione: 0 - 1000")
    id_dictionary = id_dictionary + arXiv_query(0, 1000, search_query)
    time.sleep(10)
    print("Iterazione: 1000 - 2000")
    id_dictionary = id_dictionary + arXiv_query(1000, 2000, search_query)
    time.sleep(10)
    print("Iterazione: 2000 - 3000")
    id_dictionary = id_dictionary + arXiv_query(2000, 3000, search_query)
    time.sleep(10)
    print("Iterazione: 3000 - 4000")
    id_dictionary = id_dictionary + arXiv_query(3000, 4000, search_query)
    time.sleep(10)
    print("Iterazione: 4000 - 5000")
    id_dictionary = id_dictionary + arXiv_query(4000, 5000, search_query)
    time.sleep(10)
    list_dictionary.append(id_dictionary)



# Creo la cartella dove inserire i dati
if not os.path.exists('crawled_data'):
    os.makedirs('crawled_data')
# Serializzo la lista dei dialoghi in modo da inserirla nel json
for i in range(0,len(list_search_query)):
    json_object = json.dumps(list_dictionary[i], indent = 4, ensure_ascii=False) 
    with open("crawled_data/crawled_"+ list_search_query[i][4:] + ".json", "w", encoding='utf-8') as outfile: 
        outfile.write(json_object) 