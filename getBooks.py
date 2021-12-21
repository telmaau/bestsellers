# python script for retrieving lists with NYTBooks api

import os
import json
import time
import requests
import datetime
import dateutil
import pandas as pd
from dateutil.relativedelta import relativedelta

from bookapi import *



# all NYTBook lists that are still updated (??)
book_lists =['combined-print-and-e-book-fiction', 'combined-print-and-e-book-nonfiction', 'hardcover-fiction', 'hardcover-nonfiction', 'trade-fiction-paperback', 'paperback-nonfiction', 'advice-how-to-and-miscellaneous', 'childrens-middle-grade-hardcover', 'picture-books', 'series-books', 'young-adult-hardcover', 'audio-fiction', 'audio-nonfiction', 'business-books', 'graphic-books-and-manga', 'mass-market-monthly', 'middle-grade-paperback-monthly', 'young-adult-paperback-monthly']



# set dates
end = datetime.date.today()
start = end - relativedelta(years=5)

# make a list per week (?)
dates_in_range = [x.split(' ') for x in pd.date_range(start, end, freq='W').strftime("%Y %-m %-d").tolist()]

for bl in book_lists:
    
    # set dates per list, since not all of them contain data from an equal time period
    if "audio" in bl:
        # set dates
        end = datetime.date.today()
        start = end - relativedelta(years=4)
        
        # make a list per week
        dates_in_range = [x.split(' ') for x in pd.date_range(start, end, freq='W').strftime("%Y %-m %-d").tolist()]
        bookdict=get_save_data(dates_in_range, bl)
        
    elif "paperback" in bl:
        # set dates
        end = datetime.date.today()
        start = end - relativedelta(years=3)

        dates_in_range = [x.split(' ') for x in pd.date_range(start, end, freq='W').strftime("%Y %-m %-d").tolist()]
        bookdict=get_save_data(dates_in_range, bl)
        
    else:    
        bookdict=get_save_data(dates_in_range, bl)
        print("retrieved list", bl)
    
    # save to json dictionaries
    with open("books/"+bl+".json", "w") as d:
        json.dump(bookdict,d)



if __name__=="__main__":
    main()
