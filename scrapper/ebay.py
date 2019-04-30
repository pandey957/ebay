#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings('ignore')
import datetime
import urllib3, os, sys, re, pandas as pd, numpy as np, time
from bs4 import BeautifulSoup

request_lag = 0
header = {}

http = urllib3.PoolManager()


sys.path.append('/home/sapandey/ebay')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ebay.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from etailer.models import Ebay


# In[2]:


field_req = {'Ort:': 'address',
 'Erstellungsdatum:': 'posting_dt',
 'Anzeigennummer:': 'reference',
 'Zimmer:': 'room',
 'Anzahl Schlafzimmer:': 'no_of_bedroom',
 'Anzahl Badezimmer:': 'no_of_bathrooms',
 'Wohnfläche (m²):': 'living_area',
 'Grundstücksfläche (m²):': 'land_area',
 'Verfügbar ab Monat:': 'available_from_month',
 'Verfügbar ab Jahr:': 'available_from_year',
 'Haustyp:': 'Haustyp',
 'Heizungsart:': 'heating',
 'Baujahr:': 'construction_year',
 'Provision:': 'Provision',
 'Ausstattung:': 'features',
 'Haustyp:': 'house_type',  
 'header': 'header',
 'user_url': 'user_url',
 'description': 'description', 
 'Nebenkosten (€):': 'additional_cost',
 'Kaution (€):': 'deposit',
             'original_price': 'original_price', 
             'title': 'title', 
             'user': 'user', 
             'phone': 'phone',
             'user_type': 'user_type',
             'active_since': 'active_since'
             
            }


# In[3]:


url = 'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/seite:2/c208+haus_kaufen.haustyp_s:mehrfamilienhaus'


# In[4]:


def get_http_lxml(url):
    time.sleep(request_lag)
    page = http.request('GET', url, headers = header)
    return BeautifulSoup(page.data, 'lxml')

def get_page_detail(url):
    
    page_data = get_http_lxml(url) # Change this line
    if page_data.find('dl', 'attributelist-striped') is None: 
        return {}
    dt_all = page_data.find('dl', 'attributelist-striped').findAll('dt', recursive=False)
    dd_all = page_data.find('dl', 'attributelist-striped').findAll('dd', recursive=False)

    item_dict = {}
    for index in range(len(dt_all)):    
        item_dict[dt_all[index].text.strip()] = dd_all[index].text.strip().replace('\n', '').replace('  ', '')
    art_header = page_data.find('div', 'articleheader')
    item_dict['original_price'] = art_header.find('h2', {'id': 'viewad-price'}).text
    item_dict['title']= art_header.find('h1', {'itemprop': 'name'}).text
    item_dict['user_url'] = page_data.find('div', {'id': 'viewad-profile-box'}).find('a')['href']
    
    
    contact = page_data.find('div', {'id': 'viewad-contact'})    
    contact1 = contact.find('span', 'iconlist-text')
    item_dict['user']= contact.find('span', 'text-bold').text
    item_dict['phone'] = contact.find('span', {'id': 'viewad-contact-phone'}).text if contact.find('span', {'id': 'viewad-contact-phone'}) else ''
    light_text = contact.findAll('span', 'text-light')[-1]
    item_dict['user_type'], item_dict['active_since'] = light_text.text.strip().split('\n')
    
    
    

    description = page_data.find('p', {'id': 'viewad-description-text'})
    for br in description.find_all("br"):
        br.replace_with('\n')
    item_dict['description'] = description.text.strip()
    return item_dict

def get_product_detail( url):
 item_dict = get_page_detail(url) 
 return pd.Series([item_dict.get(_) for _ in field_req], )
    
    
import math
def get_record_dict(df):
    record_dict = df.to_dict('records')
    for record in record_dict:
        record.update((key, None) for key, value in record.items() if (type(value) == float) and (math.isnan(value)) )
    return record_dict

from django.db import transaction
@transaction.atomic
def insert_into_ebay(df):            

    Ebay.objects.bulk_create(
        Ebay(**vals) for vals in get_record_dict(df[outcols])
    ) 


# In[ ]:





# In[5]:


# page_data = get_http_lxml(url)
# df = pd.DataFrame( [ ['https://www.ebay-kleinanzeigen.de'+_['href'], _.text] for _ in page_data.findAll('a', 'ellipsis')], columns = ['detail_url', 'detail'])
# next_page = page_data.find('a', 'pagination-next')
# if next_page:
#     url = 'https://www.ebay-kleinanzeigen.de' + next_page['href']


# In[6]:


outcols = ['title', 'user_id', 'zip_code', 'reference', 'room', 'no_of_bedroom', 'no_of_bathrooms', 'living_area', 
          'land_area', 'heating', 'construction_year', 'price_negotiable', 'detail_url', 'address', 'posting_dt', 
          'commision', 'price', 'features', 'description', 'available_from_year', 'available_from_month', 'create_dt', 
          'update_dt', 'house_type', 'additional_cost', 'deposit', 'user_url', 'user', 'active_since', 'user_type', 'phone']


# In[ ]:





# In[ ]:





# In[ ]:





# In[7]:


def run_single_page(url):
#     url = F'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/seite:{page_number}/c208+haus_kaufen.haustyp_s:mehrfamilienhaus'
    print (F'Running process for URL: {url}')
    page_data = get_http_lxml(url)
    
    next_page = page_data.find('a', 'pagination-next')
    df = pd.DataFrame( [ ['https://www.ebay-kleinanzeigen.de'+_['href'], _.text] for _ in page_data.findAll('a', 'ellipsis')], columns = ['detail_url', 'detail'])
    

    df_existing = pd.DataFrame.from_records(Ebay.objects.all().values('detail_url'))
    if df_existing.shape[0] > 0: 
        df_new = df.loc[~df.detail_url.isin(df_existing.detail_url)]
    else: df_new = df[:]
    if df_new.shape[0] == 0:
        if next_page: 
            run_single_page('https://www.ebay-kleinanzeigen.de' + next_page['href'])
            return None
        else: return None

    outfile = '/home/sapandey/ebay/data/df_ebay_data_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.txt'
    df.to_csv(outfile, index=False, sep='\t')

    df_detail = df_new.detail_url.apply(get_product_detail)
    df_detail.columns = list(field_req.values())
    df_new.reset_index(inplace=True, drop=True)
    df_detail.reset_index(inplace=True, drop=True)

    df_new = pd.concat([df_new, df_detail], axis = 1)
    df_new['user_id'] = df_new.user_url.str.extract('=(\d+)')
    df_new['price'] = df_new.original_price.str.extract('Preis:\s?([\d\.,]+)')
    df_new['zip_code'] = df_new.address.str.extract('(\d{5})')
    df_new['price_negotiable'] = df_new.original_price.str.lower().str.contains('vb').replace({True: 'Yes', False: 'No'})
    df_new.posting_dt = pd.to_datetime(df_new.posting_dt)
    df_new.price = df_new.price.str.replace('.', '').str.replace(',', '.')
    df_new.room = df_new.room.str.replace('.', '').str.replace(',','.')
    df_new.no_of_bedroom = df_new.no_of_bedroom.str.replace('.', '').str.replace(',','.')
    df_new.no_of_bathrooms = df_new.no_of_bathrooms.str.replace('.', '').str.replace(',','.')
    df_new.land_area = df_new.land_area.str.replace('.', '').str.replace(',', '.')
    df_new.living_area = df_new.living_area.str.replace('.', '').str.replace(',', '.')
    df_new.user_url = 'https://www.ebay-kleinanzeigen.de' + df_new.user_url
    df_new.loc[df_new.description.str.len() > 11000, 'description'] = None
    df_new.user = df_new.user.str.strip()
    df_new.active_since = pd.to_datetime(df_new.active_since.str.strip().str.replace('Aktiv seit', ''))
    df_new = df_new.loc[~df_new.reference.isnull()]
    outfile = '/home/sapandey/ebay/data/df_detail_ebay_data_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.txt'
    df_new.to_csv(outfile, index=False, sep='\t')

    df_new['commision'] = None

    curr_time = datetime.datetime.now().strftime('%Y-%m-%d')
    df_new['update_dt'] = curr_time
    df_new['create_dt'] = curr_time    
#     return page_data
    insert_into_ebay(df_new[outcols])
    
    next_page = page_data.find('a', 'pagination-next')
    if next_page: run_single_page('https://www.ebay-kleinanzeigen.de' + next_page['href'])


# In[ ]:





# In[8]:


urls = [
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/c208+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:elektroheizung', 
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/c208+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:etagenheizung', 
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/c208+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:fernwaerme',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/c208+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:fussbodenheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/c208+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:gasheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/c208+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:oelheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/c208+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:ofenheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/c208+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:andere',    
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/baden-wuerttemberg/c208l7970+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/bayern/c208l5510+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/berlin/c208l3331+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/brandenburg/c208l7711+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/bremen/c208l1+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/hessen/c208l4279+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/hamburg/c208l9409+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/mecklenburg-vorpommern/c208l61+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/niedersachsen/c208l2428+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/nordrhein-westfalen/c208l928+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/rheinland-pfalz/c208l4938+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/saarland/c208l285+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/sachsen/c208l3799+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/sachsen-anhalt/c208l2165+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/schleswig-holstein/c208l408+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
    'https://www.ebay-kleinanzeigen.de/s-haus-kaufen/mehrfamilienhaus/thueringen/c208l3548+haus_kaufen.haustyp_s:mehrfamilienhaus+haus_kaufen.heizungsart_s:zentralheizung',
]


# In[9]:


for url in urls: run_single_page(url)


# In[ ]:





# In[ ]:




