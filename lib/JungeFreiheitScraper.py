# -*- coding: utf-8 -*-
"""
Created on Sat May 26 18:09:57 2018

@author: Luc
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import logging
import os.path


def scrape(dirpath):
    logger = logging.getLogger('root')
    logger.info('start scraping junge freiheit')

    # Websites to scrape
    URL = 'https://jungefreiheit.de/kategorie/politik/'
    PAGE = urlopen(URL)
    soup_mainpage = BeautifulSoup(PAGE, 'html.parser')

    # get all article URLs
    article_links = []
    for iteration in range(0, 10):
        try:
            if iteration > 0:
                nextUrlTag = soup_mainpage.find('a', href=True, text=re.compile('Nächste Seite'))
                URL = nextUrlTag['href']
                PAGE = urlopen(URL)
                soup_mainpage = BeautifulSoup(PAGE, 'html.parser')
            for link in soup_mainpage.findAll('a', attrs={'href': re.compile("^https://jungefreiheit.de/.*")}):
                if 'politik' in link['href'] and '2018' in link['href'] and '/#comments' not in link['href']:  # eliminate non-articles - SPON marks artikels with -a-
                    article_links.append(link['href'])
        except Exception:
            logger.exception("Error while fetching links")

    article_links = list(set(article_links))  # eliminate duplicate entries

    links = os.path.join(dirpath, "articleLinks\\jfLinks.txt")
    linkFile = open(links, 'w+')
    for link in article_links:
        linkFile.write("%s\n" % link)

    # get article text and save it to file
    print(len(article_links))
    for idx, article in enumerate(article_links):
        try:
            article_url = urlopen(article)
            soup_article = BeautifulSoup(article_url, 'html.parser')
            article = soup_article.find("div", {"class": "entry-content"}).findAll('p')
            text = ''
            for element in article:
                text += '\n' + ''.join(element.findAll(text=True))
            replace = re.compile('junge freiheit', re.IGNORECASE)
            text = replace.sub(text, text)
            fileId = 'articles\\JF\\JF_' + str(idx) + '.txt'
            fileName = os.path.join(dirpath, fileId)
            sponFile = open(fileName, 'w+', encoding='utf-8')
            sponFile.write("%s\n" % text)
            sponFile.close
        except Exception:
            print(Exception)
            logger.exception("Error while parsing")




