import logging
import json
import time
import os
import re
import pandas as pd
import string
import requests
import datetime
#from pprint import pprint
#from itertools import count
from urlparse import urljoin
from bs4 import BeautifulSoup
import urllib
from lxml import html
from thready import threaded
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from scrapekit.util import collapse_whitespace
from dateutil import parser


from connectedafrica.scrapers.util import MultiCSV
from connectedafrica.scrapers.util import make_path

URL_ROOT = 'http://www.ghanayello.com'
URL_PATTERN = 'http://www.ghanayello.com/companies/NGO/%s'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}



def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
    

def ngo_urls():
    next_page = True
    i = 1
    company_urls = []
    while next_page:
        url = URL_PATTERN % i
        res = requests_retry_session().get(url, headers=HEADERS)
        page = {
            'url': url,
            'http_status': res.status_code,
            'content': res.content
        }
        soup = BeautifulSoup(page['content'])
        urls = [URL_ROOT + a["href"] for a in soup.select("div h4 a")]
        company_urls += urls
        i += 1
        if '404 error: Page not found' in page['content']:
            next_page = False
    return company_urls


def make_urls():
    # urls = ngo_urls()
    urls = ['http://www.ghanayello.com/company/49232/Watered_Kindness_Foundation', 'http://www.ghanayello.com/company/45140/Agency_for_Health_and_Food_Security', 'http://www.ghanayello.com/company/7463/JPCann_Associates_Ltd']
    for url in urls:
        time.sleep(45)
        yield url


def scrape_ngo(csv, url):
    res = requests_retry_session().get(url, headers=HEADERS)
    print("########   %s  ######" % url)
    page = {
        'url': url,
        'http_status': res.status_code,
        'content': res.content
    }
    if 'internal server error' in page['content'] or 'Either BOF or EOF is True, or the current record has been deleted' in page['content'] or page['http_status'] != 200:
        return
    data = {}
    soup = BeautifulSoup(page['content'], "html.parser")
    company_details = soup.select("div .company_details")[0]
    company_item_center = soup.select("div .company_item_center")[0]
    company_name = company_details.select("#company_name")[0].get_text().strip()
    address, phone, fax, website, year_stablishment, nbr_employees, company_manager, email_url, description, categories_txt, tags_txt, company_type, categories, tags = "", "", "","", "", "", "", "", "", "", "", "", [], []
    try:
        address = company_details.select(".location")[0].get_text().strip()
        phone = company_details.find_all("div", class_="info")[2].find("div", class_="text").get_text()
        fax = company_details.find_all("div", class_="info")[3].find("div", class_="text").get_text()
        website = company_details.find_all("div", class_="info")[4].a["href"]
        year_stablishment = company_details.find_all("div", class_="info")[5].get_text().replace('Establishment year ', '')
        nbr_employees = company_details.find_all("div", class_="info")[6].get_text().replace('Employees ', '')
        company_manager = company_details.find_all("div", class_="info")[7].get_text().replace('Company manager ', '')
        email_url = URL_ROOT + company_details.find_all("div", class_="info")[8].a["href"]
        
        description = company_item_center.select("div .description")[0].get_text().strip()
        categories = [a.get_text() for a in  company_item_center.select("div .categories")[0].find_all("a")]
        categories_txt = ",".join(categories)
        tags = [a.get_text() for a in  company_item_center.select("div .tags")[0].find_all("a")]
        tags_txt = ",".join(tags)
        company_type = "NGO"
    except:
        pass

    data = {
        'data_source': url,
        'company_name': company_name,
        'address': address,
        'phone': phone,
        'fax': fax,
        'website': website,
        'year_stablishment': year_stablishment,
        'nbr_employees': nbr_employees,
        'company_manager': company_manager,
        'email_url': email_url,
        'description': description,
        'categories': categories_txt,
        'tags': tags_txt,
        'company_type': company_type,
        'scraped_time': str(datetime.datetime.now())
    }
    
    csv.write('ngos/ghanayello_ngos.csv', data)


def scrape_ngos():
    csv = MultiCSV()
    threaded(make_urls(), lambda url: scrape_ngo(csv, url), num_threads=3)
    csv.close()

def cd():
    for d in divs:
        try:
            print(d["class"])
        except:
            pass



if __name__ == '__main__':
    scrape_ngos()



