"""
    Name:   Kathryn Kingsley and Jonathan Yu
    UTID:   KLK170230
    Class:  NLP CS4395.001
    Date:   Fall 2022
    Desc.:  This is the main .py file for the chatbot project. Some code inspired by
            Dr. Karen Mazidi's book:
            K. Mazidi, “13. Information Extraction,” in Exploring NLP  with Python: Building
            Understanding Through Code, First., 2019, p. 147 - 154.

"""
from urllib import request  # to work with urls
from urllib.error import HTTPError  # to catch errors
import requests as requests
from bs4 import BeautifulSoup  # to work with html data
import re  # needed for regex in webcrawler

'''
The webcrawler() takes a starting link and extracts related
links from a page. It takes the starting URL as an argument
and returns a list of valuable links. It is called by main().
'''


def webcrawler(links, crawl):
    url = links[crawl]
    crawl += 1
    if crawl > len(links):
        return
    # open the url and get in html format
    try:
        html = request.urlopen(url).read().decode('utf8')
    except HTTPError:
        print("Unable to open webpage. Exiting program...")
        exit(1)
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
        if url_check(link.get('href'), links):
            links.append(link.get('href'))
        if len(links) >= 10:
            return
    webcrawler(links, crawl)


'''
Url_check() filters out any potentially unwanted links using terms
I found to be impactful. It takes a url and a list of links as 
arguments and returns True or False depending on if the URL
is "good" or not.
'''


def url_check(url, links):
    # filter through the potential links
    wanted = ['graduation', 'graduate', '']
    unwanted = ['2021', '2019']
    if any(word in str(url) for word in wanted):
        if not any(word in str(url) for word in unwanted):
            if url not in links:
                return True
    return False


def allurls(links, crawl):
    url = links[crawl]
    crawl += 1
    # open the url and get in html format
    try:
        html = request.urlopen(url).read().decode('utf8')
    except HTTPError:
        print("Unable to open webpage. Exiting program...")
        exit(1)
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
        links.append(link.get('href'))
        if len(links) > 100:
            return
    allurls(links, crawl)


'''
Main() is primarily a driver function. It takes no arguments and returns
nothing. It creates the directories for all the scraped and cleaned 
files and then calls the various functions to build the eventual 
knowledge base.
'''


def main():
    url = 'https://registrar.utdallas.edu/graduation/'  # root page
    links = [url]
    allurls(links, 0)
    # webcrawler(links, 0)
    print(links)


if __name__ == '__main__':
    main()
