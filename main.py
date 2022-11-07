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
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            if url_check(link.get('href'), links):
                links.append(link.get('href'))
        webcrawler(links, crawl)
    except HTTPError:
        print(f"Unable to open {url}.")
        #if len(links) >= 60:
        #    return
'''
Url_check() filters out any potentially unwanted links using terms
I found to be impactful. It takes a url and a list of links as 
arguments and returns True or False depending on if the URL
is "good" or not.
'''


def url_check(url, links):
    # filter through the potential links
    if url not in links:
        return True
    return False


'''
Main() is primarily a driver function. It takes no arguments and returns
nothing. It creates the directories for all the scraped and cleaned 
files and then calls the various functions to build the eventual 
knowledge base.
'''


def main():
    url = 'https://www.utdallas.edu/'  # root page
    links = [url]
    webcrawler(links, 0)
    print(links)
    outFile = open("results.p", "wb")
    pickle.dump(links, outFile)


if __name__ == '__main__':
    main()
