# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 14:41:53 2020

@author: boost
"""
import requests
from os import path

def lastpage_determiner(page0):
    page = 'https://www1.president.go.kr/articles/{}'.format(page0)
    response = requests.get(page)
    #if in case the file is contaminated, and higher than page accessible.
    if response.status_code != 200 and page0 > 8800:
        try:
            page0 = str(int(page0)+1)
            page = 'https://www1.president.go.kr/articles/{}'.format(int(page0))
            response = requests.get(page)
            if response.status_code != 200:
                raise Exception('Nope')
        except:
            while response.status_code != 200:
                try:
                    page0 = str(int(page0)-1)
                    page = 'https://www1.president.go.kr/articles/{}'.format(page0)
                    response = requests.get(page)
                    if response.status_code == 200:
                        raise Exception('Nope')
                except:
                    return page0
        
    #if the page number is not the latest
    while response.status_code == 200:
        try:
            page0 = str(int(page0)+1)
            page = 'https://www1.president.go.kr/articles/{}'.format(page0)
            response = requests.get(page)
            if response.status_code != 200:
                page1 = str(int(page0) + 1)
                page = 'https://www1.president.go.kr/articles/{}'.format(page1)
                response = requests.get(page)
                if response.status_code != 200:
                    raise Exception('Nope')
        except:
            page0 = str(int(page0) - 1)
            break
    
    return page0

def file_finder(title):
    filename = '{}.csv'.format(title)
    if path.exists(filename):
        return True
    else:
        return False

    

            
            
            