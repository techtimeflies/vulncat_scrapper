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
        print(f"{category}*\nHyper-Link:{link}*")
        if index<=3:
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
        html = new_soup.find(class_="t")
        print("\n\nSummary\n" + html.text +"*")

        html = new_soup.find(class_="detail-hidden")
        print(html.text + "*")

    except Exception as err:
        print("--------ERROR!!! Unable to get explanation of vulnerability")
        print(err)

if __name__=="__main__":

    url = "https://vulncat.fortify.com/en/weakness?q="
    category_url="https://vulncat.fortify.com/en/weakness?category="

    r = requests.get(url=url)

    soup = BeautifulSoup(r.text, 'html.parser')

    parse_categories(soup)
