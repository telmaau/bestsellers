# NYT bestseller list APIs
# inspired by: https://towardsdatascience.com/collecting-data-from-the-new-york-times-over-any-period-of-time-3e365504004

import os
import json
import time
import requests
import datetime
import dateutil
import pandas as pd
from dateutil.relativedelta import relativedelta


API_KEY = "Your-API-key"

# %%
# helper functions
def send_request(date,listname, base_url):
    '''Sends a request to the NYT Archive API for given date.'''
    #base_url https://api.nytimes.com/svc/books/v3/lists/DATE/LIST
    url = base_url+date +'/'+listname+'.json?api-key=' + API_KEY
    response = requests.get(url).json()
    time.sleep(6)
    return response

def is_valid(article, date):
    '''An article is only worth checking if it is in range, and has a headline.'''
    is_in_range = date > start and date < end
    has_headline = type(article['headline']) == dict and 'main' in article['headline'].keys()
    return is_in_range and has_headline

def DateToString(date):
    newdate=[]
    for d in date:
        if len(d) == 1:
            d = "0"+d
            #print(d)
            newdate.append(d)
        else:
            newdate.append(d)
    datestring= newdate[0]+"-"+newdate[1]+"-"+newdate[2]
    return datestring

def parse_response(response):
    '''Parses and returns response as pandas data frame.'''
    data = {'headline': [],  
        'date': [], 
        'doc_type': [],
        'material_type': [],
        'section': [],
        'keywords': []}
    
    articles = response['response']['docs'] 
    for article in articles: # For each article, make sure it falls within our date range
        date = dateutil.parser.parse(article['pub_date']).date()
        if is_valid(article, date):
            data['date'].append(date)
            data['headline'].append(article['headline']['main']) 
            if 'section' in article:
                data['section'].append(article['section_name'])
            else:
                data['section'].append(None)
            data['doc_type'].append(article['document_type'])
            if 'type_of_material' in article: 
                data['material_type'].append(article['type_of_material'])
            else:
                data['material_type'].append(None)
            keywords = [keyword['value'] for keyword in article['keywords'] if keyword['name'] == 'subject']
            data['keywords'].append(keywords)
    return pd.DataFrame(data) 


def get_data(dates):
    '''Sends and parses request/response to/from NYT Archive API for given dates.'''
    total = 0
    print('Date range: ' + str(dates[0]) + ' to ' + str(dates[-1]))
    if not os.path.exists('headlines'):
        os.mkdir('headlines')
    for date in dates:
        response = send_request(date)
        df = parse_response(response)
        total += len(df)
        df.to_csv('headlines/' + date[0] + '-' + date[1] + '.csv', index=False)
        print('Saving headlines/' + date[0] + '-' + date[1] + '.csv...')
    print('Number of articles collected: ' + str(total))


def get_save_data(dates, listname, base_url='https://api.nytimes.com/svc/books/v3/lists/'):
    '''Sends and parses request/response to/from NYT Archive API for given dates.'''
    total = 0
    print('Date range: ' + str(dates[0]) + ' to ' + str(dates[-1]))
    mydict={}
    if not os.path.exists('books'):
        os.mkdir('books')
    for date in dates:
        d = DateToString(date)
        response = send_request(d,listname, base_url)
        try:
            mydict[d] = response["results"]["books"]
        except:
            print(d,response,"error")
        total += 1
    print('Number of lists collected: ' + str(total))
    return mydict

