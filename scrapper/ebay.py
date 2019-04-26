#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings('ignore')

import urllib3, os, sys, re, pandas as pd, numpy as np, time
from bs4 import BeautifulSoup

request_lag = 4
header = {}

http = urllib3.PoolManager()


# In[2]:


field_req = {'Ort:': 'address',
 'Erstellungsdatum:': 'posting_dt',
 'Anzeigennummer:': 'reference',
 'Zimmer:': 'room',
 'Anzahl Schlafzimmer:': 'Anzahl Schlafzimmer',
 'Anzahl Badezimmer:': 'Anzahl Badezimmer',
 'Wohnfläche (m²):': 'Wohnfläche (m²)',
 'Grundstücksfläche (m²):': 'Grundstücksfläche (m²)',
 'Verfügbar ab Monat:': 'Verfügbar ab Monat',
 'Verfügbar ab Jahr:': 'Verfügbar ab Jahr',
 'Haustyp:': 'Haustyp',
 'Heizungsart:': 'Heizungsart',
 'Baujahr:': 'Baujahr',
 'Provision:': 'Provision',
 'Ausstattung:': 'Ausstattung',
 'original_price': 'original_price',
 'header': 'header',
 'user_url': 'user_url',
 'description': 'description'}


# In[3]:


url = 'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/sortierung:preis/c208+haus_kaufen.haustyp_s:mehrfamilienhaus'


# In[4]:


def get_http_lxml(url):
    time.sleep(request_lag)
    page = http.request('GET', url, headers = header)
    return BeautifulSoup(page.data, 'lxml')    


# In[5]:


page_data = get_http_lxml(url)
df = pd.DataFrame( [ ['https://www.ebay-kleinanzeigen.de'+_['href'], _.text] for _ in page_data.findAll('a', 'ellipsis')], columns = ['detail_url', 'detail'])
next_page = page_data.find('a', 'pagination-next')
if next_page:
    url = 'https://www.ebay-kleinanzeigen.de' + next_page['href']


# In[6]:


def get_page_detail(url):
    page_data = get_http_lxml(url) # Change this line
    dt_all = page_data.find('dl', 'attributelist-striped').findAll('dt', recursive=False)
    dd_all = page_data.find('dl', 'attributelist-striped').findAll('dd', recursive=False)

    item_dict = {}
    for index in range(len(dt_all)):    
        item_dict[dt_all[index].text.strip()] = dd_all[index].text.strip().replace('\n', '').replace('  ', '')
    art_header = page_data.find('div', 'articleheader')
    item_dict['original_price'] = art_header.find('h2', {'id': 'viewad-price'}).text
    item_dict['title']= art_header.find('h1', {'itemprop': 'name'}).text
    item_dict['user_url'] = page_data.find('div', {'id': 'viewad-profile-box'}).find('a')['href']

    description = page_data.find('p', {'id': 'viewad-description-text'})
    for br in description.find_all("br"):
        br.replace_with('\n')
    item_dict['description'] = description.text.strip()
    return item_dict


def get_product_detail( url):
    item_dict = get_page_detail(url) 
    return pd.Series([item_dict.get(_) for _ in field_req])

df_new = df[:5]


df_detail = df_new.detail_url.apply(get_product_detail)
df_detail.columns = list(field_req.values())
df_new.reset_index(inplace=True, drop=True)
df_detail.reset_index(inplace=True, drop=True)

df_new = pd.concat([df_new, df_detail], axis = 1)
df_new['user_id'] = df_new.user_url.str.extract('=(\d+)')
del df_new['user_url']
df_new['price'] = df_new.original_price.str.extract('Preis:\s?([\d\.,]+)')
df_new.rename(columns = {'price_formatted': 'price'}, inplace=True)
df_new['zip_code'] = df_new.Ort.str.extract('(\d{5})')
df_new['negotiable'] = df_new.original_price.str.lower().str.contains('vb').replace({True: 'Yes', False: 'No'})


