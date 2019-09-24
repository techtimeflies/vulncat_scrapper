import requests
import re
from bs4 import BeautifulSoup
import logging
import os
import json

base_url = "https://vulncat.fortify.com/en/weakness?q="
logpath=f'{os.getcwd()}/logs'

def scrape_url(url):
    soup:BeautifulSoup=None
    try:
        r=requests.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')
    except requests.exceptions.RequestException as ex:
        logging.warning("There was an error with the request")
        logging.error(ex)
    except Exception as ex:
        logging.warning("An unknown exception has occured")
        logging.error(ex)
    finally:
        return soup

def get_categories(html):
    """"""
    soup = BeautifulSoup(html, 'html.parser')

    return soup.find("input", attrs={"data-filtername":"category"})


def parse_categories():
    soup = scrape_url(base_url)

    logfile=f'{logpath}/categories.json'
    open(logfile, 'w').close()
    categories={}

    try:
        for data in soup.find_all("input", attrs={"data-filtername":"category"}):
        #print(data["data-name"].replace("+"," "))

            category = data["data-name"].replace("+"," ")
            logging.info(f"found category '{category}'")
            link = "https://vulncat.fortify.com/en/weakness?category={}".format(data['data-name'])
            #print(f"{category}\nHyper-Link:{link}")
            categories[category]=link

            with open(logfile, 'w+') as f:
                f.write(json.dumps(categories))
    except Exception as ex:
        logging.error(ex)
    finally:
        return
            
def get_issue_detail(url, soup:BeautifulSoup):
    
    links = soup.find_all(class_="external-link")

    for link in links:
        parse_issue_data(f"{url}{link['href']}")

def parse_issue_data(url):
    try:
        soup=scrape_url(url)
        title = soup.find(class_="detail-title")
        print(title.text)
        content = soup.find(class_="tab-content")
        sections = content.find_all(class_="sub-title")

        if sections:
            for s in sections:
                print(s.text + "\n")
                metadata = s.findNext()
                print(metadata.text.replace("[", "\n[").replace(". ", ".\n\n") +"\n\n")

    except Exception as err:
        print("--------ERROR!!! Unable to get explanation of vulnerability")
        print(err)


def navigatePages(soup, base_url):
    if soup is None: return

    get_issue_detail(base_url, soup)

    pagination = soup.find(class_="pagination")

    if pagination is None: 
        print("Unable to find location of page navigation links")
        return

    link = pagination.find("li", class_="active")

    if link and link.text !=">":
        next_link = link.findNext("li")
        if next_link:
            next_url = next_link.find("a")
            target_url = f"{base_url}{next_url['href']}"
            print(target_url +  "\n")
            r = requests.get(url=target_url)
            soup = BeautifulSoup(r.text,"html.parser")
            if soup:
                navigatePages(soup, base_url)
    else:
        print("No more links")
            
