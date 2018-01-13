import requests
import re
from bs4 import BeautifulSoup

def get_categories(html):
    """"""
    soup = BeautifulSoup(html, 'html.parser')

    return soup.find("input", attrs={"data-filtername":"category"})


def parse_categories(soup):
    index=0
    for data in soup.find_all("input", attrs={"data-filtername":"category"}):
    #print(data["data-name"].replace("+"," "))

        category = data["data-name"].replace("+"," ")
        link = "https://vulncat.fortify.com/en/weakness?category={}".format(data['data-name'])
        print(f"{category}\nHyper-Link:{link}")
        if index<=10:
            get_issue_detail(link)
        else:
            return

        index+=1

def get_issue_detail(url):
    r = requests.get(url=url)
    if r is None:
        print("Link does not exist")
        return

    try:
        soup=BeautifulSoup(r.text,"html.parser")
        link = get_detail_link(soup)
        parse_issue_data(link)

    except Exception as err:
        print("--------ERROR!!! Unable to get explanation of vulnerability")
        print(err)


def get_detail_link(soup):
    link = soup.find(class_="external-link")
    return f"https://vulncat.fortify.com{link['href']}"


def parse_issue_data(url):
    r = requests.get(url=url)
    if r is None:
        print("Link does not exist")
        return

    try:
        new_soup=BeautifulSoup(r.text,"html.parser")
        content = new_soup.find(class_="tab-content")
        
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
            
def order_soup(url:str):
    soup:BeautifulSoup=None
    try:
        r=requests.get(url)
        soup=BeautifulSoup(r.text, 'html.parser')
    except requests.exceptions.RequestException as ex:
        print("There was an error with the request")
    except Exception as ex:
        print("An unknown exception has occured")
    finally:
        return soup

if __name__=="__main__":

    base_url="https://vulncat.fortify.com"
    url = "https://vulncat.fortify.com/en/weakness?q="
    category_url="https://vulncat.fortify.com/en/weakness?category="

    r = requests.get(url=url)

    soup = BeautifulSoup(r.text, 'html.parser')

    #parse_categories(soup)

    navigatePages(soup, base_url)
